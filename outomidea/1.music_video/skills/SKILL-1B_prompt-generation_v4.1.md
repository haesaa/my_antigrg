# SKILL-1B: 콘티 → N컷 시퀀스 시트 프롬프트 생성

> **버전**: v4.1  
> **실행 환경**: Claude Sonnet 4.5+ / Gemini  
> **선행 조건**: SKILL-1A 산출물 **또는** 유저 직접 제공 프레임 지시서  
> **후속 연결**: 유저가 이미지 생성 → SKILL-2에 클립 전달  
> **필수 참조**: `REFERENCE-prompt-and-frame-guide.md` (Part 1~6)  
> **최종 갱신**: 2026-03-01

---

## 0. 이 스킬의 정체

**입력**: 콘티(conti-script.json) + 캐릭터 앵커 태그 + 스타일 프리셋 선택  
**출력**: N컷 개별 프롬프트 + 시퀀스 시트(3x3) 통합 프롬프트

### 0.1 독립 실행 모드

| 실행 경로 | 입력 | 비고 |
|----------|------|------|
| 1A 연결 | `work/S3-conti/conti-script.json` + `work/S1-analysis/character-anchor-tag.md` | prompt_seed 존재, 기계적 변환 |
| 독립 실행 | 유저 직접 제공 프레임 지시서 + 캐릭터시트 이미지 | prompt_seed 없음, 에이전트가 생성 |

독립 실행 시 추가 작업:
1. 캐릭터시트 이미지에서 앵커 태그 추출 (SKILL-1A §3.3 절차 동일)
2. 프레임 지시서를 conti-script.json 포맷으로 파싱 (REFERENCE Part 4.3 파싱 규칙 적용... → 아래 §1에서 상세)

---

## 1. 입력 검증 및 전처리 (B0-preflight)

**쓰기 권한**: `work/S4-prompts/`

### 1.1 필수 입력 체크

| 입력 | 필수 | 없을 때 |
|------|------|---------|
| conti-script.json (또는 프레임 지시서 텍스트) | ✅ | 중단 |
| 캐릭터 앵커 태그 (또는 캐릭터시트 이미지) | ✅ | 중단 — 캐릭터 일관성 보장 불가 |
| 스타일 프리셋 선택 | ✅ | 유저에게 질의 |
| character-profile.json | 권장 | 앵커 태그만으로 진행 |
| music-analysis.json | 선택 | 타임코드 없이 순서 기반 |

### 1.2 독립 실행 시: 프레임 지시서 → conti-script.json 변환

유저가 아래 형태로 프레임 지시서를 제공하면:

```markdown
## scene-01
- 화면: 카페 유리문 앞, 여자가 Help Wanted 스티커를 본다
- 감정: 설렘+불안
- 카메라: 미디엄롱, 아이레벨, 서서히 돌리인
- 동선: 문 앞에 서서 → 한발 앞으로
- 대사: (없음)
- 전환: 문 손잡이 매치컷 → 실내
- SFX: 거리 소음, 바람
```

**파싱 → conti-script.json 변환 → prompt_seed 자동 생성** 순서로 처리한다.

파싱 규칙:
1. `화면:` → `narrative.action` (동사 포함 문장) + `visual.background` (장소/오브젝트)
2. `감정:` → `narrative.emotion` — REFERENCE Part 1.1 표정 키워드에서 가장 가까운 태그 매핑
3. `카메라:` → 쉼표로 분리 → `visual.shot_size` / `visual.camera_angle` / `visual.camera_movement`
4. `동선:` → `character_direction.pose` (화살표를 시퀀스로 해석)
5. `대사:` → `audio_direction.dialogue` (없음/빈값 → null)
6. `전환:` → `transition.to_next` (효과명) + `transition.transition_detail` (상세)
7. `SFX:` → `audio_direction.sfx`
8. `타임코드:` → `timecode.start` / `timecode.end` (없으면 순서 기반 균등 배분)

