# GUIDE: 스토리→시각 연출 설계 규칙

> **위치**: SKILL-1A 실행 시 S2(스토리), S3(콘티) 단계에서 필수 참조  
> **역할**: 서사 설계 시점에서 시각 연출을 동시에 결정하는 규칙 사전  
> **원칙**: 프롬프트(1B)에서 뒤늦게 시각 요소를 붙이지 않는다. 스토리 단계에서 감정→환경→카메라가 한 덩어리로 설계된다.

---

## 0. 이 가이드의 작동 원리

```
[S2 스토리 설계]
  감정 아크 → §1 감정-환경 동기화 테이블 참조 → 각 ACT의 환경/조명 톤 확정
  캐릭터 설정 → §2 심리-행동 번역 테이블 참조 → 표정/포즈/소품 방향 확정
  서사 구조 → §3 서사 기법→컷 설계 테이블 참조 → 카메라 워크/전환 방향 확정

[S3 콘티 생성]
  각 장면의 visual/character_direction/prompt_seed 필드를
  위에서 확정한 방향으로 채운다.
  에이전트가 "적당히" 시각 요소를 붙이는 것을 금지한다.
  반드시 이 가이드의 테이블에서 선택한다.
```

---

## 1. 감정→환경 동기화 테이블 (Pathetic Fallacy 규칙)

> **적용 시점**: S2 각 ACT의 `감정` 태그를 확정한 직후, 같은 ACT의 `핵심 이미지`를 작성할 때.
> **원칙**: 감정이 먼저 결정되고, 환경이 감정을 따른다. 역순 금지.

### 1.1 감정→시간대·날씨·조명 강제 매핑

| 감정 태그 | 시간대 | 날씨/계절 | 조명 방향 | 색온도 | 특수효과 |
|----------|--------|----------|----------|--------|---------|
| hopeful | golden hour / morning | 맑음, 봄 | back-lit | 3500K warm amber | lens flare, god rays |
| melancholic | blue hour / night | 비, 안개 | side-lit | 7500K cool blue | volumetric haze |
| tender | golden hour / dusk | 맑음, 가을 초 | soft front + rim | 3000K amber | bokeh, dappled light |
| nostalgic | afternoon / golden hour | 흐림, 가을 | back-lit diffused | 4000K warm muted | film grain, haze |
| angry | night / midnight | 폭풍, 바람 | under-lit / split | 3000K fiery + 7000K cold | harsh contrast, flicker |
| tense | night / blue hour | 흐림, 안개 | chiaroscuro | 5000K neutral cold | deep shadows |
| euphoric | golden hour / morning | 맑음, 벚꽃/눈 | back-lit + rim | 3500K golden | lens flare, bloom |
| lonely | blue hour / midnight | 비, 겨울 | single side-lit | 8000K deep blue | silhouette, fog |
| bittersweet | dusk / blue hour | 석양+구름 | mixed side+back | warm amber + cool blue 혼합 | 없음 — 자연광만 |
| fearful | midnight / dawn | 안개, 어둠 | under-lit | 6000K cold pale | flicker, deep void |
| peaceful | morning / afternoon | 맑음, 녹음 | dappled / loop | 3500K~5000K neutral warm | komorebi, soft fill |
| rebellious | night | 네온, 도시 | rim + neon glow | neon magenta/cyan | lens flare, glow |
| cathartic | dawn / golden hour | 비 갠 후 | back-lit | 5500K → 3500K 변화 | god rays, wet reflections |

### 1.2 적용 규칙

1. S2에서 ACT별 `감정` 태그를 먼저 확정한다
2. 위 테이블에서 해당 감정의 행을 찾는다
3. 해당 행의 시간대/날씨/조명을 **그 ACT의 모든 장면에 기본값으로 적용**한다
4. 장면 내에서 감정이 전환(pivot)되면 → §4 전환점 규칙 적용
5. **테이블에 없는 감정 태그가 나오면** → 가장 가까운 2개 감정의 중간값을 사용하고, 어떤 2개를 혼합했는지 `color_palette` 필드에 명시한다

### 1.3 금지사항

- 감정이 `melancholic`인데 조명이 `warm golden`인 장면을 만들지 마라 (의도적 아이러니가 아닌 한)
- 의도적 불일치(dramatic irony)를 사용하려면 → `mood_override` 필드에 이유를 명시해야 한다
- "적당히 분위기 있게"라는 지시는 금지. 반드시 테이블의 구체적 값을 선택한다

---

## 2. 캐릭터 심리→행동 번역 테이블

