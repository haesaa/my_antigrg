# SKILL-1: Story → Conti → Sequence Sheet Prompt Generator

> **버전**: v4.0  
> **실행 환경**: Claude Sonnet 4.5+ / Gemini  
> **선행 조건**: 없음 (독립 실행)  
> **후속 연결**: SKILL-2 (편집/배치)에 산출물 전달  
> **참조 문서**:  
>
> - `REFERENCE-prompt-and-frame-guide.md` — 프롬프트 키워드 사전 (S4 필수)  
> - `SKILL-1A_story-conti-GUIDE-story-visual-design.md` — 스토리→시각 연출 설계 규칙 (S2·S3 필수)  
> **최종 갱신**: 2026-03-01

---

## 0. 이 스킬의 정체

### 0.1 스킬 분리 구조

```
SKILL-1A: 입력 분석 + 스토리 + 콘티 (상세 프레임 지시서)
SKILL-1B: 콘티 → N컷 시퀀스 시트 프롬프트 생성
```

- 1A 산출물이 1B 입력
- 각각 독립 실행 가능 (1A만 돌려서 콘티만 뽑을 수 있음)
- 1B만 단독 실행 시: 유저가 프레임 지시서를 직접 제공

### 0.2 지원 모드

| 모드 | 입력 | 특징 |
|------|------|------|
| 뮤비 | 음악 메타 + 캐릭터시트 | 타임코드 필수, 음악 구간=서사 구조 |
| 드라마 | 시놉시스 + 캐릭터시트 | 대사 필수, 에피소드/씬 단위 |
| 단편 | 컨셉 텍스트 + 캐릭터시트(선택) | 최소 입력, 에이전트 재량 최대 |

### 0.3 핵심 변경점 (v3 → v4)

- 9컷 고정 → **N컷 가변, 시퀀스 시트(3x3) 단위**
- S3 콘티에 `prompt_seed` 필드 추가 → S4 변환이 결정론적
- 프레임 지시서 입력 규격 표준화 (`REFERENCE` 문서 분리)
- 뮤비/드라마/단편 3모드 지원

---

## 1. 전역 규칙

### 1.1 파일 관리

- 쓰기 격리: 각 단계는 지정 폴더에만 파일 생성
- 원본 보존: `input/` 폴더 READ-ONLY

### 1.2 산출물 규격

- 텍스트: UTF-8, JSON: 4-space indent, BOM 없음
- 마크다운: GitHub Flavored Markdown
- 파일명: 영문+숫자+하이픈만 (한글 금지)

### 1.3 로깅

- 매 단계 시작/완료 → `PIPELINE-LOG.md` 기록
- 실패 시 사유+재시도 횟수, 누적 토큰 기록

### 1.4 중간 확인 포인트

- S2(스토리 완성) 후 → 유저 승인 대기
- S3(콘티 완성) 후 → 유저 승인 대기 **(v4 추가)**
- S4(프롬프트) → 첫 시퀀스 시트 샘플 승인 후 나머지 생성

---

## 2. 프로젝트 초기화 (S0-preflight)

**쓰기 권한**: `project-{timestamp}/` 루트

```
project-{YYYYMMDD-HHmmss}/
├── input/                  ← 유저 원본 복사
├── work/
│   ├── S1-analysis/
│   ├── S2-story/
│   ├── S3-conti/
│   └── S4-prompts/
│       ├── SEQ-01/         ← 시퀀스 시트 단위 폴더
│       ├── SEQ-02/
│       └── ...
├── output/
├── logs/
└── PIPELINE-LOG.md
```

### Gate-S0

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| input/ 내 파일 ≥ 1개 | 존재 | 중단 |
| 디렉토리 구조 일치 | 위 트리 | 재생성 |
| 모드 판별 | 뮤비/드라마/단편 중 1개 확정 | 유저에게 질의 |

---

# SKILL-1A: 입력 분석 → 스토리 → 콘티

---

## 3. 입력 분석 (S1-analyze)

