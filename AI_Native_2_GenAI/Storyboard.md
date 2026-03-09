# 새벽책방 (Dawn Pages) — 32초 브랜드 영상 스토리보드

## 컨셉

| 항목 | 내용 |
|------|------|
| 브랜드명 | **새벽책방 (Dawn Pages)** |
| 업종 | 디카페인 커피 + 독립서점 (새벽 영업 특화) |
| 타겟 | 야근 후 잠들기 전 한 잔의 여유가 필요한 직장인 |
| 톤앤매너 | 미니멀, 시네마틱, 따뜻한 간접조명, 정적인 카메라 |
| 핵심 메시지 | **"잠들기 전, 한 페이지."** |
| USP | 디카페인이라 새벽에 마셔도 괜찮은 커피 + 밤에만 여는 서점 |

## 영상 구성

| 항목 | 값 |
|------|---|
| 총 길이 | 32초 (8초 × 4씬) |
| 생성 도구 | Google Gemini (Veo) — 씬당 8초 영상 |
| 화면 비율 | 16:9 |
| 스타일 | 시네마틱, 얕은 피사계 심도, 따뜻한 톤(3200K), 느린 카메라 움직임 |

## 에셋 파일 목록

| 파일명 | 유형 | 설명 |
|--------|------|------|
| Late_Night_Bookshop_Scene_1 | 영상 (8초) | 씬 1 — 새벽 거리 |
| Late_Night_Bookshop_Scene_2 | 영상 (8초) | 씬 2 — 가게 발견 |
| Late_Night_Bookshop_Scene_3 | 영상 (8초) | 씬 3 — 내부 (커피+책) |
| Late_Night_Bookshop_Scene_4 | 영상 (8초) | 씬 4 — 외관 와이드 + 메시지 |
| Midnight_Rain_on_Cobblestones | BGM (30초) | 로파이 피아노 |
| Late_Night_Bookshop | 합본 (32초) | 최종 편집본 |

---

## 씬 간 연결 설계

Gemini 8초 영상 4개를 이어붙이므로, **씬의 끝 프레임과 다음 씬의 첫 프레임이 시각적으로 연결**되어야 한다.

```
씬 1 끝: 인물이 골목 끝의 불빛을 향해 걸어감 (불빛이 화면 중앙)
    ↓ 연결: "불빛"이 공통 요소
씬 2 끝: 인물이 문을 열고 안으로 들어가며, 카메라도 함께 내부로 진입
    ↓ 연결: "내부 진입" 동선이 자연스럽게 씬 3의 내부 장면으로 이어짐
씬 3 끝: 커피잔과 펼쳐진 책의 클로즈업
    ↓ 연결: "클로즈업 → 와이드 전환" (같은 따뜻한 톤 유지)
씬 4:   가게 외관 와이드 샷 + 텍스트 오버레이 공간
```

---

## 씬 1 — 새벽 거리 (8초)

**의도:** 야근 후 텅 빈 도시의 고요함. 지친 걸음이지만 어딘가를 향하고 있다는 느낌.

| 항목 | 내용 |
|------|------|
| 화면 | 새벽 2시쯤의 서울 골목. 한국인 남성(코트 차림)이 카메라를 등지고 천천히 걸어간다. 골목 끝에 따뜻한 불빛 하나가 보인다. |
| 카메라 | 인물 뒤를 따라가는 슬로우 트래킹 샷. 약간 낮은 앵글. |
| 분위기 | 차가운 도시 톤(블루-그레이) + 골목 끝 따뜻한 불빛의 대비 |
| 씬 끝 프레임 | 인물이 불빛에 가까워지며, 불빛이 화면을 채우기 시작 |

### Gemini 프롬프트

```
Cinematic slow tracking shot from behind. A young Korean man in a dark coat 
walks alone through a quiet narrow Seoul alley at 2am. The street is empty and 
slightly wet. Cool blue-gray city tones. At the end of the alley, a single warm 
golden light glows from a small shop. He walks steadily toward the light. Shallow 
depth of field, anamorphic lens flare from the distant light. Minimal movement, 
contemplative mood. 24fps cinematic look.
```