> **적용 시점**: S2에서 캐릭터 설정을 읽은 후, S3에서 각 장면의 `character_direction`을 채울 때.
> **원칙**: 캐릭터의 감정 상태가 표정·포즈·소품을 결정한다. 에이전트가 "예쁜 포즈"를 임의 배정하는 것을 금지한다.

### 2.1 애착 유형→장면별 행동 패턴

캐릭터에 애착 유형이 설정되어 있으면 (character-profile.json 또는 유저 입력), 아래 규칙을 S3 character_direction에 적용한다.

**가까워지는 장면 (호감 상승, 고백, 재회)**:

| 애착 유형 | 표정 | 포즈 | 시선 |
|----------|------|------|------|
| 안정형 | warmly smiling / content serene | casual weight-shifted, open posture | 상대를 편하게 바라봄 |
| 불안형 | shy bashful smile / anxious nervous | 앞으로 기울어짐, 손 만지작 | 상대를 확인하듯 자주 봄 |
| 회피형 | neutral / wistful look | arms crossed 또는 back turned | 상대를 보다가 시선 회피 |
| 혼란형 | conflicted torn / bittersweet smile | reaching out → pulling back | 시선 흔들림, 접근-회피 |

**멀어지는 장면 (이별, 갈등, 배신)**:

| 애착 유형 | 표정 | 포즈 | 시선 |
|----------|------|------|------|
| 안정형 | steely determined / dejected | 서서 정면 대화 시도 | 상대 눈을 봄 |
| 불안형 | tearful / desperate pleading | reaching out, collapsing | 상대에게 매달리는 시선 |
| 회피형 | empty vacant stare / cold | standing back turned, walking away | 시선 차단, 먼 곳 |
| 혼란형 | heartbroken → fierce angry (급변) | 접근→후퇴→접근 반복 | 불안정하게 흔들림 |

### 2.2 갈등 장면→카메라 워크 강제 매핑

캐릭터의 갈등 처리 방식에 따라 카메라 워크가 결정된다.

| 갈등 스타일 | 카메라 앵글 | 샷 사이즈 | 카메라 무브먼트 |
|-----------|-----------|----------|-------------|
| 경쟁 (정면 대립) | low-angle (양쪽 번갈아) | CU~MCU | static 또는 slow dolly in |
| 협력 (대화 해결) | eye-level, OTS | MS~MCU | static |
| 회피 (감정 차단) | high-angle (위에서 내려다봄) | MLS~LS | slow dolly out |
| 수용 (양보/체념) | high-angle → eye-level 복귀 | MS | static → tilt down |
| 폭발 (억눌린 감정 터짐) | dutch angle → eye-level 복귀 | ECU→CU→MS (점점 넓어짐) | handheld shake → static |

### 2.3 사랑의 언어→소품/행동 강제 삽입

캐릭터의 사랑의 언어(Give 유형)가 설정되어 있으면, **호감 장면에서 해당 유형의 소품/행동이 반드시 1개 이상 등장**해야 한다.

| Give 유형 | 장면에 삽입할 것 | conti 위치 | 프롬프트 효과 |
|----------|---------------|-----------|-------------|
| 인정의 말 | 대사 존재 + 입 모양 클로즈업 | audio_direction.dialogue + visual.shot_size: CU | 입/눈 디테일 |
| 봉사 | 행동 소품 (외투, 약, 음식, 문 잡아줌) | character_direction.pose에 행동 포함 + visual.background에 소품 | 전경 소품 |
| 선물 | 오브젝트 (꽃, 상자, 물건) | visual.background 전경 + character_direction에 건네는 동작 | macro 소품 |
| 함께하는 시간 | 나란히 있는 구도, 빈 공간 | visual.composition: 두 인물 병렬, negative space | 넓은 화면 |
| 신체 접촉 | 손/어깨/팔 접촉 | character_direction에 접촉 동작 + visual.shot_size: CU/MCU | 접촉부 클로즈업 |

### 2.4 적용 규칙

1. S1에서 캐릭터 프로필을 분석할 때, 유저 입력에 애착 유형/갈등 스타일/사랑의 언어가 있으면 → character-profile.json에 기록한다
2. **없으면 추론하지 않는다** — 유저가 명시하지 않은 심리 유형을 에이전트가 임의 부여하는 것을 금지한다
3. 있으면 S3의 모든 해당 장면에서 §2 테이블을 의무적으로 참조한다
4. 테이블의 표정/포즈 키워드는 REFERENCE Part 1.1/1.2의 영문 키워드를 정확히 사용한다

---

## 3. 서사 기법→컷 설계 테이블