**쓰기 권한**: `work/S1-analysis/` 만

### 3.1 음악 분석 (뮤비 모드)

입력이 음악 메타인 경우:

1. 메타데이터 추출: 곡 제목, 아티스트, 장르, BPM, 키/스케일, 총 길이(초)
2. 구간 분리: intro / verse1 / pre-chorus / chorus1 / verse2 / chorus2 / bridge / outro (최소)
3. 각 구간: 시작~끝 타임코드, 에너지(1~10), 무드 태그
4. 감정 곡선 도출: 클라이맥스 지점 + 감정 전환점(pivot point) 표시

무드 사전 (공식 24태그 — 이 목록 외 태그 사용 금지):

```
[positive]
joyful, excited, romantic, hopeful, peaceful, dreamy, playful, euphoric, triumphant
[neutral]
nostalgic, mysterious, serious, bittersweet, longing, whimsical
[negative]
melancholic, anxious, angry, lonely, fearful, tense, cold, aggressive, cathartic
```

> `peaceful` / `angry` / `lonely` / `fearful` — GUIDE §1.1 감정-환경 매핑에서 공식 통합 (v4.1)

### 3.2 시놉시스 분석 (드라마/단편 모드)

1. 시놉시스 텍스트에서 장면 구분, 캐릭터 행동, 대사 추출
2. 서사 아크 자동 도출: 발단→전개→위기→절정→결말
3. 감정 곡선 도출 (에너지 값은 추론 기반)

### 3.3 캐릭터시트 분석 (모든 모드 공통)

캐릭터시트 이미지 제공 시:

1. **외형 추출** — 아래 JSON 전 항목을 빠짐없이 텍스트화:

```json
{
  "character_id": "char_01",
  "gender": "",
  "apparent_age": "",
  "ethnicity_appearance": "",
  "body": { "height_impression": "", "build": "", "skin_tone": "" },
  "face": {
    "shape": "",
    "eyes": { "shape": "", "color": "", "brow_style": "" },
    "nose": "", "lips": "",
    "distinctive_features": []
  },
  "hair": { "color": "", "length": "", "style": "", "texture": "" },
  "default_outfit": {
    "top": "", "bottom": "", "outerwear": "",
    "shoes": "", "accessories": []
  },
  "available_expressions": [],
  "available_angles": ["front", "back", "3/4-left", "3/4-right", "profile-left", "profile-right"],
  "raw_description": ""
}
```

1. **캐릭터 앵커 태그** 생성 (프로젝트 전체에서 고정 삽입):
   - 1줄 축약: `young Korean man, late 20s, sharp jawline, dark narrow eyes, black tousled wet hair, black suit with gray tie`
   - 표정별 변형 태그 (available_expressions에서 도출)

**표정시트(expression sheet)가 별도 제공된 경우**:

- 그리드 내 각 표정을 개별 식별하여 `expression_tags[]`에 매핑
- 예: `[neutral, gentle-smile, surprised, angry, sad-downcast, pensive, tearful, smirk, laughing, anxious, ...]`

### 3.4 산출물

- `work/S1-analysis/music-analysis.json` (뮤비 모드) 또는 `synopsis-analysis.json` (드라마/단편)
- `work/S1-analysis/character-profile.json` (캐릭터시트 있을 때)
- `work/S1-analysis/character-anchor-tag.md` — 앵커 태그 (전 프롬프트에 삽입용)
- `work/S1-analysis/TASK-REPORT.md`

### Gate-S1

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| 분석 JSON 존재 | 크기 > 0 | 재분석 |
| 구간 수 (뮤비) | ≥ 3개 | 재분석 |
| 에너지 값 범위 | 1~10 | 보정 |
| character-profile.json (있을 때) | 필수 필드 누락 없음 | 재추출 |
| 앵커 태그 | 1줄 축약 존재 | 재생성 |

---

## 4. 스토리 생성 (S2-story)

**쓰기 권한**: `work/S2-story/` 만