파싱 후 **prompt_seed 자동 생성**:
- `subject_key` = `character_direction.pose` + `narrative.emotion`에 대응하는 REFERENCE Part 1.1 표정 키워드 + 시선 추론
- `setting_key` = `visual.background`에서 장소 유형 추출 → REFERENCE Part 2.1 핵심 오브젝트 자동 보강
- `camera_key` = `visual.shot_size` + `camera_angle` + `camera_movement` + 구도 추론 (REFERENCE Part 3.1)
- `lighting_key` = `narrative.emotion`에서 REFERENCE Part 2.2 감정별 조명 레시피 자동 매핑 + 시간대 힌트

### 1.3 독립 실행 시: 캐릭터시트 → 앵커 태그 추출

캐릭터시트 이미지가 제공되면:
1. 이미지에서 외형 추출 → character-profile.json 생성 (SKILL-1A §3.3 동일)
2. 1줄 앵커 태그 생성: `{인종/나이/성별}, {얼굴 특징}, {헤어}, {체형}`
3. `character-anchor-tag.md`로 저장

### 1.4 스타일 프리셋 확정

유저에게 REFERENCE Part 3.2 프리셋 목록을 제시하고 선택을 받는다:

```
사용 가능 스타일:
1. photorealistic-cinematic (한국 드라마 룩)
2. photorealistic-documentary (인디/다큐 룩)
3. photorealistic-fashion (패션 화보 룩)
4. korean-webtoon (네이버 웹툰 스타일)
5. japanese-anime-cinematic (극장판 애니)
6. noir-monochrome (흑백 느와르)
7. retro-film-grain (90s 필름 룩)
8. (custom — 유저 직접 키워드 입력)
```

확정된 프리셋은 **모든 씬에 동일 적용**. 프로젝트 중간 변경 금지.

### Gate-B0

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| conti-script.json (또는 변환 완료) | 유효 JSON, scenes ≥ 1 | 중단 |
| 캐릭터 앵커 태그 | 1줄 축약 존재 | 중단 |
| 스타일 프리셋 | 확정 | 유저 질의 |
| prompt_seed | 모든 씬에 4개 키 존재 | 독립실행 시 자동 생성 확인 |

---

## 2. 시퀀스 시트 분할 (B1-sheet-split)

### 2.1 시트 매핑

전체 N컷 → `ceil(N/9)` 장의 시퀀스 시트로 분할.

```
전체 18컷 → SEQ-01 (scene-01~09), SEQ-02 (scene-10~18)
전체 14컷 → SEQ-01 (scene-01~09), SEQ-02 (scene-10~14, 빈 5칸)
```

각 시트 내 9칸 배치:
```
[1-1] [1-2] [1-3]    ← 읽기 순서 = 시간 순서
[2-1] [2-2] [2-3]
[3-1] [3-2] [3-3]
```

### 2.2 빈 셀 처리

마지막 시트가 9컷 미만일 때:
- 빈 셀은 `grid_position`에 `"empty"` 표기
- 프롬프트 생성 대상에서 제외
- grid 통합 프롬프트에서 해당 위치는 `[empty panel]`로 명시

### 2.3 시트 경계 연속성 규칙

- SEQ-01 마지막 컷(3-3)의 감정/조명 → SEQ-02 첫 컷(1-1)과 자연스럽게 이어져야 함
- 급격한 시간대 변화(밤→낮)가 시트 경계에 오면 → 전환 효과(FADE, DISSOLVE) 힌트를 prompt에 반영
- 의상 변경이 시트 경계에서 발생하면 → 명시적 outfit_note 변경

---

## 3. prompt_seed → 7블록 변환 (B2-transform) — 핵심 엔진

**이 단계가 SKILL-1B의 본체. REFERENCE 파일을 참조하여 기계적으로 변환한다.**

### 3.1 변환 규칙 (7블록)

각 씬의 `prompt_seed` 4개 키를 7블록 프롬프트로 확장한다.

**[1. SUBJECT]**

```
= {character-anchor-tag.md 1줄 축약}, {prompt_seed.subject_key}
```

- 앵커 태그는 **절대 수정 금지** — 모든 씬에서 동일 문자열
- subject_key 뒤에 추가: REFERENCE Part 1.1에서 `narrative.emotion`에 매칭되는 표정 키워드
- 샷 사이즈별 기술 범위 조절 (§3.2 가중치 테이블 참조)

