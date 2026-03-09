# Codyssey Mission Samples

코디세이 **AI 올인원** / **AI 네이티브** 과정의 대표 미션 샘플 코드 모음입니다.

각 미션의 요구사항을 충족하는 레퍼런스 구현을 제공하며, 커리큘럼 검토 및 내부 공유 목적으로 관리합니다.

---

## 과정 소개

| 과정 | 대상 | 기간 |
|------|------|------|
| **AI 올인원** (AI All-in-One) | 개발 경험이 있는 학습자 | 약 18개월 |
| **AI 네이티브** (AI Native) | 비전공 / 비개발 학습자 | 약 5개월 |

---

## 미션 목록

### AI 올인원

| # | 미션명 | 핵심 주제 | 폴더 |
|---|--------|-----------|------|
| 8 | Mini Redis 구축 | 해시맵, 이중 연결 리스트, 힙, LRU, TTL | [`8_Mini Redis/`](./8_Mini%20Redis/) |
| 19 | 문서 스캐너 | OpenCV, 엣지 검출, 투시 변환, 적응형 이진화 | [`19_Document Scanner/`](./19_Document%20Scanner/) |

### AI 네이티브

| # | 미션명 | 핵심 주제 | 폴더 |
|---|--------|-----------|------|
| 2 | GenAI 기초 2: 멀티모달 콘텐츠 제작 | 멀티모달 AI 도구, 스토리보드, 브랜드 광고 (샘플) | [`AI_Native_2_GenAI/`](./AI_Native_2_GenAI/) |

---

## 실행 방법

### AI 올인원 (코드 미션)

각 미션 폴더에 진입한 뒤 `main.py`를 실행합니다.

```bash
# 예시: Mini Redis
cd "8_Mini Redis"
python main.py

# 예시: 문서 스캐너
cd "19_Document Scanner"
pip install opencv-python numpy
python main.py scan "./images/images (N).jpg"     # 단일 스캔
python main.py trackbar "./images/images (N).jpg" # 트랙바 모드
python main.py batch ./images                     # 배치 스캔
python main.py webcam                             # 웹캠 모드
python main.py eda ./images                       # 히스토그램 EDA
```

> **문서 스캐너 테스트 이미지**는 아래 Google Drive에서 다운로드 후 `19_Document Scanner/images/` 폴더에 넣어주세요.
> [Google Drive 링크](https://drive.google.com/drive/folders/1-Eqv09FmsdJ7ywOZag8wg-zHomjIOGKs?usp=drive_link)

Python 3.13 이상이 필요합니다. 미션별 필요 라이브러리는 각 폴더의 코드를 참고하세요.

### AI 네이티브 (기획/도구 활용 미션)

> **미션 2**: 스토리보드 샘플 — Gemini 특화(새벽책방). 새벽책방은 실제 생성 결과물(영상/BGM)을 Google Drive에서 제공 ('Late_Night_Bookshop'.zip)
> [Google Drive 링크](https://drive.google.com/drive/folders/1-Eqv09FmsdJ7ywOZag8wg-zHomjIOGKs?usp=drive_link)

---

## 프로젝트 구조

### AI 올인원

```
codyssey-mission-samples/
├── README.md
├── 8_Mini Redis/
│   ├── main.py                  # CLI 진입점 (REPL)
│   ├── doubly_linked_list.py    # 이중 연결 리스트
│   ├── hash_map.py              # 체이닝 기반 해시맵
│   ├── min_heap.py              # 최소 힙 (TTL 관리)
│   └── mini_redis.py            # 코어 엔진 + 명령어 파서
├── 19_Document Scanner/
│   ├── main.py                  # CLI 진입점 (5개 모드)
│   ├── core/                    # 핵심 이미지 처리
│   │   ├── preprocessing.py
│   │   ├── contour_detector.py
│   │   ├── perspective_transform.py
│   │   ├── postprocessing.py
│   │   └── scanner.py
│   ├── ui/                      # 사용자 인터페이스
│   │   ├── trackbar_ui.py
│   │   └── webcam.py
│   ├── analysis/                # 분석 도구
│   │   └── eda.py
│   └── EVALUATION.md            # 성능 평가 보고서
└── ...                          # 추후 미션 추가
```

### AI 네이티브

```
codyssey-mission-samples/
├── 2_GenAI Multimodal/
│   ├── README.md                    # 미션 개요 + 샘플 범위 설명
│   ├── storyboard.md                # 샘플: 새벽책방 (4씬, 32초, Gemini 특화)
└── ...                              # 추후 미션 추가
```

---

## 참고

- 이 레포지토리의 코드는 **채점 기준이 아닌 레퍼런스 구현**입니다.
- 미션별 상세 요구사항은 각 과정의 미션 문서를 참고하세요.
- 학습자에게 직접 공유하는 용도가 아닌, 내부 검토용입니다.
