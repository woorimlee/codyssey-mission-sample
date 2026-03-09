# 2. GenAI 기초 2: 멀티모달 콘텐츠 제작

AI 도구만으로 브랜드 광고 영상을 제작하는 프로젝트의 기획 문서 + 생성 결과물 샘플.

---

## 샘플 정답의 범위

이 미션은 AI 도구를 활용하여 실제 미디어(이미지/영상/오디오)를 생성하는 과제이므로, 샘플 정답은 **기획 문서(스토리보드)** + **Gemini로 생성한 영상/BGM 결과물**을 포함한다.

이 샘플이 보여주는 것:
- 씬별 필수 필드가 빠짐없이 채워진 문서화 수준
- Gemini 영상 생성 프롬프트 작성 예시
- 8초 단위 영상의 씬 간 연결 설계 방법
- BGM 프롬프트 작성 및 에셋 파일 관리 방식

---

## 파일 구조

```
2_GenAI Multimodal/
├── README.md               # 이 파일
└── storyboard.md           # 새벽책방 스토리보드 (4씬, 32초, Gemini 특화)
```

---

## 새벽책방 (Dawn Pages)

Gemini(Veo) 8초 영상 생성에 특화된 4씬 구성. **실제 영상/BGM 생성 결과물 포함.**

| 항목 | 내용 |
|------|------|
| 브랜드명 | 새벽책방 (Dawn Pages) |
| 컨셉 | 디카페인 커피 + 심야 독립서점 |
| 핵심 메시지 | "잠들기 전, 한 페이지." |
| 영상 길이 | 32초 (8초 × 4씬) |
| 스토리 구조 | 새벽 거리 → 가게 발견 → 내부(커피+책) → 브랜드 메시지 |
| 주요 도구 | Gemini (Veo) 영상 + BGM 생성 |

### 씬 흐름

```
씬 1 (0:00-0:08)  새벽 골목 트래킹, 끝에 불빛
        ↓ 불빛 → 가게 외관
씬 2 (0:08-0:16)  가게 발견, 문 열고 들어감
        ↓ 내부 진입 → 내부 장면
씬 3 (0:16-0:24)  내부 클로즈업, 커피+책
        ↓ 클로즈업 → 와이드
씬 4 (0:24-0:32)  외관 와이드 + 메시지 오버레이
```

### 에셋 파일

| 파일명 | 유형 |
|--------|------|
| Late_Night_Bookshop | 합본 영상 (32초) |
| Late_Night_Bookshop_Scene_1 | 씬 1 영상 (8초) |
| Late_Night_Bookshop_Scene_2 | 씬 2 영상 (8초) |
| Late_Night_Bookshop_Scene_3 | 씬 3 영상 (8초) |
| Late_Night_Bookshop_Scene_4 | 씬 4 영상 (8초) |
| Midnight_Rain_on_Cobblestones | BGM (30초) |

> **생성 결과물('Late_Night_Bookshop'.zip)**은 아래 Google Drive에서 확인할 수 있습니다.
> [Google Drive 링크](https://drive.google.com/drive/folders/1-Eqv09FmsdJ7ywOZag8wg-zHomjIOGKs?usp=drive_link)