> 🗂️ **이 단계 필수 참조**: `SKILL-1A_story-conti-GUIDE-story-visual-design.md`  
>
> - §1 감정→환경 동기화 테이블 — 각 ACT 감정 확정 직후 적용  
> - §2 캐릭터 심리→행동 번역 — 캐릭터 설정 있을 때 적용  
> - §3 서사 기법→컷 설계 — ACT별 핵심 기법 선택 후 적용  
> **에이전트는 위 테이블 없이 조명·포즈·카메라를 임의 결정하는 것을 금지한다.**

### 4.1 스토리 원칙

1. **뮤비**: 음악 구조 = 서사 구조. 에너지 곡선과 감정 아크 동기화
2. **드라마**: 에피소드 구조. 씬 전환 = 감정 전환점
3. **단편**: 3막 구조 최소 보장. 컨셉에서 서사 자동 확장
4. 캐릭터시트가 있으면 해당 캐릭터가 주인공

### 4.2 스토리 구조 포맷

```markdown
# Story: {제목}

## 로그라인
{1문장 요약}

## 테마
{핵심 주제}

## 캐릭터
- 주인공: {이름/설명}
- (선택) 조연: {이름/설명}

## 서사 구조

### ACT 1: 발단
- 음악 구간 / 씬 범위: {구간명 또는 씬ID 범위}
- 에너지: {값}/10
- 감정: {무드 태그}
- 서사: {이 구간에서 일어나는 이야기}
- 핵심 이미지: {대표 장면 묘사}

### ACT 2~4: {동일 포맷}

## 감정 아크 요약
| 구간 | 에너지 | 서사 감정 | 동기화 확인 |
```

### 4.3 산출물

- `work/S2-story/story.md`
- `work/S2-story/emotion-sync-table.json`
- `work/S2-story/TASK-REPORT.md`

### ★ 중간 확인 #1

> 유저에게 story.md 요약 제출. **승인 전까지 S3 미진입.**

### Gate-S2

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| story.md 존재 | 크기 > 0 | 재생성 |
| ACT 수 | ≥ 3개 | 재구성 |
| 감정 아크 테이블 빈 행 | 0건 | 보완 |
| 유저 승인 | 명시적 승인 | 수정 후 재제출 |

---

## 5. 콘티 대본 생성 (S3-conti)

**쓰기 권한**: `work/S3-conti/` 만

> 🗂️ **이 단계 필수 참조**: `SKILL-1A_story-conti-GUIDE-story-visual-design.md`  
>
> - §4 감정 전환점(Pivot) 연출 규칙 — 장면 간 emotion 계열 변화 시 적용  
> - §5 장면 리듬 설계 — 시퀀스 시트 내 샷 사이즈 배치 결정 시 적용  
> - §7 Gate 추가 항목 — Gate-S3 통과 기준 강화 (이 가이드 적용 결과 포함)

### 5.1 장면 분할 규칙 (v4: N컷 가변)

1. **컷 분할 기준**: 감정 전환점(pivot) + 음악 구간 경계(뮤비) 또는 씬 전환(드라마)에서 끊음
2. **최소 컷 수**: ACT당 2컷 → 전체 최소 6컷
3. **최대 컷 수**: 제한 없음 (시퀀스 시트 수로 관리)
4. **시퀀스 시트 매핑**: 전체 N컷 → `ceil(N/9)` 장의 시퀀스 시트
5. 각 시트 내 9컷은 읽기 순서 = 시간 순서:

```
[1-1] [1-2] [1-3]
[2-1] [2-2] [2-3]
[3-1] [3-2] [3-3]
```

1. **마지막 시트가 9컷 미만**이면 빈 셀은 `"empty"` 표기
2. 시트 간 연속성: 이전 시트 마지막 컷의 감정/조명이 다음 시트 첫 컷과 자연스럽게 이어져야 함

### 5.2 프레임 지시서 포맷 (v4: prompt_seed 내장)

