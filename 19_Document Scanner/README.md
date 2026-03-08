# 19. 문서 스캐너 (Document Scanner)

OpenCV 기반 CLI 문서 스캐너. 비스듬하게 촬영된 문서를 자동으로 인식하고 반듯하게 펴준다.

---

## 이미지 처리 파이프라인

```
원본 이미지
  ↓  Grayscale 변환
  ↓  가우시안 블러 (노이즈 제거)
  ↓  Canny Edge Detection (엣지 검출)
  ↓  윤곽선 추출 + 사각형 검출 (approxPolyDP)
  ↓  좌표 정렬 (좌상-우상-우하-좌하, 직접 구현)
  ↓  투시 변환 (getPerspectiveTransform + warpPerspective)
  ↓  적응형 이진화 (Adaptive Thresholding)
최종 스캔본
```

---

## 실행 방법

```bash
pip install opencv-python numpy

# 단일 이미지 스캔
python main.py scan "./images/images (N).jpg"

# 트랙바 인터랙티브 모드 (블러/Canny 파라미터 실시간 조절)
python main.py trackbar "./images/images (N).jpg"

# 배치 스캔 (폴더 내 전체 이미지 + 성능 평가)
python main.py batch ./images

# 웹캠 실시간 스캔
python main.py webcam

# 이미지 EDA (히스토그램 분석)
python main.py eda ./images
```

> **문서 스캐너 테스트 이미지**는 아래 Google Drive에서 다운로드 후 `19_Document Scanner/images/` 폴더에 넣어주세요.
> [Google Drive 링크](https://drive.google.com/drive/folders/1-Eqv09FmsdJ7ywOZag8wg-zHomjIOGKs?usp=drive_link)

---

## 파일 구조

```
19_Document Scanner/
├── main.py                          # CLI 진입점 (5개 모드)
├── core/                            # 핵심 이미지 처리
│   ├── preprocessing.py             #   그레이스케일, 가우시안 블러, Canny 엣지
│   ├── contour_detector.py          #   윤곽선 추출, 면적 필터링, 사각형 검출
│   ├── perspective_transform.py     #   좌표 정렬 (직접 구현) + 투시 변환
│   ├── postprocessing.py            #   적응형 이진화, 샤프닝
│   └── scanner.py                   #   파이프라인 통합 + 다중 전략 자동 폴백
├── ui/                              # 사용자 인터페이스
│   ├── trackbar_ui.py               #   트랙바 인터랙티브 UI
│   └── webcam.py                    #   웹캠 실시간 검출
├── analysis/                        # 분석 도구
│   └── eda.py                       #   히스토그램 EDA 분석
├── README.md
└── EVALUATION.md                    # 성능 평가 보고서
```

---

## 다중 전략 자동 폴백

기본 파라미터(blur=5, Canny 50/150)로 실패할 경우, 자동으로 다음 전략을 순차 시도한다.

| 단계 | 전략 | 대응하는 상황 |
|------|------|--------------|
| 1 | 파라미터 변경 | 블러/임계값 조합 6가지 시도 |
| 2 | Morphology 보강 | 끊긴 엣지 연결 (dilate → erode) |
| 3 | 적응형 임계값 전처리 | 배경-문서 대비가 낮은 이미지 |
| 4 | 확장 epsilon | 극도로 어려운 케이스 (최후 수단) |

20장 테스트 기준: 기본 파라미터 75% → 다중 전략 적용 후 100% 검출.

---

## 핵심 구현 사항

**좌표 정렬 (외부 라이브러리 미사용)**
- x+y 합: 최소 → 좌상, 최대 → 우하
- y-x 차: 최소 → 우상, 최대 → 좌하

**used_memory 없이 동작**
- dict, set, collections 등 제한 사항 없음 (OpenCV, NumPy만 사용)

---

## 환경 요구사항

- Python 3.13+
- OpenCV (opencv-python >= 4.5)
- NumPy (numpy >= 1.20)
- 트랙바/imshow: 로컬 데스크톱 환경 권장 (GUI 필요)