> **적용 시점**: S2에서 서사 구조를 짤 때, 각 ACT의 핵심 서사 기법을 확정하고, S3에서 해당 기법을 컷 레벨 연출로 번역할 때.
> **원칙**: 서사 기법을 "문학적 장식"이 아니라 "카메라가 무엇을 찍는가"로 번역한다.

### 3.1 기법→시각 연출 변환

| 서사 기법 | 카메라/구도 번역 | 조명 번역 | 편집 번역 | S3 필드 반영 |
|----------|---------------|----------|----------|-------------|
| Pathetic Fallacy (환경=감정) | ELS/LS로 환경 비중 확대 | §1 테이블 강제 적용 | 환경→인물 순서 (환경 컷 먼저) | visual.background 최우선 |
| Show Don't Tell (행동=감정) | CU/MCU 손·입·눈 클로즈업 | 행동을 비추는 soft key light | 행동 컷 후 반응 컷 | character_direction.pose에 행동 |
| Strategic Silence (침묵=감정) | 정적 카메라, 긴 호흡 | 변화 없음, 정적 | 컷 길이 길게 (6초+) | audio_direction: sfx만, dialogue: null |
| Push-Pull (밀당) | 거리 변화 (dolly in→dolly out) | warm↔cool 교차 | 컷 길이 짧아졌다 길어졌다 | 연속 2컷의 lighting_key 대조 |
| Emotional Whiplash (낙차) | 급격한 샷 사이즈 변화 (ELS→ECU) | 따뜻→차가움 급전환 | smash cut | transition.to_next: smash_cut |
| Register Contrast (낙차) | 같은 인물의 두 장면을 대조 구도 | 공식=cool neutral / 비공식=warm amber | match cut 또는 dissolve | 연속 2컷의 전체 톤 대조 |
| Surrogate Confession (대리고백) | 소품 또는 행동 macro CU | 소품에 warm spot light | 소품 컷 → 인물 반응 컷 | visual.background에 소품, shot_size: ECU |
| In Medias Res (사건 한가운데) | 첫 컷부터 action — LS/MS, 동적 | harsh/dramatic | 첫 컷은 설명 없이 시작 | 첫 씬의 narrative.action이 사건 중간 |
| Hard Cut (단절) | 마지막 컷을 설명 없이 끊음 | 조명 변화 없이 암전 | cut to black | transition.to_next: fade_out |
| Cliffhanger (갈고리) | 마지막 컷 = 결정적 순간 직전에서 끊음 | 긴장 최고조 유지 | 마지막 컷 이후 다음 시트 첫 컷이 해소 | 시트 마지막 scene의 transition: cut (해소 없이) |

### 3.2 적용 규칙

1. S2의 각 ACT에서 **핵심 서사 기법 1~2개를 명시적으로 선택**한다
2. S3에서 해당 ACT의 장면을 생성할 때, 위 테이블의 시각 연출을 의무적으로 적용한다
3. **서사 기법을 선택하지 않고 "적당히" 콘티를 짜는 것을 금지한다**
4. story.md에 기법 선택을 기록한다:

```markdown
### ACT 2: 전개
- 서사 기법: [Push-Pull] + [Strategic Silence]
- 시각 연출 근거: 밀당 구간이므로 거리 변화(dolly in/out) + 침묵 장면의 정적 카메라
```

---

## 4. 감정 전환점(Pivot) 연출 규칙

> **적용 시점**: S3에서 연속된 두 장면의 `narrative.emotion`이 다른 계열로 바뀔 때.
> **원칙**: 감정 전환은 "갑자기" 일어나지 않는다. 조명·카메라·편집이 전환을 예고하거나 강조한다.

### 4.1 전환 유형별 시각 변화

| 전환 유형 | 조명 변화 | 카메라 변화 | 편집 (전환효과) | prompt_seed 힌트 |
|----------|----------|-----------|------------|--------------|
| 행복→슬픔 | warm gold → cool blue (점진적) | 샷 넓어짐 (CU→LS) | dissolve (느린) | lighting_key에 color shift 명시 |
| 평화→긴장 | soft diffused → harsh contrast | static → handheld | J-cut (긴장 SFX 먼저) | sfx 변화가 lighting보다 선행 |
| 혼란→깨달음 | haze/blur → sharp clear | out-of-focus → rack focus | slow zoom-in | lighting_key: clarity, sharp |
| 분노→체념 | red/harsh → desaturated | CU → ELS (pull back) | slow dissolve | camera_key에 pull-back 명시 |
| 현재→회상 | 현재 색감 → golden/sepia + grain | sharp → soft focus | white flash → dissolve | mood_override: nostalgia |
| 일상→비일상 | neutral → dramatic (어느 쪽이든) | eye-level → dutch angle | smash cut | 전환 직전 컷에 일상 소품 강조 |