**각 장면마다 아래 모든 항목 작성. 빠뜨리면 Gate 실패.**

```json
{
  "scenes": [
    {
      "scene_id": "scene-01",
      "sheet_id": "SEQ-01",
      "grid_position": "1-1",
      "act": "ACT 1",
      "music_section": "intro",
      "timecode": { "start": "0:00", "end": "0:15" },
      "duration_sec": 15,

      "narrative": {
        "action": "주인공이 카페 유리문 앞에 서서 Help Wanted 스티커를 바라본다",
        "emotion": "hopeful",
        "story_beat": "일상에서의 새로운 시작"
      },

      "visual": {
        "shot_size": "medium-long",
        "camera_angle": "eye-level",
        "camera_movement": "static → slow dolly in",
        "composition": "주인공을 프레임 좌측 1/3에 배치, 카페 문이 우측 2/3",
        "depth_of_field": "shallow (f/2.8)",
        "lighting": "golden hour backlight, 역광으로 실루엣 가장자리 빛남",
        "color_palette": "warm amber + soft blue shadow",
        "background": "도심 골목길의 작은 카페 외관, 나무 벤치, 화분"
      },

      "character_direction": {
        "character_id": "char_01",
        "pose": "standing, weight on left leg, slight head tilt right",
        "expression": "neutral → gentle smile",
        "gaze_direction": "카페 문의 스티커를 바라봄 (시선 우측 위)",
        "outfit": "default",
        "outfit_note": "후드 살짝 내려 어깨선 보임"
      },

      "audio_direction": {
        "bgm_section": "intro — 피아노 아르페지오",
        "sfx": "도시 소음, 새 지저귀는 소리",
        "dialogue": null,
        "narration": null
      },

      "transition": {
        "to_next": "match_cut",
        "transition_detail": "카페 문 손잡이 → 다음 컷 카페 내부 카운터"
      },

      "prompt_seed": {
        "subject_key": "standing with weight on left leg, slight head tilt, neutral to gentle smile, gazing at cafe door sign",
        "setting_key": "small neighborhood cafe exterior, glass door with help wanted sticker, wooden bench, potted plants, cobblestone sidewalk",
        "camera_key": "medium-long shot, eye-level, slow dolly in, subject left-third, shallow DOF f/2.8",
        "lighting_key": "golden hour backlight, warm amber rim light, soft blue fill, subtle lens flare",
        "mood_override": null
      }
    }
  ]
}
```

### 5.3 prompt_seed 규칙

- `subject_key`: 포즈+표정+시선 키워드 (캐릭터 앵커 태그와 **합쳐져서** SUBJECT 블록이 됨)
- `setting_key`: 장소+오브젝트 키워드 → SETTING 블록으로 직접 변환
- `camera_key`: 샷+앵글+무브먼트+구도+DOF → CAMERA 블록으로 직접 변환
- `lighting_key`: 광원+색온도+특수효과 → LIGHTING 블록으로 직접 변환
- `mood_override`: 감정 톤이 narrative.emotion과 다를 때만 사용 (보통 null)

**이 4개 키가 있으면 S4(1B)는 기계적 확장만 수행한다.**

### 5.4 산출물

- `work/S3-conti/conti-script.json` — 전체 N장면
- `work/S3-conti/conti-summary.md` — 시퀀스 시트별 요약 테이블
- `work/S3-conti/outfit-timeline.json` — 캐릭터별 의상 변경 타임라인 (**SKILL-2 필수 입력**)
- `work/S3-conti/TASK-REPORT.md`

> `outfit-timeline.json` 생성 규칙: §10 참조

**conti-summary.md 포맷:**

```markdown
## SEQ-01 (scene-01 ~ scene-09)

| # | 위치 | 구간 | 타임코드 | 장면 한 줄 요약 | 샷 | 감정 |
|---|------|------|---------|---------------|-----|------|
| 1 | 1-1 | intro | 0:00-0:15 | 카페 앞에 서 있는 주인공 | ML | hopeful |
| 2 | 1-2 | verse1 | 0:15-0:32 | ... | ... | ... |
...

## SEQ-02 (scene-10 ~ scene-18)
| # | 위치 | 구간 | ... |
...
```

