# TP_C. 멀티모달 기반 AI 웹툰/동화 창작 플랫폼

Writer + Illustrator 멀티 에이전트가 협업하여 텍스트 스토리를 동화로 변환하는 플랫폼.

> **⚠️ 현재 데모 상태 안내**
>
> 이 데모는 **수채화풍(Watercolor) 동화 1편**만 포함되어 있습니다.
> 실제 서비스에서는 만화풍, 픽셀아트 등 다양한 화풍을 선택할 수 있으나,
> 현재 샘플은 **"숲속의 기사 토끼" 수채화풍 4컷**으로만 구성되어 있습니다.
> 이미지는 Gemini로 직접 생성한 결과물이며, API 키 없이 로컬에서 바로 실행 가능합니다.

---

## 샘플 구성

이 샘플은 **체험형 데모 + 핵심 백엔드 코드** 하이브리드 구성.

| 파일 | 역할 |
|------|------|
| `demo.jsx` | 체험형 데모 웹앱 (React). 로컬에서 API 키 없이 실행 가능 |
| `core_agents.py` | 핵심 백엔드 코드. LangChain 멀티 에이전트 구조, 프롬프트 조합, Safety Check, 일관성 검증 |
| `sample_images/` | Gemini로 생성한 동화 4컷 이미지 |

---

## 파일 구조

```
AI_Native_TP_Multimodal_Webtoon/
├── README.md               # 이 파일
├── demo.jsx                # 체험형 데모 (로컬 실행 가능)
├── core_agents.py          # 멀티 에이전트 파이프라인 핵심 코드
└── sample_images/          # Gemini 생성 이미지
    ├── scene01_forest_entrance.png
    ├── scene02_dark_mist.png
    ├── scene03_confrontation.png
    └── scene04_happy_ending.png
```

---

## 샘플 동화: 숲속의 기사 토끼

| 항목 | 내용 |
|------|------|
| 제목 | 숲속의 기사 토끼 |
| 장르 | 어린이 판타지 동화 |
| 주인공 | 토끼 기사 "달" — 흰 털, 은색 갑옷, 파란 망토, 나무 검 |
| 화풍 | 수채화풍 그림책 |

### 스토리 흐름

```
씬 1 (기) 햇살 가득한 숲 입구에 선 토끼 기사
씬 2 (승) 보라색 안개가 숲을 뒤덮고, 안개 속으로 들어감
씬 3 (전) 안개의 왕과 대면, 나무 검에서 금빛이 퍼짐
씬 4 (결) 안개 걷히고 숲에 평화가 돌아옴, 동물 친구들과 축하
```

---

## 핵심 아키텍처

### 멀티 에이전트 파이프라인

```
사용자 입력 (장르, 캐릭터, 줄거리)
    ↓
[Safety Checker] 입력 텍스트 유해성 검사
    ↓
[Writer Agent] LLM으로 장면별 텍스트 + 시각 묘사 생성
    ↓
[Safety Checker] 생성된 텍스트 유해성 검사
    ↓
[Illustrator Agent] 캐릭터 앵커 + 장면 묘사 + 화풍 앵커 조합
    ↓
[Safety Checker] 이미지 프롬프트 유해성 검사
    ↓
[Image API] DALL-E 3 / Stable Diffusion / Gemini 이미지 생성
    ↓
[Consistency Reporter] 캐릭터 일관성 검증 리포트
    ↓
결과 저장 (DB) + 렌더링 (웹)
```

### 캐릭터 일관성 유지 — 앵커 프롬프트 전략

모든 씬의 이미지 프롬프트는 아래 구조로 조합된다:

```
[캐릭터 앵커] + [장면별 시각 묘사] + [화풍 앵커]
```

- 캐릭터 앵커: `CharacterProfile.to_anchor_prompt()` — 매 씬 동일
- 화풍 앵커: `STYLE_ANCHORS[art_style]` — 매 씬 동일
- 장면별 묘사: Writer Agent가 생성 — 씬마다 다름

이 구조 덕분에 캐릭터 외형과 화풍은 일관되면서 장면만 변화한다.

---

## 이미지 생성 방법

`gemini_prompts.md`의 프롬프트를 Gemini에 입력하여 이미지를 생성한다. 생성 후 `sample_images/` 폴더에 배치하거나 Google Drive에 업로드한다.

생성된 이미지 4장은 `sample_images/` 폴더에 포함되어 있다.

---

## 데모 실행 방법 (로컬, API 키 불필요)

샘플 이미지가 포함된 오프라인 데모. Node.js만 있으면 됩니다.

> **샘플 이미지**: `AIN_TP_sample_images.zip`을 아래 Google Drive에서 다운로드 후 `sample_images/` 폴더에 압축 해제하세요.
> [Google Drive 링크](https://drive.google.com/drive/folders/1-Eqv09FmsdJ7ywOZag8wg-zHomjIOGKs?usp=drive_link)

```bash
# 1. Vite React 프로젝트 생성
npm create vite@latest webtoon-demo -- --template react
cd webtoon-demo

# 2. demo.jsx를 App으로 교체
copy "..\demo.jsx" src\App.jsx          # Windows
# cp ../demo.jsx src/App.jsx            # Mac/Linux

# 3. 이미지를 public 폴더에 복사
xcopy "..\sample_images" public\sample_images\ /E   # Windows
# cp -r ../sample_images public/                      # Mac/Linux

# 4. 실행
npm install
npm run dev
```

브라우저에서 `http://localhost:5173` 접속. 체험 가능한 기능:

- 스토리 입력 폼 (장르, 화풍, 주인공, 줄거리)
- 에이전트 생성 과정 로그 (Writer → Safety → Illustrator 애니메이션)
- 스토리북 뷰어 (Gemini 생성 이미지 + 동화 텍스트, 페이지 넘기기)
- 갤러리 (2×2 그리드 뷰, 저장/공유 버튼)
- 일관성 리포트 (8개 항목 × 4씬 체크 테이블)

---

## 백엔드 코드 사용법

`core_agents.py`는 독립 실행 가능한 파이프라인 코드.

```bash
pip install langchain langchain-openai openai pydantic

# API 키 설정
export OPENAI_API_KEY="sk-..."

# 실행 (이미지 생성 없이 텍스트+프롬프트만)
python core_agents.py

# 이미지 생성 포함
# core_agents.py 하단의 generate_images=True로 변경 후 실행
```

### 핵심 클래스 구조

| 클래스 | 역할 |
|--------|------|
| `CharacterProfile` | 캐릭터 외형 프로필 + 앵커 프롬프트 생성 |
| `WriterAgent` | LLM으로 장면별 텍스트 생성 |
| `IllustratorAgent` | 프롬프트 조합 + 이미지 API 호출 |
| `SafetyChecker` | 텍스트/프롬프트 유해성 필터링 |
| `ConsistencyReporter` | 캐릭터 일관성 검증 + 리포트 생성 |
