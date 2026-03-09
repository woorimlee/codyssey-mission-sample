"""
멀티 에이전트 동화 생성 파이프라인 — 핵심 코드

Writer Agent + Illustrator Agent + Safety Checker + Consistency Reporter
LangChain 기반 멀티 에이전트 구조의 레퍼런스 구현.

이 파일은 전체 웹 서비스가 아닌, 에이전트 파이프라인의 핵심 로직만 담고 있다.
실제 서비스에서는 FastAPI 엔드포인트, DB 저장, 프론트엔드 연동이 추가되어야 한다.
"""

# ====================================================================== #
#  의존성
# ====================================================================== #
#
# pip install langchain langchain-openai openai pydantic
#
# 이미지 생성은 OpenAI DALL-E 3 또는 Stable Diffusion 중 선택.
# 아래 코드는 DALL-E 3 기준이며, Stable Diffusion 사용 시
# IllustratorAgent.generate_image()만 교체하면 된다.

import os
import json
from typing import Optional
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser


# ====================================================================== #
#  데이터 모델
# ====================================================================== #

class CharacterProfile(BaseModel):
    """캐릭터 외형 프로필 — 일관성 유지의 핵심."""
    name: str
    species: str          # 예: "rabbit"
    fur_color: str        # 예: "white"
    outfit: str           # 예: "tiny silver armor and a blue cape"
    accessories: str      # 예: "small wooden sword"
    eye_description: str  # 예: "round bright eyes"
    other_features: str   # 예: "pink inner ears"

    def to_anchor_prompt(self) -> str:
        """
        모든 이미지 프롬프트에 반복 삽입할 캐릭터 앵커 문구를 생성한다.
        이 문구가 씬마다 정확히 동일해야 캐릭터 일관성이 유지된다.
        """
        return (
            f"a cute small {self.fur_color} {self.species} wearing {self.outfit}, "
            f"{self.eye_description}, {self.other_features}, "
            f"holding {self.accessories}"
        )


class Scene(BaseModel):
    """하나의 장면(컷)."""
    scene_id: int
    title: str
    narration: str           # 동화 텍스트
    visual_description: str  # 이미지 생성용 장면 묘사
    image_prompt: str = ""   # 최종 조합된 프롬프트
    image_url: str = ""      # 생성된 이미지 URL


class Story(BaseModel):
    """전체 동화."""
    work_id: str
    title: str
    genre: str
    art_style: str
    character: CharacterProfile
    scenes: list[Scene]


class ConsistencyCheckResult(BaseModel):
    """일관성 체크 결과."""
    work_id: str
    scene_id: int
    checks: dict[str, bool]  # {"fur_color": True, "outfit": False, ...}
    score: float
    notes: str = ""


# ====================================================================== #
#  Writer Agent — 스토리 텍스트 생성
# ====================================================================== #

WRITER_SYSTEM_PROMPT = """당신은 어린이 동화 작가 에이전트입니다.

사용자가 제공한 장르, 주인공 특징, 줄거리를 바탕으로
최소 4개의 장면(Scene)을 생성합니다.

각 장면에는 반드시 다음을 포함합니다:
1. title: 장면 제목 (한글, 짧게)
2. narration: 동화 본문 텍스트 (아이가 읽을 수 있는 문체)
3. visual_description: 이미지 생성용 시각 묘사 (영어, 구체적)
   - 반드시 포함: 장소, 시간대, 조명, 인물의 행동/표정, 분위기
   - 캐릭터 외형은 포함하지 마세요 (별도 앵커로 결합됩니다)

스토리 구조는 기승전결을 따릅니다:
- 씬 1: 기(起) — 평화로운 일상 소개
- 씬 2: 승(承) — 문제/갈등 발생
- 씬 3: 전(轉) — 클라이맥스
- 씬 4: 결(結) — 해결/교훈

JSON 형식으로만 응답하세요."""

WRITER_USER_TEMPLATE = """장르: {genre}
주인공: {character_description}
줄거리: {plot}
화풍: {art_style}

위 내용을 바탕으로 4개 장면을 생성하세요.
{format_instructions}"""