### ★ 중간 확인 #2

> 유저에게 conti-summary.md + scene-01 상세 JSON을 제출.  
> "콘티 초안입니다. 장면 수/순서/감정 흐름을 확인해주세요."  
> **승인 전까지 S4 미진입.**

### Gate-S3

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| 장면 수 | ≥ 6 | 보완 |
| 필수 필드 누락 | 0건 | 보완 후 재검증 |
| grid_position | 시트 내 중복 없음 | 수정 |
| sheet_id 연속성 | SEQ-01, SEQ-02... 순서 | 수정 |
| prompt_seed 존재 | 모든 씬에 4개 키 존재 | 수정 |
| timecode 연속성 (뮤비) | 끊김/겹침 없음 | 수정 |
| 시트 간 감정 연속성 | 이전 마지막↔다음 첫 컷 자연스러움 | 수정 |
| 유저 승인 | 명시적 승인 | 수정 후 재제출 |

---

# SKILL-1B: 콘티 → 시퀀스 시트 프롬프트 생성

---

## 6. 이미지 생성 프롬프트 제작 (S4-prompts)

**쓰기 권한**: `work/S4-prompts/` 만  
**필수 참조**: `REFERENCE-prompt-and-frame-guide.md`

### 6.1 입력

- `work/S3-conti/conti-script.json` (1A 산출물) 또는 유저 직접 제공 프레임 지시서
- `work/S1-analysis/character-anchor-tag.md` (캐릭터 앵커)
- 프로젝트 스타일 설정 (STYLE 프리셋 선택)

### 6.2 프롬프트 구조 (7블록)

```
[1. SUBJECT] 캐릭터 앵커 태그 + prompt_seed.subject_key
[2. OUTFIT]  캐릭터 default_outfit + outfit_note
[3. SETTING] prompt_seed.setting_key 확장
[4. LIGHTING] prompt_seed.lighting_key 확장
[5. CAMERA]  prompt_seed.camera_key 확장
[6. STYLE]   프로젝트 스타일 프리셋 (고정)
[7. NEGATIVE] 공통 부정어 + 장면 특화 부정어
```

### 6.3 prompt_seed → 7블록 변환 규칙

**이 규칙이 S3→S4 변환의 핵심. 에이전트 재량 개입 최소화.**

1. **SUBJECT** = `character-anchor-tag.md의 1줄 축약` + `,` + `prompt_seed.subject_key`
2. **OUTFIT** = `character-profile.json의 default_outfit` 영문 변환 + `outfit_note` 반영
3. **SETTING** = `prompt_seed.setting_key`를 REFERENCE Part 2.1 키워드로 보강
4. **LIGHTING** = `prompt_seed.lighting_key`를 REFERENCE Part 2.2 키워드로 보강
5. **CAMERA** = `prompt_seed.camera_key` 그대로 (이미 충분히 구체적)
6. **STYLE** = S0에서 확정한 프리셋 문자열 (전 씬 동일)
7. **NEGATIVE** = REFERENCE Part 3.2 공통 + 화풍별 + 장면 특화 자동 조합

### 6.4 샷 사이즈별 블록 가중치

> SUBJECT 블록의 기술 범위를 샷에 따라 조절

| 샷 사이즈 | SUBJECT 비중 | SETTING 비중 | 비고 |
|----------|-------------|-------------|------|
| extreme-close-up | 90% (눈/입 디테일) | 10% | 배경 거의 생략 |
| close-up | 70% (얼굴+목선) | 30% | |
| medium | 50% (상반신+표정) | 50% | |
| medium-long | 35% (무릎 위) | 65% | |
| long | 20% (전신) | 80% | |
| extreme-long | 10% (실루엣) | 90% | 환경 중심 |

### 6.5 시퀀스 시트별 출력