```
# 예시 (CU, emotion: melancholic)
young Korean man, late 20s, sharp jawline, dark narrow eyes, black tousled wet hair,
standing with weight on left leg gazing out window,
melancholic gaze, half-closed eyelids, unfocused distant stare
```

**[2. OUTFIT]**

```
= {character-profile.json → default_outfit 영문 변환} + {outfit_note 반영}
```

- outfit이 "default"면 character-profile.json에서 그대로
- outfit_note가 있으면 차이점만 반영 (예: "hoodie off one shoulder" → 해당 문구 추가)
- 의상 상태 키워드: wet, wrinkled, torn, dust-covered, blood-stained 등 (해당 시)

```
# 예시
open black zip-up hoodie slightly off one shoulder,
fitted light gray tank top, high-waisted medium-wash denim shorts,
white canvas sneakers, no accessories
```

**[3. SETTING]**

```
= {prompt_seed.setting_key} + REFERENCE Part 2.1 보강
```

보강 규칙:
1. setting_key에서 장소 유형 식별 → REFERENCE Part 2.1 테이블에서 해당 공간의 **핵심 오브젝트** 중 setting_key에 없는 것 2~3개 추가
2. 시간대 키워드 추가 — `narrative.emotion` 또는 `visual.lighting`에서 추론
3. 날씨/계절 키워드 추가 — conti에 명시되어 있으면 REFERENCE Part 2.1 날씨/계절에서 매칭

```
# 예시 (setting_key: "small neighborhood cafe exterior, glass door...")
small neighborhood cafe exterior, glass door with help wanted sticker,
wooden bench beside entrance, potted plants on window sill,
cobblestone sidewalk, Edison bulb pendant visible through window,
golden hour, quiet urban alley
```

**[4. LIGHTING]**

```
= {prompt_seed.lighting_key} + REFERENCE Part 2.2 보강
```

보강 규칙:
1. lighting_key의 광원 방향이 REFERENCE Part 2.2 조명 패턴 테이블에 있으면 → 그 행의 `감정 효과`가 `narrative.emotion`과 일치하는지 확인
2. 불일치하면 `mood_override`가 있는지 확인 → 없으면 경고 로그
3. 색온도가 명시되지 않았으면 → REFERENCE Part 2.2 감정별 조명 레시피에서 자동 매핑
4. 특수 조명 효과가 lighting_key에 포함되어 있으면 → REFERENCE Part 2.2 발생 조건 확인하여 부자연스러우면 제거

```
# 예시
golden hour backlighting from low sun, 3500K warm amber,
soft rim light on hair and shoulder edges,
soft blue fill from ambient sky, subtle anamorphic lens flare
```

**[5. CAMERA]**

```
= {prompt_seed.camera_key} (보강 최소화 — 이미 구체적)
```

- camera_key를 그대로 사용
- 단, 렌즈 화각 느낌이 빠져 있으면 → 샷 사이즈에서 추론하여 추가:
  - CU/ECU → 85mm portrait lens
  - MS/MCU → 50mm natural view  
  - LS/ELS → 24mm wide angle
- REFERENCE Part 3.1 DOF 테이블에서 `depth_of_field` 값을 프롬프트 키워드로 변환

```
# 예시
medium-long shot, eye-level angle, slow dolly in,
subject positioned at left third of frame, 50mm lens,
shallow depth of field f/2.8, soft background bokeh
```

**[6. STYLE]**

```
= {B0에서 확정한 스타일 프리셋 문자열} (전 씬 동일)
```

REFERENCE Part 3.2에서 선택된 프리셋의 프롬프트 문자열을 **그대로 복사**.

```
# 예시 (photorealistic-cinematic)
Cinematic K-drama aesthetic, soft clean lighting,
high-end DI color grading, 85mm lens, shallow DOF,
clear skin texture, subtle warm highlights
```

**[7. NEGATIVE]**

```
= {REFERENCE Part 3.2 공통 부정어}
+ {선택된 스타일의 전용 부정어}  
+ {장면 특화 부정어 자동 조합}
```