class WriterAgent:
    """스토리 텍스트를 생성하는 작가 에이전트."""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.8)
        self.parser = PydanticOutputParser(pydantic_object=Story)

    def generate_scenes(self, genre: str, character: CharacterProfile,
                        plot: str, art_style: str) -> list[Scene]:
        """줄거리를 받아 장면별 텍스트를 생성한다."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", WRITER_SYSTEM_PROMPT),
            ("human", WRITER_USER_TEMPLATE),
        ])

        chain = prompt | self.llm

        response = chain.invoke({
            "genre": genre,
            "character_description": f"{character.name} — {character.to_anchor_prompt()}",
            "plot": plot,
            "art_style": art_style,
            "format_instructions": self.parser.get_format_instructions(),
        })

        # 파싱 (실패 시 기본 구조 반환)
        try:
            parsed = json.loads(response.content)
            scenes = []
            for i, s in enumerate(parsed.get("scenes", []), 1):
                scenes.append(Scene(
                    scene_id=i,
                    title=s.get("title", f"장면 {i}"),
                    narration=s.get("narration", ""),
                    visual_description=s.get("visual_description", ""),
                ))
            return scenes
        except Exception:
            # LLM 출력 파싱 실패 시 에러 핸들링
            raise ValueError(f"Writer Agent 출력 파싱 실패: {response.content[:200]}")


# ====================================================================== #
#  Illustrator Agent — 이미지 프롬프트 조합 및 생성
# ====================================================================== #

# 화풍별 스타일 앵커
STYLE_ANCHORS = {
    "watercolor": "children's book illustration, soft watercolor style, warm pastel colors, gentle brushstrokes, storybook aesthetic, no text",
    "cartoon": "children's cartoon illustration, bold outlines, bright vivid colors, playful style, clean digital art, no text",
    "pixel": "cute pixel art style, 16-bit RPG aesthetic, warm retro colors, detailed pixel characters, no text",
}


class IllustratorAgent:
    """이미지 프롬프트를 조합하고 생성 API를 호출하는 삽화가 에이전트."""

    def __init__(self, api_key: Optional[str] = None):
        """
        api_key: OpenAI API 키 (DALL-E 3 사용 시)
        Stable Diffusion 사용 시 이 클래스의 generate_image()를 오버라이드
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def compose_prompt(self, scene: Scene, character: CharacterProfile,
                       art_style: str) -> str:
        """
        캐릭터 앵커 + 장면 묘사 + 화풍 앵커를 조합하여
        최종 이미지 프롬프트를 생성한다.

        조합 순서:
        1. 캐릭터 앵커 (매 씬 동일 → 일관성 유지)
        2. 장면별 시각 묘사 (Writer가 생성)
        3. 화풍 앵커 (매 씬 동일 → 스타일 통일)
        """
        character_anchor = character.to_anchor_prompt()
        style_anchor = STYLE_ANCHORS.get(art_style, STYLE_ANCHORS["watercolor"])

        prompt = f"{character_anchor}. {scene.visual_description}. {style_anchor}."
        scene.image_prompt = prompt
        return prompt

    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """
        DALL-E 3 API를 호출하여 이미지를 생성한다.
        반환: 이미지 URL

        Stable Diffusion 사용 시 이 메서드만 교체하면 된다.
        """
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )

        return response.data[0].url


# ====================================================================== #
#  Safety Checker — 유해 콘텐츠 필터링
# ====================================================================== #

# 유해 키워드 목록 (간소화된 예시)
BLOCKED_KEYWORDS = [
    "violence", "blood", "weapon", "gun", "death", "kill",
    "sexual", "nude", "drug", "alcohol", "horror", "gore",
    "폭력", "피", "무기", "죽음", "선정", "마약", "공포",
]


class SafetyChecker:
    """입력 텍스트와 생성 결과의 유해성을 검사한다."""

    @staticmethod
    def check_text(text: str) -> tuple[bool, str]:
        """
        텍스트에 유해 키워드가 포함되어 있는지 검사한다.

        Returns:
            (is_safe, message)
        """
        text_lower = text.lower()
        for keyword in BLOCKED_KEYWORDS:
            if keyword in text_lower:
                return False, f"유해 키워드 감지: '{keyword}'"
        return True, "PASS"

    @staticmethod
    def check_image_prompt(prompt: str) -> tuple[bool, str]:
        """이미지 프롬프트의 유해성을 검사한다."""
        return SafetyChecker.check_text(prompt)

    @staticmethod
    def check_with_moderation_api(text: str) -> tuple[bool, str]:
        """
        OpenAI Moderation API를 사용한 정밀 검사.
        프로덕션 환경에서는 이 방법을 권장한다.
        """
        from openai import OpenAI
        client = OpenAI()
        response = client.moderations.create(input=text)
        result = response.results[0]

        if result.flagged:
            categories = [
                cat for cat, flagged in result.categories.model_dump().items()
                if flagged
            ]
            return False, f"Moderation API 플래그: {', '.join(categories)}"
        return True, "PASS"