파일 구조:

```
work/S4-prompts/
├── SEQ-01/
│   ├── scene-01-prompt.md
│   ├── scene-02-prompt.md
│   ├── ...
│   ├── scene-09-prompt.md
│   └── grid-SEQ-01-prompt.md    ← 3x3 통합 프롬프트
├── SEQ-02/
│   ├── scene-10-prompt.md
│   ├── ...
│   └── grid-SEQ-02-prompt.md
└── prompt-index.json
```

### 6.6 개별 씬 프롬프트 파일 포맷

파일명: `scene-{NN}-prompt.md`

```markdown
# Scene {NN} — Sheet {SEQ-XX} Grid [{row}-{col}]
## Emotion: {감정 태그}

### Positive Prompt
[SUBJECT]
{7블록 변환 결과}

[OUTFIT]
{...}

[SETTING]
{...}

[LIGHTING]
{...}

[CAMERA]
{...}

[STYLE]
{프리셋}

### Negative Prompt
{공통 + 화풍별 + 장면 특화}

### Generation Parameters (권장)
- Aspect Ratio: 16:9 (1920x1080)
- CFG Scale: 7~8
- Steps: 30~50
- Sampler: DPM++ 2M Karras
```

### 6.7 3x3 그리드 통합 프롬프트

파일명: `grid-{SEQ-XX}-prompt.md`

```markdown
# 3x3 Grid — {SEQ-XX}

## Grid Layout
3x3 grid layout, cinematic storyboard, 9 sequential panels:
[top-left: {scene-XX 한 줄}] [top-center: {XX+1}] [top-right: {XX+2}]
[middle-left: {XX+3}] [middle-center: {XX+4}] [middle-right: {XX+5}]
[bottom-left: {XX+6}] [bottom-center: {XX+7}] [bottom-right: {XX+8}]

## Character Anchor
{캐릭터 앵커 태그 — 9컷 일관성 보장}

## Style Coherence
{스타일 프리셋 — 전 셀 통일}

## Negative
{공통 부정어}
inconsistent character appearance between panels, different art styles between panels
```

### 6.8 프롬프트 피드백 루프

**S4 내부 서브스텝** (v4 신규):

1. **SEQ-01의 scene-01 프롬프트만 먼저 생성** → 유저에게 샘플 제출
2. 유저가 이미지 생성 테스트 후 피드백
3. 피드백 반영하여 프롬프트 보정 (앵커 태그 or 스타일 조정)
4. **보정된 기준으로 나머지 전체 일괄 생성**

### 6.9 시트 간 연속성 검증

일괄 생성 후, 다음을 자동 검증:

- 캐릭터 앵커 태그가 모든 SUBJECT 블록에 동일하게 포함되어 있는가
- 의상 변경이 스토리상 정당한 시점에서만 발생하는가
- 조명/시간대가 시트 경계에서 급변하지 않는가 (의도적 전환 제외)

### 6.10 산출물

- `work/S4-prompts/SEQ-{XX}/scene-{NN}-prompt.md` (N개)
- `work/S4-prompts/SEQ-{XX}/grid-SEQ-{XX}-prompt.md` (시트 수만큼)
- `work/S4-prompts/prompt-index.json`

**prompt-index.json 포맷:**

```json
{
  "total_scenes": 18,
  "total_sheets": 2,
  "style_preset": "photorealistic",
  "character_anchor": "young Korean man, late 20s, sharp jawline...",
  "sheets": [
    {
      "sheet_id": "SEQ-01",
      "scenes": [
        {
          "scene_id": "scene-01",
          "grid_position": "1-1",
          "emotion": "hopeful",
          "shot_size": "medium-long",
          "file": "SEQ-01/scene-01-prompt.md"
        }
      ],
      "grid_file": "SEQ-01/grid-SEQ-01-prompt.md"
    }
  ]
}
```

### ★ 중간 확인 #3