### 4.2 적용 규칙

1. S3에서 장면 간 emotion 태그가 **다른 계열**로 바뀌면 → 반드시 위 테이블에서 해당 전환 유형을 찾는다
2. **전환 컷 = 이전 감정의 마지막 컷** — 이 컷의 prompt_seed에 전환 힌트를 삽입한다
3. 같은 계열 내 강도 변화 (hopeful→euphoric)는 전환이 아님 → 테이블 미적용, 자연스러운 강화만
4. 시트 경계에서 전환이 일어나면 → transition 효과를 강화하고, 다음 시트 첫 컷에 새 감정의 환경을 완전히 확립한다

---

## 5. 장면 리듬 설계 규칙

> **적용 시점**: S3에서 시퀀스 시트 내 9컷의 샷 사이즈 배치를 결정할 때.
> **원칙**: 9컷이 전부 같은 샷 사이즈이면 안 된다. 시각적 리듬이 감정 리듬을 만든다.

### 5.1 샷 사이즈 리듬 패턴

| 시트 내 위치 | 서사 기능 | 권장 샷 사이즈 |
|------------|----------|-------------|
| 1-1 (시작) | 상황 제시 | LS / MLS (공간 확립) |
| 1-2 | 인물 도입 | MS / MCU |
| 1-3 | 행동/반응 | MS / CU |
| 2-1 | 전개/긴장 | MCU / CU |
| 2-2 | 핵심 순간 | CU / ECU (감정 최대) |
| 2-3 | 반응/여파 | MS / MCU |
| 3-1 | 전환 준비 | MLS / LS (거리 다시 벌림) |
| 3-2 | 전환 | MS (중립) |
| 3-3 (끝) | 여운/갈고리 | CU (감정) 또는 ELS (고립) |

### 5.2 금지 패턴

- 9컷 연속 CU 금지 — 최소 3종 이상의 샷 사이즈를 사용한다
- 9컷 연속 static 금지 — 최소 1~2컷은 카메라 무브먼트가 있어야 한다
- 첫 컷과 마지막 컷이 같은 샷 사이즈+같은 앵글이면 안 된다 (변화 없는 시트)

### 5.3 예외

- 의도적 반복 (시간 흐름 표현, 루틴 강조)일 때는 금지 패턴을 깰 수 있다
- 이 경우 story.md에 "의도적 반복: [이유]"를 명시해야 한다

---

## 6. S2 story.md 확장 필드

이 가이드를 적용하면 S2 story.md의 각 ACT에 아래 필드가 추가된다.

```markdown
### ACT {N}: {제목}
- 음악 구간 / 씬 범위: {구간명}
- 에너지: {값}/10
- 감정: {무드 태그}
- 서사: {이 구간에서 일어나는 이야기}
- 핵심 이미지: {대표 장면 묘사}

## ▼ 시각 연출 설계 (이 가이드 적용 결과)
- 환경 톤: {§1 테이블에서 선택한 시간대/날씨/조명}
- 서사 기법: {§3 테이블에서 선택한 기법 1~2개}
- 시각 연출: {§3 테이블에서 해당 기법의 카메라/조명/편집 번역}
- 캐릭터 행동: {§2 테이블 해당 시 — 애착유형/갈등스타일 기반}
- 전환점: {§4 테이블 해당 시 — 이 ACT에서 다음 ACT로의 전환 유형}
```

---

## 7. 검증 체크리스트 (Gate-S2, Gate-S3에 추가)

### S2 Gate 추가 항목

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| 감정-환경 일치 | 모든 ACT의 환경 톤이 §1 테이블과 일치 | 수정 |
| 서사 기법 선택 | 모든 ACT에 기법 1~2개 명시 | 추가 |
| 시각 연출 근거 | 서사 기법→시각 연출 번역이 §3과 일치 | 수정 |
| mood_override 근거 | 사용 시 이유 명시 | 추가 |

### S3 Gate 추가 항목

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| 캐릭터 행동 근거 | 애착유형/갈등스타일 설정 있으면 §2 테이블 적용됨 | 수정 |
| 소품 삽입 | 사랑의 언어 설정 있는 호감 장면에 해당 소품 존재 | 추가 |
| 전환점 처리 | 감정 계열 변경 씬에 §4 전환 연출 적용됨 | 수정 |
| 샷 리듬 | 시트 내 3종+ 샷 사이즈, 금지 패턴 미위반 | 수정 |
| lighting_key 근거 | §1 테이블에서 도출, 임의 값 금지 | 수정 |