# ====================================================================== #
#  Consistency Reporter — 일관성 테스트 리포트
# ====================================================================== #

class ConsistencyReporter:
    """
    생성된 이미지의 캐릭터 일관성을 검증하고 리포트를 생성한다.

    실제 구현에서는 이미지를 Vision LLM(GPT-4V 등)에 보내 검증하거나,
    CLIP 기반 유사도를 측정할 수 있다. 여기서는 프롬프트 기반 검증을 사용한다.
    """

    def __init__(self, character: CharacterProfile):
        self.character = character
        self.check_items = {
            "fur_color": character.fur_color,
            "outfit": character.outfit,
            "accessories": character.accessories,
            "eye_description": character.eye_description,
            "other_features": character.other_features,
        }

    def check_prompt_consistency(self, scene: Scene) -> ConsistencyCheckResult:
        """
        프롬프트 수준에서 캐릭터 앵커가 정확히 포함되어 있는지 검증한다.
        (이미지 수준 검증의 대리 지표)
        """
        prompt_lower = scene.image_prompt.lower()
        checks = {}

        for key, expected in self.check_items.items():
            checks[key] = expected.lower() in prompt_lower

        passed = sum(checks.values())
        total = len(checks)
        score = passed / total if total > 0 else 0

        notes = ""
        failed = [k for k, v in checks.items() if not v]
        if failed:
            notes = f"누락 항목: {', '.join(failed)}"

        return ConsistencyCheckResult(
            work_id="",  # 파이프라인에서 설정
            scene_id=scene.scene_id,
            checks=checks,
            score=score,
            notes=notes,
        )

    def check_with_vision_llm(self, scene: Scene) -> ConsistencyCheckResult:
        """
        Vision LLM을 사용하여 실제 이미지에서 캐릭터 특징을 검증한다.
        (프로덕션 환경 권장)

        이 메서드는 이미지 URL이 필요하며, GPT-4V 등을 사용한다.
        """
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4o", max_tokens=1000)
        anchor = self.character.to_anchor_prompt()

        prompt = f"""아래 이미지에서 캐릭터의 특징을 확인하세요.

기대하는 캐릭터: {anchor}

각 항목이 이미지에서 확인 가능한지 JSON으로 답하세요:
- fur_color: {self.character.fur_color} 확인 가능? (true/false)
- outfit: {self.character.outfit} 확인 가능? (true/false)
- accessories: {self.character.accessories} 확인 가능? (true/false)
- eye_description: {self.character.eye_description} 확인 가능? (true/false)
- other_features: {self.character.other_features} 확인 가능? (true/false)

JSON만 응답하세요."""

        # Vision LLM 호출 (이미지 URL 필요)
        response = llm.invoke([
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": scene.image_url}},
            ]}
        ])

        try:
            checks = json.loads(response.content)
            passed = sum(checks.values())
            total = len(checks)
            return ConsistencyCheckResult(
                work_id="",
                scene_id=scene.scene_id,
                checks=checks,
                score=passed / total,
            )
        except Exception:
            return ConsistencyCheckResult(
                work_id="",
                scene_id=scene.scene_id,
                checks={k: False for k in self.check_items},
                score=0.0,
                notes="Vision LLM 응답 파싱 실패",
            )

    def generate_report(self, scenes: list[Scene], work_id: str) -> dict:
        """전체 씬에 대한 일관성 리포트를 생성한다."""
        results = []
        for scene in scenes:
            result = self.check_prompt_consistency(scene)
            result.work_id = work_id
            results.append(result)

        total_score = sum(r.score for r in results) / len(results) if results else 0
        failed_scenes = [r.scene_id for r in results if r.score < 1.0]

        return {
            "work_id": work_id,
            "total_scenes": len(scenes),
            "average_score": round(total_score * 100, 1),
            "failed_scenes": failed_scenes,
            "details": [r.model_dump() for r in results],
        }