> scene-01-prompt.md 샘플 제출 → 유저 테스트 → 피드백 → 보정 → 나머지 일괄 생성

### Gate-S4

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| 프롬프트 파일 수 | = N(씬) + S(시트) | 보완 |
| 7블록 구조 | 모든 파일에서 7블록 존재 | 수정 |
| 캐릭터 앵커 일관성 | 모든 SUBJECT에 동일 앵커 | 수정 |
| prompt_seed→블록 매칭 | 콘티의 seed와 프롬프트 불일치 0건 | 수정 |
| 부정 프롬프트 | 모든 파일에 존재 | 추가 |
| prompt-index.json | 유효 JSON, 전 씬 포함 | 수정 |
| 시트 간 연속성 | 검증 통과 | 수정 |

---

## 7. 최종 패키징 (S5-package)

**쓰기 권한**: `output/`

```
output/
├── story.md
├── conti-script.json
├── conti-summary.md
├── outfit-timeline.json            ← SKILL-2 필수 입력
├── prompts/
│   ├── SEQ-01/
│   │   ├── scene-01-prompt.md ~ scene-09-prompt.md
│   │   └── grid-SEQ-01-prompt.md
│   ├── SEQ-02/
│   │   └── ...
│   └── prompt-index.json
├── references/
│   ├── music-analysis.json (또는 synopsis-analysis.json)
│   ├── character-profile.json
│   └── character-anchor-tag.md
└── FINAL-REPORT.md
```

### FINAL-REPORT.md

```markdown
# Final Report: Story-Conti-Prompt Generation

## 요약
- 모드: {뮤비/드라마/단편}
- 스토리: {제목} / {로그라인}
- 장면 수: {N}
- 시퀀스 시트 수: {S}
- 캐릭터: {이름} / 스타일: {프리셋}

## 산출물 체크리스트
| 파일 | 상태 | 비고 |
|------|------|------|

## SKILL-2 핸드오프 정보
1. conti-script.json — 편집 순서/타임코드
2. prompt-index.json — 장면-감정 매핑
3. music-analysis.json — 비트 싱크 (뮤비 모드)
4. story.md — 서사 흐름 참조
5. outfit-timeline.json — 캐릭터 의상 변경 타임라인
```

### Gate-S5

| 항목 | 기준 |
|------|------|
| output/ 내 필수 파일 | story.md, conti-script.json, prompt-index.json, FINAL-REPORT.md |
| 프롬프트 파일 수 | = N + S |
| conti-script.json | JSON 파싱 성공 + N장면 |

---

## 8. 실패 처리 매트릭스

| 실패 지점 | 제공 가능 산출물 | 조치 |
|----------|----------------|------|
| S1 실패 | 없음 | 입력 파일 확인 요청 |
| S2 실패 | 분석 데이터 | 수동 스토리 요청 |
| S3 실패 | 스토리 + 분석 | 수동 콘티 요청 |
| S4 실패 | 스토리 + 콘티 | 수동 프롬프트 요청 |

모든 실패 시 `work/` 폴더 전체 보존. 유저에게 빈 손 없음.

---

## 9. SKILL-2 핸드오프 규격

| 파일 | SKILL-2 사용 목적 | 필수 필드 |
|------|------------------|----------|
| conti-script.json | 클립 순서, 타임코드 | scene_id, sheet_id, grid_position, timecode, transition |
| music-analysis.json | 비트 싱크, 에너지 기반 컷 타이밍 | sections[].start_sec, energy, bpm |
| prompt-index.json | 장면-감정 매핑, 시트 구조 | sheets[].scenes[].emotion, scene_id, shot_size |
| outfit-timeline.json | 클립 의상 일치 검증, 씬별 outfit 확인 | character_id, timeline[].scene_id, outfit_state |
| story.md | 서사 흐름 순서 | ACT 구분, 서사 요약 |

**스키마 변경 시 양쪽 모두 업데이트하라.**

---

## 부록 A: conti-script.json 최소 스키마 (v4)

