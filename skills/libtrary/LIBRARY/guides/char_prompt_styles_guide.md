# NijiJourney & NanoBanana2 캐릭터 프롬프트 가이드

이 문서는 AI 이미지(특히 니지저니 및 나노바나나 등) 캐릭터 생성 시 활용되는 프롬프트 어휘 집합(백과사전) 및 포맷 규정입니다.
`char_prompts_maker` 스킬은 1_full_prompt의 텍스트 외형/성격 요소를 아래의 키워드 체계에 맞춰 영어 태그 위주로 치환하여 프롬프트를 조립해야 합니다.

## 1. 프롬프트 기본 포맷

1. **Niji Journey (니지저니)**
   - 문법: `[주제/캐릭터 기본 외형], [복장/포즈], [조명/분위기/배경], [아트 스타일/작화 태그] --ar 16:9 --niji 6 --style raw` (예시)
   - 주요 태그: `anime style, masterpiece, best quality, ultra-detailed`
2. **NanoBanana2 (SD 기반)**
   - 문법: `(masterpiece, best quality:1.2), 1girl, [외형 쉼표 나열], [복장 나열], [포즈 나열], [배경 나열]`
   - 부정 프롬프트: `(worst quality, low quality:1.4), deformed, bad anatomy, bad hands, missing fingers`

## 2. 참조 키워드 백과사전

### 2.1 사진 및 앵글 (Photography Style)

- **High Angle Shot / Low Angle Shot**: 인물의 권위(위축됨 vs 지배적) 조절
- **Close-up**: 얼굴 표정 및 눈빛 강조 (`intense eyes` 등)
- **Full Body Shot / Upper Body Shot / Knee Shot**

### 2.2 조명 스타일 (Lighting Style)

- **Cinematic Lighting / Studio Lighting**
- **Low-Key Lighting**: 다크판타지, 스릴러 장르 캐릭터에 적합 (드라마틱하고 미스터리한 음영)
- **Backlighting**: 실루엣 강조

### 2.3 포즈 및 신체 태도 (Pose)

- 방어적/권위적: `Arms Crossed`, `Standing Straight`
- 전투/아웃사이더: `Hands in Pockets`, `Leaning Against a Wall`
- 전투(무기 소지): `holding sword`, `dynamic pose`, `fighting stance`

### 2.4 헤어 스타일 (Hair Styles)

- 여성: `long straight hair`, `layered cut`, `pixie cut`, `bob cut`, `ponytail`, `messy hair`
- 남성: `two block cut`, `slicked back hair`, `messy hair`, `long hair`, `short hair`

### 2.5 패션 스타일 (Fashion Styles)

- **Hunter / Dark Fantasy**: `tactical gear`, `combat boots`, `leather jacket`, `trench coat`, `armor parts`
- **Modern / Casual**: `casual wear`, `street style`, `business formal` (정장)

### 2.6 외형 분위기 및 표정 (Appearance & Emotion)

- 외모 분위기: `mysterious`, `rugged(거친/흉터)`, `charismatic`, `elegant`, `cool`
- 눈빛/표정: `sharp eyes`, `glowing eyes`, `smirk`, `emotionless`, `angry`, `intense gaze`, `bags under eyes`

## 3. 프롬프트 생성 시 주의사항

- **반드시 영어 태그** 단어의 나열 (단어와 단어 사이 쉼표 `,` 로 연결) 구조를 띄어야 합니다.
- 스토리 내러티브가 아닌 **지각 가능한(Visualizable) 요소** 위주로만 번역.
  - O: `1man, tall, black coat, messy black hair, glowing red eyes, holding a sword, low-key lighting, dark fantasy`
  - X: `a man who is an S-class hunter feeling guilty about the past` (추상적 과거/성격X)

**이 외에 필요한 요소들이 있으면 검색해서 붙여오고, 알맞은 섹션에 append한다.* must 신뢰할 수 있는 정보여야 한다**