# ====================================================================== #
#  파이프라인 — 전체 흐름 통합
# ====================================================================== #

def run_pipeline(genre: str, character_data: dict, plot: str,
                 art_style: str = "watercolor",
                 generate_images: bool = False) -> dict:
    """
    전체 동화 생성 파이프라인을 실행한다.

    1. 캐릭터 프로필 생성
    2. Writer Agent — 장면 텍스트 생성
    3. Safety Check — 텍스트 유해성 검사
    4. Illustrator Agent — 이미지 프롬프트 조합
    5. Safety Check — 프롬프트 유해성 검사
    6. (선택) 이미지 생성 API 호출
    7. Consistency Report — 일관성 검증

    Parameters:
        genre: 장르
        character_data: CharacterProfile 필드 딕셔너리
        plot: 줄거리
        art_style: 화풍 ("watercolor", "cartoon", "pixel")
        generate_images: True이면 실제 이미지 생성 (API 키 필요)

    Returns:
        Story + ConsistencyReport 딕셔너리
    """
    import uuid

    work_id = str(uuid.uuid4())[:8]
    character = CharacterProfile(**character_data)
    safety = SafetyChecker()

    # 1. 입력 텍스트 안전성 검사
    is_safe, msg = safety.check_text(f"{genre} {plot}")
    if not is_safe:
        return {"error": f"입력 텍스트 차단: {msg}"}

    print(f"[Pipeline] work_id: {work_id}")
    print(f"[Pipeline] 캐릭터 앵커: {character.to_anchor_prompt()}")

    # 2. Writer Agent — 장면 생성
    print("[Writer Agent] 장면 생성 중...")
    writer = WriterAgent()
    scenes = writer.generate_scenes(genre, character, plot, art_style)
    print(f"[Writer Agent] {len(scenes)}개 장면 생성 완료")

    # 3. 텍스트 안전성 검사
    for scene in scenes:
        is_safe, msg = safety.check_text(scene.narration)
        if not is_safe:
            print(f"[Safety] 씬 {scene.scene_id} 차단: {msg}")
            scene.narration = "(유해 콘텐츠가 감지되어 차단되었습니다)"
        else:
            print(f"[Safety] 씬 {scene.scene_id} 텍스트 PASS")

    # 4. Illustrator Agent — 프롬프트 조합
    illustrator = IllustratorAgent()
    for scene in scenes:
        prompt = illustrator.compose_prompt(scene, character, art_style)
        print(f"[Illustrator] 씬 {scene.scene_id} 프롬프트 조합 완료")

        # 프롬프트 안전성 검사
        is_safe, msg = safety.check_image_prompt(prompt)
        if not is_safe:
            print(f"[Safety] 씬 {scene.scene_id} 이미지 프롬프트 차단: {msg}")
            scene.image_prompt = ""
            continue

        # 5. (선택) 이미지 생성
        if generate_images:
            print(f"[Illustrator] 씬 {scene.scene_id} 이미지 생성 중...")
            scene.image_url = illustrator.generate_image(prompt)
            print(f"[Illustrator] 씬 {scene.scene_id} 이미지 생성 완료")

    # 6. 일관성 리포트
    reporter = ConsistencyReporter(character)
    report = reporter.generate_report(scenes, work_id)
    print(f"[Consistency] 일관성 점수: {report['average_score']}%")

    # 결과 조합
    story = Story(
        work_id=work_id,
        title=f"동화: {character.name}의 모험",
        genre=genre,
        art_style=art_style,
        character=character,
        scenes=scenes,
    )

    return {
        "story": story.model_dump(),
        "consistency_report": report,
    }


# ====================================================================== #
#  실행 예시
# ====================================================================== #

if __name__ == "__main__":
    result = run_pipeline(
        genre="판타지 동화",
        character_data={
            "name": "달",
            "species": "rabbit",
            "fur_color": "white",
            "outfit": "tiny silver armor and a blue cape",
            "accessories": "a small wooden sword",
            "eye_description": "round bright eyes",
            "other_features": "pink inner ears",
        },
        plot="어두운 안개가 숲을 뒤덮자, 용감한 토끼 기사 달이 숲의 빛을 되찾기 위해 모험을 떠난다",
        art_style="watercolor",
        generate_images=False,  # True로 변경 시 DALL-E 3 호출
    )

    print("\n=== 결과 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))