장면 특화 부정어 자동 판단:
- `visual.background`에 "interior" 키워드 → 실내 부정어 추가
- `visual.lighting`에 "night" → 야간 부정어 추가
- `narrative.emotion`이 슬픔 계열 → 슬픔 부정어 추가
- character 수 = 2 → 2인 부정어 추가
- `visual.background`에 rain/snow → 비/눈 부정어 추가

```
# 예시 (photorealistic + 실외 + 슬픔 아님)
worst quality, low quality, watermark, text, signature, logo,
deformed, distorted, extra fingers, mutated hands, blurry,
anime style, 3d render, cartoon, illustration, painting
```

### 3.2 샷 사이즈별 블록 가중치

SUBJECT vs SETTING의 프롬프트 분량(토큰) 비율:

| 샷 사이즈 | SUBJECT | OUTFIT | SETTING | LIGHTING | CAMERA |
|----------|---------|--------|---------|----------|--------|
| ECU | 45% | 0% | 5% | 30% | 20% |
| CU | 35% | 5% | 10% | 30% | 20% |
| MCU | 30% | 10% | 15% | 25% | 20% |
| MS | 25% | 15% | 20% | 20% | 20% |
| MLS | 20% | 15% | 25% | 20% | 20% |
| LS | 10% | 10% | 35% | 25% | 20% |
| ELS | 5% | 5% | 45% | 25% | 20% |

- ECU/CU: SUBJECT에서 얼굴 디테일 극대화, 의상/배경 최소화
- LS/ELS: SETTING에서 환경 디테일 극대화, 캐릭터는 실루엣 수준
- LIGHTING과 CAMERA는 샷에 관계없이 비교적 균등

### 3.3 장르 연출 반영

conti-script.json의 `mode` 필드 또는 유저 지정 장르에 따라:
- REFERENCE Part 4.1 장르별 연출 레시피에서 해당 장르의 **선호 조명**, **카메라 패턴**을 LIGHTING/CAMERA 블록 보강 시 우선 참조
- 예: 로맨스 모드 → LIGHTING에 `soft diffusion`, `back-lit golden hour` 우선 매핑

### 3.4 감정 전환점(Pivot) 처리

conti-script.json에서 연속된 두 씬의 `narrative.emotion`이 급변하면:
1. REFERENCE Part 4.2 감정 전환점 테이블에서 해당 전환 유형 매칭
2. 후속 씬의 LIGHTING 블록에 전환 프롬프트 힌트 반영
3. 예: 행복→슬픔 → 후속 씬에 `shift from warm sun to cold blue shadow` 키워드 추가

---

## 4. 프롬프트 출력 (B3-output)

### 4.1 파일 구조

```
work/S4-prompts/
├── SEQ-01/
│   ├── scene-01-prompt.md
│   ├── scene-02-prompt.md
│   ├── ...
│   ├── scene-09-prompt.md
│   └── grid-SEQ-01-prompt.md
├── SEQ-02/
│   ├── scene-10-prompt.md
│   ├── ...
│   └── grid-SEQ-02-prompt.md
├── prompt-index.json
└── TASK-REPORT.md
```

### 4.2 개별 씬 프롬프트 파일

파일명: `scene-{NN}-prompt.md`

```markdown
# Scene {NN} — Sheet {SEQ-XX} Grid [{row}-{col}]
## Emotion: {narrative.emotion}
## Story Beat: {narrative.story_beat}

### Positive Prompt

[SUBJECT]
{변환 결과}

[OUTFIT]
{변환 결과}

[SETTING]
{변환 결과}

[LIGHTING]
{변환 결과}

[CAMERA]
{변환 결과}

[STYLE]
{프리셋 문자열}

### Negative Prompt
{자동 조합 결과}

### Generation Parameters
- Aspect Ratio: 16:9 (1920x1080)
- CFG Scale: {REFERENCE Part 3.2 프리셋별 권장값}
- Steps: {프리셋별 권장값}
- Sampler: {프리셋별 권장값}

### Conti Reference (검증용)
- Scene ID: {scene_id}
- Shot: {shot_size}
- Camera: {camera_angle}, {camera_movement}
- Composition: {composition}
- Transition to next: {transition.to_next}
```

### 4.3 3x3 그리드 통합 프롬프트