---

## 씬 2 — 가게 발견 (8초)

**의도:** 따뜻한 불빛의 정체가 드러남. "새벽책방"이라는 공간을 처음 보여주는 순간.

| 항목 | 내용 |
|------|------|
| 화면 | 작은 가게 외관. 나무 프레임 유리문, 안쪽에서 따뜻한 조명이 새어나옴. 문 옆에 작은 칠판 사인("DECAF ONLY / OPEN TILL DAWN"). 한국인 인물(코트 차림)이 문을 열고 안으로 들어간다. 카메라가 뒤를 따라가며 내부 빛이 점점 화면을 채운다. |
| 카메라 | 인물 뒤에서 따라가는 팔로우 샷 → 문을 열고 들어가는 동선을 따라 자연스럽게 내부로 진입 |
| 분위기 | 새벽 2시의 칠흑 같은 거리. 가게 문에서 새는 빛만이 유일한 광원. 문을 열고 들어가는 순간 어둠에서 따뜻함으로의 극적 전환 |
| 씬 끝 프레임 | 카메라가 인물을 따라 문 안으로 들어가며, 따뜻한 내부 빛이 화면을 가득 채움 |

### Gemini 프롬프트

```
Cinematic follow shot from behind at 2am. A young Korean man in a dark coat 
opens the wooden frame glass door of a small minimalist bookshop-cafe and walks 
inside. The street behind him is pitch dark, only the cafe doorway glows warm 
golden. The camera follows him through the doorway, transitioning from the dark 
empty street into the warm interior. A small chalkboard sign by the door reads 
"DECAF ONLY". Strong contrast between the dark 2am street and the warm light 
inside. Shallow depth of field, low-key lighting, cinematic 24fps.
```

---

## 씬 3 — 내부: 커피와 책 (8초)

**의도:** 공간 경험의 핵심. 디카페인 커피 한 잔과 책 한 권이 주는 고요한 위안.

| 항목 | 내용 |
|------|------|
| 화면 | 미니멀한 카페-서점 내부, 새벽 2시. 나무 테이블 위에 디카페인 라테 한 잔과 펼쳐진 책. 벽면에 책이 빼곡한 선반. 작은 테이블 램프의 은은한 간접조명만 켜져 있고, 창 밖은 칠흑. 인물(남성)의 손이 천천히 책장을 넘긴다. |
| 카메라 | 테이블 높이의 클로즈업에서 시작, 천천히 살짝 풀백하며 공간을 보여줌 |
| 분위기 | 어두운 공간에 램프 빛만 따뜻하게 비침. 창 밖 어둠과의 대비로 아늑함이 극대화 |
| 씬 끝 프레임 | 커피잔과 책의 탑다운에 가까운 클로즈업 |

### Gemini 프롬프트

```
Cinematic interior of a minimalist cafe-bookshop at 2am. Dim warm ambient 
lighting from small table lamps only, the window shows pitch black night outside. 
Wooden table with a white ceramic cup of latte and an open book. Bookshelves 
line the wall in the background, softly out of focus in shadow. A young man's hand slowly 
turns a page of the book. Camera starts as a close-up on the coffee and book, 
then slowly pulls back to reveal the intimate dimly-lit space. Low-key warm 
tones, shallow depth of field. Quiet, late-night contemplative atmosphere. 
24fps cinematic.
```

---

## 씬 4 — Outro: 메시지 (8초)

**의도:** 브랜드 메시지 전달. 가게 외관의 와이드 샷으로 마무리하며 여운을 남긴다.