```json
{
  "$schema": "conti-script-v4",
  "project_title": "",
  "mode": "mv|drama|short",
  "total_scenes": 0,
  "total_sheets": 0,
  "style_preset": "",
  "scenes": [
    {
      "scene_id": "scene-01",
      "sheet_id": "SEQ-01",
      "grid_position": "1-1",
      "act": "ACT 1",
      "music_section": "",
      "timecode": { "start": "", "end": "" },
      "duration_sec": 0,
      "narrative": { "action": "", "emotion": "", "story_beat": "" },
      "visual": {
        "shot_size": "", "camera_angle": "", "camera_movement": "",
        "composition": "", "depth_of_field": "",
        "lighting": "", "color_palette": "", "background": ""
      },
      "character_direction": {
        "character_id": "", "pose": "", "expression": "",
        "gaze_direction": "", "outfit": "", "outfit_note": ""
      },
      "audio_direction": {
        "bgm_section": "", "sfx": "", "dialogue": null, "narration": null
      },
      "transition": { "to_next": "", "transition_detail": "" },
      "prompt_seed": {
        "subject_key": "", "setting_key": "",
        "camera_key": "", "lighting_key": "",
        "mood_override": null
      }
    }
  ]
}
```

## 부록 B: music-analysis.json 최소 스키마

```json
{
  "$schema": "music-analysis-v3",
  "title": "", "artist": "", "genre": "",
  "bpm": 0, "key": "", "total_duration_sec": 0,
  "sections": [
    {
      "name": "intro", "start_sec": 0, "end_sec": 0,
      "energy": 0, "mood": [], "instruments": "", "description": ""
    }
  ],
  "climax_section": "", "pivot_points": []
}
```

---

## 10. 의상 타임라인 생성 규칙 (outfit-timeline.json)

> S3 콘티 생성 완료 직후, `conti-script.json`의 `character_direction.outfit` 필드를 기반으로 자동 생성한다.

### 10.1 생성 조건

- 캐릭터시트가 제공된 경우만 생성 (캐릭터시트 없으면 빈 배열로 생성)
- 캐릭터가 2명 이상인 경우 `characters[]` 안에 캐릭터별 배열로 분리

### 10.2 최소 스키마

```json
{
  "$schema": "outfit-timeline-v1",
  "project_title": "",
  "characters": [
    {
      "character_id": "char_01",
      "default_outfit": "(character-profile.json의 default_outfit 요약)",
      "timeline": [
        {
          "scene_id": "scene-01",
          "sheet_id": "SEQ-01",
          "outfit_state": "default",
          "outfit_delta": null,
          "outfit_note": "후드 살짝 내려 어깨선 보임"
        },
        {
          "scene_id": "scene-05",
          "sheet_id": "SEQ-01",
          "outfit_state": "changed",
          "outfit_delta": "재킷 탈의, 흰 셔츠 소매 걷어올림",
          "outfit_note": "감정 고조 구간 — 긴장 해소 행동"
        }
      ],
      "changes": [
        {
          "change_id": "ch-01",
          "from_scene": "scene-04",
          "to_scene": "scene-05",
          "description": "재킷 탈의",
          "reason": "시간 경과 + 에너지 상승",
          "applies_to": ["scene-05", "scene-06", "scene-07", "scene-08", "scene-09"]
        }
      ]
    }
  ]
}
```

### 10.3 규칙

| 항목 | 규칙 |
|------|------|
| `outfit_state` | `"default"` / `"changed"` / `"partial"` 중 하나 |
| `outfit_delta` | `"default"` 상태이면 `null`, 변경 시 변경 내용 1줄 영문 |
| `changes[].applies_to` | 변경 이후 해당 의상이 유지되는 씬 ID 전체 목록 |
| 씬 누락 금지 | `conti-script.json`의 모든 `scene_id`가 `timeline[]`에 존재해야 함 |
| Gate-S3 추가 항목 | `outfit-timeline.json` 존재 + 씬 목록 누락 0건 |