파일명: `grid-{SEQ-XX}-prompt.md`

```markdown
# 3x3 Grid Storyboard — {SEQ-XX}

## Grid Layout Description
3x3 grid layout, cinematic storyboard sequence, 9 panels arranged left-to-right top-to-bottom:

[top-left: {scene-XX 한 줄 요약}]
[top-center: {XX+1 한 줄}]
[top-right: {XX+2 한 줄}]
[middle-left: {XX+3 한 줄}]
[middle-center: {XX+4 한 줄}]
[middle-right: {XX+5 한 줄}]
[bottom-left: {XX+6 한 줄}]
[bottom-center: {XX+7 한 줄}]
[bottom-right: {XX+8 한 줄}]

## Character Anchor (9컷 일관성)
{character-anchor-tag.md 1줄 축약}

## Style (전 셀 통일)
{스타일 프리셋 문자열}

## Negative
{공통 부정어}
inconsistent character appearance between panels,
different art styles between panels,
merged panels, overlapping frames
```

### 4.4 prompt-index.json

```json
{
  "$schema": "prompt-index-v4.1",
  "total_scenes": 0,
  "total_sheets": 0,
  "style_preset": "",
  "style_prompt": "",
  "character_anchor": "",
  "mode": "mv|drama|short",
  "sheets": [
    {
      "sheet_id": "SEQ-01",
      "scene_range": "scene-01 ~ scene-09",
      "scenes": [
        {
          "scene_id": "scene-01",
          "grid_position": "1-1",
          "emotion": "hopeful",
          "shot_size": "medium-long",
          "file": "SEQ-01/scene-01-prompt.md"
        }
      ],
      "empty_cells": [],
      "grid_file": "SEQ-01/grid-SEQ-01-prompt.md"
    }
  ]
}
```

---

## 5. 피드백 루프 (B4-feedback)

### 5.1 샘플 제출

**SEQ-01의 scene-01 프롬프트만 먼저 생성** → 유저에게 제출:

> "첫 장면 프롬프트 샘플입니다.  
> 이걸로 이미지 생성 테스트 후 피드백 주세요.  
> 확인 항목: 캐릭터 외형 일치, 분위기/톤, 상세도 수준"

### 5.2 피드백 반영

유저 피드백 유형별 처리:

| 피드백 | 수정 대상 | 영향 범위 |
|--------|----------|----------|
| "캐릭터가 안 닮음" | character-anchor-tag.md 앵커 태그 수정 | **전체** 씬 SUBJECT 블록 |
| "분위기가 너무 밝음/어두움" | LIGHTING 블록 색온도/강도 조정 | 해당 감정 계열 씬들 |
| "스타일이 안 맞음" | 스타일 프리셋 변경 | **전체** 씬 STYLE+NEGATIVE 블록 |
| "배경이 부정확" | setting_key 또는 SETTING 보강 수정 | 해당 씬만 |
| "카메라 앵글 변경" | camera_key 수정 | 해당 씬만 |
| "더 구체적으로/간결하게" | 블록별 토큰 비율 조정 | 전체 (가중치 테이블 조정) |

### 5.3 확정 후 일괄 생성

유저 승인 후:
1. 보정된 기준(앵커 태그, 스타일, 가중치)으로 **나머지 전체 씬 일괄 생성**
2. 시트별 grid 프롬프트 생성
3. prompt-index.json 생성
4. 시트 간 연속성 자동 검증 (§6)

---

## 6. 품질 검증 (B5-verify)

### 6.1 자동 검증 항목

| 검증 | 기준 | 실패 시 |
|------|------|---------|
| 캐릭터 앵커 일관성 | 모든 SUBJECT 블록에 동일 앵커 태그 문자열 | 해당 씬 수정 |
| 7블록 완전성 | 모든 프롬프트에 7블록 전부 존재 | 누락 블록 추가 |
| 스타일 일관성 | 모든 STYLE 블록이 동일 프리셋 | 해당 씬 수정 |
| 부정 프롬프트 존재 | 모든 파일에 NEGATIVE 존재 | 추가 |
| 의상 연속성 | outfit_note 변경이 스토리상 정당한 시점에서만 | 경고 로그 |
| 조명 연속성 | 시트 경계에서 급변 없음 (의도적 전환 제외) | 경고 로그 |
| prompt_seed 매칭 | 콘티의 seed와 프롬프트 불일치 0건 | 해당 씬 수정 |
| prompt-index.json | 유효 JSON, 전 씬 포함 | 재생성 |
| 감정 전환점 | pivot 씬에 전환 힌트 키워드 반영 여부 | 해당 씬 보강 |