| 항목 | 내용 |
|------|------|
| 화면 | 가게 외관 와이드 샷. 새벽 2시의 칠흑 같은 밤하늘. 가게 창문에서만 따뜻한 빛이 새어 나와 주변 바닥을 은은하게 비춤. 거리는 완전히 비어 있고 고요. 화면 중앙 하단에 텍스트 오버레이 공간 확보. |
| 카메라 | 정적인 와이드 샷. 거의 움직이지 않거나, 아주 느린 줌 아웃. |
| 분위기 | 칠흑의 밤거리에 이 가게만 빛나고 있는 느낌. "저 안에 누군가 있다"는 따뜻함 |
| 씬 끝 프레임 | 와이드 샷 유지 — 편집 시 텍스트/로고를 올릴 공간 |
| 오버레이 (편집 시 추가) | **새벽책방** / Before you sleep, one page. / DECAF ONLY · OPEN TILL DAWN |

### Gemini 프롬프트

```
Cinematic wide establishing shot of a small bookshop-cafe on a quiet street at 
2am. Completely dark night sky, no hint of dawn. The cafe is the only source of 
light, warm golden glow spilling from its windows onto the dark pavement. The 
street is completely empty and silent. Very slow subtle zoom out. The shop looks 
like the only living thing in the darkness. Minimalist composition with empty 
space in the lower third. Low-key lighting, cinematic 24fps, strong contrast 
between the dark surroundings and the single warm light source.
```

---

## 편집 가이드

### 영상 이어붙이기

```
[0:00-0:08]  씬 1 — 새벽 거리 (트래킹)
[0:08-0:16]  씬 2 — 가게 발견 (문 열림)
[0:16-0:24]  씬 3 — 내부 (커피+책)
[0:24-0:32]  씬 4 — 외관 와이드 + 메시지
```

### 씬 전환

- 씬 1→2: 컷 전환 또는 0.5초 크로스 디졸브 (불빛 → 가게 외관)
- 씬 2→3: 카메라가 내부로 진입한 상태에서 컷 → 내부 클로즈업으로 자연스럽게 연결
- 씬 3→4: 1초 크로스 디졸브 (클로즈업 → 와이드, 스케일 대비)

### 오디오

| 요소 | 파일명 | 내용 |
|------|--------|------|
| BGM | Midnight_Rain_on_Cobblestones | 로파이 피아노, 30초, 전체 영상 깔림 |
| 효과음 | (편집 시 추가) | 문 여는 소리(씬 2), 책장 넘기는 소리(씬 3) |
| 내레이션 (선택) | (편집 시 추가) | "잠들기 전, 한 페이지." — 씬 4 시작 부근 |

#### BGM Gemini 프롬프트

```
Lo-fi piano, soft and melancholic, late night cafe atmosphere, 
slow tempo 70bpm, minimal arrangement, instrumental only, 
warm vinyl texture, 30 seconds
```

### 텍스트 오버레이 (씬 4, 편집 시 추가)

```
[24초~28초]  새벽책방
[28초~32초]  Before you sleep, one page.
             DECAF ONLY · OPEN TILL DAWN
```

폰트: 산세리프 얇은 웨이트 (Pretendard Thin 또는 Noto Sans KR Light 권장)

---

## Gemini 프롬프트 작성 팁

### 씬 연결을 위한 핵심 원칙

1. **공통 시각 요소 유지**: 모든 씬에 "warm golden light"를 넣어 색감 일관성 확보
2. **카메라 방향 연속성**: 씬 1은 앞으로(트래킹), 씬 2는 정면, 씬 3은 뒤로(풀백), 씬 4는 정적 — 자연스러운 리듬
3. **톤 키워드 통일**: 모든 프롬프트에 `cinematic`, `24fps`, `shallow depth of field` 반복
4. **씬 끝/시작 설계**: 씬 1 끝의 "불빛"이 씬 2 시작의 "가게 외관"으로, 씬 2 끝의 "문 열림"이 씬 3의 "내부"로 이어짐

### Gemini 특성 고려

- 8초라 카메라 움직임은 한 가지만 지정하는 게 안정적 (pan OR zoom, 둘 다는 위험)
- 인물 얼굴을 정면으로 보여주면 일관성이 깨질 수 있으므로 최대한 뒷모습/손/실루엣 위주. 한국인 남성(dark coat)으로 통일
- "text on screen" 같은 지시는 잘 안 먹히므로 텍스트는 추후에 편집 단계에서 추가하기로 결정