### 6.2 수동 확인 요청

자동 검증 통과 후 유저에게:

> "전체 {N}씬 × {S}시트 프롬프트 생성 완료.  
> prompt-index.json과 첫/마지막 시트 grid 프롬프트를 확인해주세요."

---

## 7. 산출물 요약

| 파일 | 수량 | 용도 |
|------|------|------|
| `scene-{NN}-prompt.md` | N개 | 개별 씬 이미지 생성용 |
| `grid-{SEQ-XX}-prompt.md` | S개 | 3x3 시퀀스 시트 생성용 |
| `prompt-index.json` | 1개 | 전체 인덱스, SKILL-2 핸드오프 |
| `TASK-REPORT.md` | 1개 | 작업 기록 |

---

## 8. SKILL-2 핸드오프

SKILL-2가 이 스킬의 산출물에서 읽는 것:

| 파일 | 필드 | 용도 |
|------|------|------|
| prompt-index.json | `sheets[].scenes[].emotion` | 클립-장면 무드 매칭 |
| prompt-index.json | `sheets[].scenes[].scene_id` | 클립 매칭 키 |
| prompt-index.json | `sheets[].scenes[].shot_size` | 클립 프레이밍 검증 |
| prompt-index.json | `total_scenes`, `total_sheets` | 커버리지 분모 |

---

## 9. 실패 처리

| 실패 지점 | 제공 가능 산출물 | 조치 |
|----------|----------------|------|
| B0 실패 (입력 부족) | 없음 | 필요 입력 안내 |
| B1 실패 (시트 분할) | conti 파싱 결과 | 수동 분할 요청 |
| B2 실패 (변환 오류) | 파싱된 conti + 앵커 태그 | 수동 프롬프트 요청 |
| B3 실패 (출력 오류) | 변환된 프롬프트 텍스트 | 파일 구조 수동 정리 |
| B4 피드백 무한루프 | 마지막 버전 프롬프트 | 유저에게 확정 요청 |

모든 실패 시 `work/S4-prompts/` 보존. 유저에게 빈 손 없음.

---

## 부록: REFERENCE 파일 참조 매핑

| 1B 단계 | REFERENCE 파트 | 참조 목적 |
|---------|---------------|----------|
| B0 (프레임 지시서 파싱) | Part 1.1 표정 키워드 | emotion → 표정 태그 매핑 |
| B2 [SUBJECT] | Part 1.1 표정 + Part 1.2 포즈 | 감정에 맞는 표정/포즈 선택 |
| B2 [SETTING] | Part 2.1 공간 + 소품 + 시간대 + 날씨 | 배경 키워드 보강 |
| B2 [LIGHTING] | Part 2.2 조명 패턴 + 색온도 + 감정 레시피 | 조명 키워드 보강 |
| B2 [CAMERA] | Part 3.1 샷/앵글/구도/DOF/렌즈 | 카메라 키워드 보강, 렌즈 추론 |
| B2 [STYLE] | Part 3.2 스타일 프리셋 | 프리셋 문자열 복사 |
| B2 [NEGATIVE] | Part 3.2 공통+화풍별+장면특화 부정어 | 부정 프롬프트 자동 조합 |
| B2 장르 반영 | Part 4.1 장르별 연출 레시피 | 장르 특화 조명/카메라 우선 매핑 |
| B2 감정 전환점 | Part 4.2 Pivot Point 연출 | 전환 힌트 키워드 삽입 |
| B3 grid 프롬프트 | Part 3.2 부정어 | 시트 일관성 부정어 추가 |
| B0 SFX 파싱 | Part 5 SFX 키워드 | SFX 텍스트 → 표준 키워드 매핑 |
