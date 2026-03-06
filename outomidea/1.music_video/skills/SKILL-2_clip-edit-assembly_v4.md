# SKILL-2: Clip Analysis → Music-Synced Cut Edit & Assembly

> **버전**: v4.0  
> **실행 환경**: Google Antigravity / Claude Sonnet 4.5+  
> **선행 조건**: SKILL-1 v4 산출물 존재 (또는 동등 형식의 수동 입력)  
> **후속 연결**: 없음 (최종 산출물 = 편집 타임라인 + 컷편집 지시서)  
> **최종 갱신**: 2026-03-01

---

## 0. 이 스킬의 정체

**입력**:  

1. 단편 영상 클립 폴더 (유저가 직접 제작한 장면별 영상)
2. SKILL-1 v4 산출물 (conti-script.json, music-analysis.json, story.md, prompt-index.json, character-profile.json, character-anchor-tag.md, conti-summary.md, outfit-timeline.json)
3. 원본 음악 파일 (선택 — 없으면 music-analysis.json만으로 진행)

**출력**: 음악 무드 동기화된 컷편집 타임라인 + 어셈블리 지시서 + ffmpeg 실행 스크립트

**이 스킬이 하는 것**: 영상을 직접 렌더링하지 않는다. 클립을 분석하고, 최적 순서와 편집점을 계산하여 **편집 설계도**를 만든다. ffmpeg 스크립트 생성까지가 범위.

### 0.1 v3 → v4 핵심 변경점

| 항목 | v3 | v4 |
|------|----|----|
| 핸드오프 규격 | 4개 파일 의존 | **8개 파일**, graceful degradation 원칙 |
| 클립-씬 매칭 | 전략 A/B/C 순차 시도 | **스코어 매트릭스 (0~100점)** + 확신도 등급 |
| N컷 대응 | 9컷 고정 전제 ("9/9") | **N컷 가변, 시퀀스 시트(3×3) 단위** |
| 의상 검증 | 없음 | **outfit-timeline.json 기반 의상 변화 추적** |
| 무드 벡터 | confidence 없음 | **confidence + rationale 필드 추가** |
| 매칭 알고리즘 | 순차 시도 | **전체 N×M 매트릭스 → 그리디 최적 배정** |

---

## 1. 전역 규칙

SKILL-1과 동일한 전역 규칙 적용:

- 삭제 금지, 쓰기 격리, 원본 보존, UTF-8, 로깅
- 추가: **영상 클립 원본은 절대 인코딩/변환하지 마라** (분석용 메타데이터 추출만)

---

## 2. 프로젝트 초기화 (E0-preflight)

**쓰기 권한**: `project-{timestamp}/` 루트

### 2.1 디렉토리 구조

```
project-edit-{YYYYMMDD-HHmmss}/
├── input/
│   ├── clips/                  ← 유저의 단편 영상 클립들
│   ├── skill1-output/          ← SKILL-1 v4 산출물 전체 복사
│   │   ├── conti-script.json       ← [필수] N씬 콘티+prompt_seed+sheet_id
│   │   ├── music-analysis.json     ← [필수:뮤비] 음악 구간/BPM/에너지
│   │   ├── story.md                ← [필수] 서사 구조 (ACT 순서)
│   │   ├── prompt-index.json       ← [필수] 장면-감정 매핑, 시트 구조
│   │   ├── character-profile.json  ← [필수] 캐릭터 외형 데이터
│   │   ├── character-anchor-tag.md ← [필수] 캐릭터 앵커 태그 (1줄 축약)
│   │   ├── conti-summary.md        ← [권장] 시트별 요약 테이블
│   │   └── outfit-timeline.json    ← [필수] 의상 변화 타임라인
│   └── music/                  ← 원본 음악 (선택)
├── work/
│   ├── E1-clip-analysis/       ← 클립 메타 + 무드 분석
│   ├── E2-matching/            ← 스코어 매트릭스 + 매칭 결과
│   ├── E3-timeline/            ← 타임라인 설계
│   └── E4-assembly/            ← 편집 지시서 + 스크립트
├── output/                     ← 최종 산출물
├── logs/
└── PIPELINE-LOG.md
```

### 2.2 입력 검증

아래 표의 순서대로 검증하라. **"실패 시" 열의 행동을 정확히 따르라.**

| # | 검증 항목 | 기준 | 실패 시 | 비고 |
|---|----------|------|---------|------|
| 1 | clips/ 내 영상 파일 | ≥ 1개, 확장자 .mp4/.mov/.avi/.webm | **중단** — "영상 클립이 없습니다" 알림 | 이 검증 실패 시 나머지 검증 불필요 |
| 2 | conti-script.json | JSON 파싱 성공 + `scenes[]` 배열 존재 + `total_scenes` 정수 + `total_sheets` 정수 | **중단** — "콘티 데이터가 유효하지 않습니다" 알림 | v4 필수 필드: scene_id, sheet_id, grid_position |
| 3 | music-analysis.json | JSON 파싱 성공 + `sections[]` 배열 존재 + `bpm` 정수 | **뮤비 모드: 중단** / 드라마·단편: 경고 후 계속 | 없으면 비트 싱크 비활성, 에너지 매칭 비활성 |
| 4 | story.md | 파일 존재 + `### ACT` 헤더 ≥ 3개 | 경고 후 계속 — 서사 순서 검증 단계 생략 | |
| 5 | prompt-index.json | JSON 파싱 성공 + `sheets[]` 배열 존재 | 경고 후 계속 — 감정 보조 참조 생략 | |
| 6 | character-profile.json | JSON 파싱 성공 + `character_id` 필드 존재 | 경고 후 계속 — 캐릭터/의상 검증 생략 | |
| 7 | character-anchor-tag.md | 파일 존재 + 내용 1줄 이상 | 경고 후 계속 — 캐릭터 식별 참조 생략 | |
| 8 | outfit-timeline.json | JSON 파싱 성공 + `timeline[]` 배열 존재 (빈 배열 허용 = 의상 변화 없음) | 경고 후 계속 — 의상 검증 생략 | |
| 9 | 클립 파일 재생 가능 | ffprobe로 스트림 정보 추출 성공 | 해당 클립 제외 후 계속 | 제외된 클립은 로그에 기록 |

**원칙**: 검증 #1(클립)과 #2(콘티)만 **hard fail**. 나머지는 **graceful degradation** — 해당 기능을 비활성화하고 진행하되, 비활성화된 기능을 로그와 유저 알림에 명시하라.

---

## 3. 클립 분석 (E1-clip-analysis)

**쓰기 권한**: `work/E1-clip-analysis/` 만

### 3.1 기술 메타데이터 추출

**각 클립에 대해 아래 정보를 추출하라:**

```json
{
  "clip_id": "clip-001",
  "filename": "scene_cafe_exterior.mp4",
  "technical": {
    "duration_sec": 12.5,
    "resolution": "1920x1080",
    "fps": 30,
    "codec": "h264",
    "bitrate_kbps": 8000,
    "audio_present": true,
    "audio_codec": "aac",
    "filesize_mb": 15.2
  }
}
```

추출 방법 (우선순위):

1. ffprobe MCP
2. ffprobe 로컬 CLI
3. 파일 헤더 직접 읽기

### 3.2 파일명 파싱

**에이전트는 클립의 프레임을 직접 보지 못할 수 있다.** 이 한계를 전제로, 파일명에서 최대한 정보를 추출하는 것이 E1의 핵심이다.

**파일명 파싱 규칙 (모든 클립에 대해 실행):**

1. 확장자 제거 후 토큰 분리 (구분자: `_`, `-`, `.`, 공백, 카멜케이스)
2. 각 토큰을 아래 카테고리로 분류:

| 카테고리 | 판별 기준 | 예시 |
|----------|----------|------|
| `sequence_number` | 순수 숫자 또는 `scene` + 숫자 | `01`, `scene03`, `s7` |
| `location_keyword` | 장소를 나타내는 일반 명사 | `cafe`, `street`, `room`, `park`, `exterior`, `interior` |
| `action_keyword` | 동작을 나타내는 동사/명사 | `enter`, `walk`, `meet`, `dance`, `run`, `cry`, `smile` |
| `character_keyword` | 캐릭터 식별 | `char01`, `heroine`, `male`, `female` |
| `mood_keyword` | 감정/분위기 | `happy`, `sad`, `tense`, `calm` |
| `noise` | 위 어디에도 해당 안 됨 | `IMG`, `DSC`, `MVI`, `final`, `v2`, `edit` |

1. 파싱 결과를 JSON으로 기록:

```json
{
  "clip_id": "clip-001",
  "filename": "01_cafe_enter.mp4",
  "filename_parsed": {
    "sequence_number": 1,
    "location_keywords": ["cafe"],
    "action_keywords": ["enter"],
    "character_keywords": [],
    "mood_keywords": [],
    "noise_tokens": [],
    "meaningful_token_count": 3,
    "parse_quality": "good"
  }
}
```

**`parse_quality` 판정 기준:**

- `"good"`: `sequence_number` 존재 + (location 또는 action) 1개 이상 → meaningful_token_count ≥ 2
- `"partial"`: `sequence_number`만 존재, 또는 location/action만 존재 → meaningful_token_count = 1
- `"poor"`: meaningful_token_count = 0 (예: `IMG_0234.mp4`, `clip.mp4`)

**중요**: `parse_quality == "poor"`인 클립이 전체의 50% 이상이면, E1 완료 시점에 유저에게 다음을 알려라:
> "클립 파일명에서 장면 정보를 충분히 추출할 수 없습니다. 클립-씬 매핑의 정확도가 낮을 수 있습니다. 가능하면 파일명을 `{순번}_{장소}_{액션}.mp4` 형식으로 수정하거나, 수동 매핑 테이블을 제공해주세요."

### 3.3 시각 내용 분석 — 콘티 크로스레퍼런스

**에이전트가 클립 프레임을 직접 볼 수 없을 때의 분석 전략이다. 이것이 이 스킬의 핵심.**

각 클립에 대해, conti-script.json의 모든 씬과 **예비 매칭 점수(preliminary score)**를 계산한다. 이 점수는 E2에서 최종 매칭에 사용된다.

**예비 매칭 점수 계산 (클립 1개 × 씬 1개):**

아래 6개 요소를 합산한다. **각 요소의 점수를 정확히 지켜라.**

#### 요소 1: 파일명 씬번호 매칭 (최대 30점)

| 조건 | 점수 |
|------|------|
| 파일명의 `sequence_number` == 씬의 `scene_id` 내 순번 (예: clip `01` ↔ scene-01) | **30** |
| 순번 차이가 ±1 (예: clip `02` ↔ scene-01) | **15** |
| `sequence_number`가 없거나 차이 ≥ 2 | **0** |

- `scene_id`에서 순번 추출법: `scene-01` → 1, `scene-12` → 12
- 파일명에 순번이 없으면 (`parse_quality == "poor"`) 이 요소는 항상 0

#### 요소 2: 파일명 키워드 매칭 (최대 15점)

파일명의 `location_keywords` + `action_keywords`가 씬의 아래 필드 텍스트에 포함되는지 확인:

- `narrative.action`
- `visual.background`
- `character_direction.pose` (action 키워드만)

| 조건 | 점수 |
|------|------|
| 매칭 토큰 1개당 | **+5** (최대 15) |
| 매칭 토큰 0개 | **0** |

- 매칭 판정: 대소문자 무시, 부분 문자열 매칭 허용 (예: `cafe` → "카페"는 불가, `cafe` → "cafe exterior"는 가능)
- 한글 키워드는 영문 동의어로 변환 후 비교 시도 (예: 파일명 `카페` → `cafe`로 변환)

#### 요소 3: 클립 duration 대응 (최대 15점)

클립의 `technical.duration_sec` vs 씬의 `duration_sec`를 비교한다.

| 조건 | 점수 |
|------|------|
| 오차 ≤ 20% (즉, `abs(clip_dur - scene_dur) / scene_dur ≤ 0.2`) | **15** |
| 오차 ≤ 50% | **10** |
| 오차 ≤ 100% | **5** |
| 오차 > 100% | **2** (완전 0점은 주지 않음 — 클립 분할 가능성 있으므로) |

- 클립이 씬보다 긴 경우: 트림으로 해결 가능하므로 감점을 줄인다 (위 기준의 한 단계 위 점수 적용)
- 예: 클립 30초, 씬 15초 → 오차 100% → 본래 5점이지만 "클립이 더 길므로" 한 단계 위 → **10점**

#### 요소 4: 무드 벡터 일치 (최대 20점)

클립의 `mood_vector.primary` vs 씬의 `narrative.emotion`을 비교한다.

| 조건 | 점수 |
|------|------|
| 정확 일치 (예: 둘 다 "hopeful") | **20** |
| 같은 valence (둘 다 positive 또는 둘 다 negative) | **12** |
| valence 불일치 | **0** |

**valence 분류표** (이 표를 기준으로 판정하라):

- **positive**: hopeful, tender, energetic, euphoric, triumphant, playful, whimsical, romantic, cathartic, serene, peaceful
- **negative**: melancholic, nostalgic, ominous, tense, fierce, longing, angry, lonely, fearful
- **ambiguous**: dreamy, mysterious, bittersweet, rebellious → positive로 간주

#### 요소 5: 에너지 레벨 일치 (최대 10점)

클립의 `mood_vector.energy_level` vs 씬이 속한 음악 구간의 `energy`를 비교한다.

| 조건 | 점수 |
|------|------|
| delta ≤ 1 | **10** |
| delta ≤ 2 | **7** |
| delta ≤ 3 | **4** |
| delta > 3 | **0** |

- music-analysis.json이 없으면 (드라마/단편 모드) 이 요소는 **모든 씬에 5점 균일 부여** (중립)

#### 요소 6: 순서 위치 일치 (최대 10점)

클립의 파일 정렬 순서 (clips/ 내 알파벳 정렬) vs 씬의 전체 순서 (scene-01=1, scene-02=2...)를 비교한다.

| 조건 | 점수 |
|------|------|
| 정확 일치 (예: 3번째 파일 ↔ scene-03) | **10** |
| 차이 ±1 | **5** |
| 차이 ±2 이상 | **0** |

- 이 요소는 유저가 클립을 순서대로 이름 붙였을 때만 유효. `parse_quality == "poor"`면 이 요소도 신뢰도 낮음.

---

**예비 매칭 점수 요약:**

| 요소 | 최대 | 출처 |
|------|------|------|
| 파일명 씬번호 | 30 | filename ↔ scene_id |
| 파일명 키워드 | 15 | filename ↔ narrative/visual |
| duration 대응 | 15 | ffprobe ↔ conti timecode |
| 무드 벡터 일치 | 20 | mood_vector ↔ narrative.emotion |
| 에너지 레벨 | 10 | mood_vector ↔ music section energy |
| 순서 위치 | 10 | file sort order ↔ scene order |
| **합계** | **100** | |

### 3.4 무드 스코어링

**각 클립에 무드 벡터를 할당하라.** music-analysis.json의 무드 사전과 동일한 태그를 사용한다.

```json
{
  "clip_id": "clip-001",
  "mood_vector": {
    "primary": "hopeful",
    "secondary": "tender",
    "energy_level": 4,
    "valence": "positive",
    "arousal": "low-medium",
    "confidence": "inferred",
    "rationale": "파일명 'cafe_enter' + conti scene-01 emotion 'hopeful' 크로스레퍼런스"
  }
}
```

**`confidence` 값과 부여 기준:**

| confidence | 조건 | 의미 |
|-----------|------|------|
| `"direct"` | 유저가 클립에 무드 태그를 직접 제공 | 가장 높은 신뢰도 |
| `"inferred"` | 파일명 키워드 + conti 감정 태그 크로스레퍼런스로 도출 | 보통 신뢰도 |
| `"guessed"` | 파일 순서 기반으로 대응되는 씬의 감정을 그대로 복사 | 낮은 신뢰도 |

**무드 판단 로직 (순서대로 시도):**

1. 파일명에 `mood_keyword` 있음 → 해당 무드 사용, confidence = `"inferred"`
2. 파일명 `sequence_number`로 매칭되는 씬의 `narrative.emotion` 사용 → confidence = `"inferred"`
3. 파일명에 `location_keyword`/`action_keyword` 있고, 이것이 특정 씬과 매칭 → 해당 씬의 emotion 사용 → confidence = `"inferred"`
4. 위 모두 실패 → 파일 정렬 순서로 대응되는 씬의 emotion 복사 → confidence = `"guessed"`

### 3.5 의상 타임라인 참조 (outfit-timeline.json 활용)

**outfit-timeline.json이 존재하고 유효할 때만 이 단계를 실행한다.**

각 클립의 예비 매칭 결과(3.3에서 가장 높은 점수의 씬)를 기준으로, 해당 씬에 적용되는 의상을 조회하여 `expected_outfit` 필드를 추가한다.

```json
{
  "clip_id": "clip-004",
  "content_analysis": {
    "matched_scene_id": "scene-04",
    "expected_outfit": {
      "base_outfit": "gray tank top, black zip-up hoodie, blue denim shorts, white sneakers",
      "modifications": ["add: brown apron"],
      "change_source": "outfit-change-01",
      "description": "기본 의상 위에 카페 에이프런 추가"
    },
    "outfit_verification": "cannot_verify_visually",
    "outfit_note": "에이전트 시각 검증 불가 — 중간확인에서 유저 확인 요청 예정"
  }
}
```

**조회 로직:**

1. outfit-timeline.json의 `changes[].applies_to[]`에 해당 scene_id가 포함되어 있는지 확인
2. 포함되면: `default_outfit` + 해당 change의 `outfit_delta` 적용
3. 포함 안 되면: `default_outfit` 그대로

**현실적 한계 명시**: 에이전트가 클립 프레임을 볼 수 없으므로 실제 의상 일치 여부를 자동 검증할 수 없다. `expected_outfit`은 **유저가 수동 확인할 때의 체크리스트**로 사용된다.

### 3.6 산출물

- `work/E1-clip-analysis/clip-manifest.json` — 전체 클립 기술 메타 + 파일명 파싱 + 예비 매칭 점수(상위 3개 씬)
- `work/E1-clip-analysis/mood-scores.json` — 클립별 무드 벡터 (confidence/rationale 포함)
- `work/E1-clip-analysis/outfit-check.json` — 클립별 expected_outfit (outfit-timeline.json 존재 시에만)
- `work/E1-clip-analysis/TASK-REPORT.md`

### Gate-E1

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| clip-manifest.json | 클립 수 = clips/ 내 유효 파일 수 | 재분석 |
| 모든 클립에 `filename_parsed` | 존재 | 재파싱 |
| mood_vector | 모든 클립에 존재 + confidence 필드 포함 | 보완 |
| 파일명 파싱 품질 경고 | `parse_quality == "poor"` 비율 < 50% | 유저 알림 (중단은 아님) |

---

## 4. 클립-장면 매칭 및 순서 결정 (E2-matching)

**쓰기 권한**: `work/E2-matching/` 만

### 4.1 스코어 매트릭스 생성

**E1에서 계산한 예비 매칭 점수를 N(클립) × M(씬) 전체 매트릭스로 조합한다.**

```json
{
  "score_matrix": {
    "clips": ["clip-001", "clip-002", "clip-003"],
    "scenes": ["scene-01", "scene-02", "scene-03"],
    "scores": [
      [85, 12, 5],
      [10, 78, 15],
      [3, 20, 92]
    ]
  }
}
```

위 예시: clip-001↔scene-01 = 85점, clip-001↔scene-02 = 12점, ...

### 4.2 매칭 알고리즘

**스코어 매트릭스에서 1:1 최적 배정을 수행한다. 아래 순서를 정확히 따르라.**

```
STEP 1: 스코어 매트릭스 N×M 생성 (E1 예비 점수 사용)
STEP 2: 그리디 배정 — 전체 매트릭스에서 최고 점수 셀부터 확정
         → 확정된 클립 행과 씬 열을 제거
         → 남은 매트릭스에서 반복
         → 모든 클립 또는 모든 씬이 소진될 때까지
STEP 3: 각 배정 결과에 확신도 등급 부여
STEP 4: 미배정 항목 분류
```

**STEP 2 상세 — 그리디 배정 규칙:**

1. 매트릭스에서 최고 점수 셀 (i, j) 를 찾는다
2. clip-i ↔ scene-j 를 확정한다
3. clip-i 행 전체와 scene-j 열 전체를 매트릭스에서 제거한다
4. 남은 매트릭스에서 1~3 반복
5. 매트릭스가 비거나, 남은 셀의 최고 점수가 0이면 종료

**STEP 3 — 확신도 등급:**

| 스코어 범위 | 확신도 | 자동/수동 | 설명 |
|------------|--------|----------|------|
| 80 ~ 100 | `"high"` | **자동 확정** | 매칭 신뢰할 수 있음 |
| 50 ~ 79 | `"medium"` | **잠정 배정** — 중간확인에서 유저에게 노란색 표시 | 대체로 맞지만 확인 권장 |
| 30 ~ 49 | `"low"` | **유저 확인 필수** — 후보 상위 3개 씬 제시 | 신뢰도 낮음 |
| 0 ~ 29 | `"unmatched"` | **미매칭** — 유저에게 직접 매핑 요청 | 자동 매칭 불가 |

**STEP 4 — 미배정 항목 처리:**

| 상황 | 분류 | 처리 |
|------|------|------|
| 씬에 매칭된 클립 없음 | `unmatched_scenes` | 유저에게 알림 + "해당 구간 스킵 or 인접 클립 확장" 선택지 |
| 클립에 매칭된 씬 없음 | `unmatched_clips` → B-roll 분류 | 타임라인 여유 구간에 삽입 제안 |

### 4.3 갈등 해결 (동점/경합)

| 상황 | 해결 로직 |
|------|----------|
| 1 장면에 2+ 클립이 동점 | duration 대응 점수가 높은 쪽 선택. 여전히 동점이면 파일 정렬 순서가 앞인 것 선택. 나머지는 B-roll |
| 1 클립에 2+ 장면이 경합 | 클립 duration이 두 씬 합계의 80% 이상이면 → 클립 분할(in/out 포인트) 제안. 미만이면 → 점수 높은 씬에 배정 |
| 장면에 매칭 클립 없음 | 유저에게 알림. 선택지: (a) 해당 구간 스킵, (b) 인접 클립 확장, (c) 유저가 추가 클립 제공 |
| 클립에 매칭 장면 없음 | B-roll 분류. 타임라인의 에너지 하강 구간 또는 전환 구간에 삽입 제안 |

### 4.4 순서 결정 원칙

매칭이 확정된 클립들의 재생 순서를 결정한다.

1. **서사 순서 우선**: story.md의 ACT 순서 → conti의 sheet_id + grid_position 순서가 기본
2. **시퀀스 시트 단위 그루핑**: 같은 sheet_id 내의 클립들은 grid_position 순서(1-1, 1-2, 1-3, 2-1...) 유지
3. **음악 구간 정렬**: 각 장면의 timecode가 해당 음악 구간에 위치하도록
4. **에너지 흐름 보존**: 음악의 에너지 곡선을 클립의 에너지가 따라가도록
5. **전환 자연스러움**: 연속된 두 클립 간 시각적 급변(jump cut) 최소화

**N컷 가변 대응:**

- SKILL-1 v4에서 총 장면 수 N은 가변이며, `ceil(N/9)`장의 시퀀스 시트로 그루핑됨
- 마지막 시트가 9컷 미만일 수 있음 → `prompt-index.json`의 `empty_cells[]` 배열을 참조하여 빈 슬롯은 커버리지 계산 및 match-table 할당 대상에서 원천 스킵한다.
- 커버리지 계산: `매칭된 클립 수 / total_scenes` (empty_cells는 전체 분모인 total_scenes에 이미 제외되어 있음)

### 4.5 매칭 결과 테이블

```json
{
  "match_table": [
    {
      "sequence_order": 1,
      "scene_id": "scene-01",
      "sheet_id": "SEQ-01",
      "grid_position": "1-1",
      "clip_id": "clip-001",
      "match_score": 85,
      "confidence": "high",
      "match_type": "auto",
      "score_breakdown": {
        "filename_number": 30,
        "filename_keyword": 10,
        "duration": 15,
        "mood": 20,
        "energy": 10,
        "position": 0
      },
      "music_section": "intro",
      "music_energy": 3,
      "clip_energy": 4,
      "energy_delta": 1,
      "mood_alignment": "matched",
      "expected_outfit": "gray tank top + black hoodie + denim shorts",
      "outfit_change": false
    }
  ],
  "unmatched_clips": [],
  "unmatched_scenes": [],
  "b_roll_clips": [],
  "coverage": "9/9",
  "coverage_ratio": 1.0,
  "auto_confirmed_count": 7,
  "needs_user_check_count": 2
}
```

### 4.6 산출물

- `work/E2-matching/score-matrix.json` — 전체 N×M 스코어 매트릭스
- `work/E2-matching/match-table.json` — 매칭 결과 (위 포맷)
- `work/E2-matching/sequence-order.json` — 최종 재생 순서
- `work/E2-matching/TASK-REPORT.md`

### ★ 중간 확인 #1

유저에게 아래 내용을 제출하라. **유저 승인 전까지 E3로 넘어가지 마라.**

> **제출 내용:**
>
> 1. match-table 요약 (씬ID / 클립파일명 / 스코어 / 확신도 / 매칭 근거 1줄)
> 2. `confidence == "medium"` 항목: 노란색 표시 + "확인 부탁" 메모
> 3. `confidence == "low"` 항목: 후보 상위 3개 씬 목록
> 4. `confidence == "unmatched"` 항목: 빨간색 표시 + 직접 매핑 요청
> 5. 미매칭 씬 목록 + 미매칭 클립(B-roll) 목록
> 6. **의상 변화 포인트** — outfit-timeline.json에서 변화가 있는 씬들을 별도 표시:
>    "scene-04부터 의상 변화(에이프런 추가)가 있습니다. 해당 클립의 의상이 맞는지 확인해주세요."
>
> **질문 형태:**
> "클립-장면 매칭 결과입니다. 순서나 매칭을 수정할 부분이 있나요?"

### Gate-E2

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| 매칭 커버리지 | ≥ 80% (`매칭 클립 / total_scenes ≥ 0.8`) | 유저 확인 필수 |
| sequence-order.json | 빈 항목 없음 (B-roll 제외) | 보완 |
| 유저 승인 | 명시적 | 수정 후 재제출 |
| 스코어 매트릭스 | JSON 유효 + 행/열 수 = 클립/씬 수 | 재생성 |

---

## 5. 타임라인 설계 (E3-timeline)

**쓰기 권한**: `work/E3-timeline/` 만

### 5.1 타임라인 구조

음악의 시간축을 기준으로 클립을 배치한다.

```json
{
  "$schema": "edit-timeline-v4",
  "music_source": "input/music/song.mp3",
  "music_duration_sec": 210,
  "bpm": 128,
  "total_scenes": 18,
  "total_sheets": 2,
  "timeline": [
    {
      "order": 1,
      "scene_id": "scene-01",
      "sheet_id": "SEQ-01",
      "grid_position": "1-1",
      "clip_id": "clip-001",
      "clip_file": "input/clips/01_cafe_enter.mp4",
      "match_score": 85,
      "match_confidence": "high",
      
      "placement": {
        "timeline_start_sec": 0.0,
        "timeline_end_sec": 14.5,
        "clip_in_sec": 0.5,
        "clip_out_sec": 11.8,
        "speed_factor": 1.0
      },
      
      "music_sync": {
        "section": "intro",
        "beat_snap_point_sec": 0.0,
        "on_beat": true,
        "energy_match": true
      },
      
      "transition_in": {
        "type": "fade_in",
        "duration_sec": 1.0,
        "params": { "from_black": true }
      },
      "transition_out": {
        "type": "crossfade",
        "duration_sec": 0.8,
        "params": {}
      },
      
      "audio": {
        "clip_audio_action": "mute",
        "volume_db": 0
      },
      
      "color_grade": {
        "apply": false,
        "preset": null,
        "notes": ""
      }
    }
  ]
}
```

### 5.2 비트 싱크 규칙

1. **컷 전환은 비트에 맞춰라**
   - BPM에서 비트 간격 = 60/BPM 초
   - 각 컷 전환점이 가장 가까운 비트에 스냅되어야 한다
   - 허용 오차: ±50ms (beat_snap_threshold)

2. **에너지 변화 지점에서 전환**
   - 음악 구간이 바뀌는 지점(verse→chorus 등)에서 반드시 컷 전환
   - 에너지 급상승 시: sharp_cut 또는 match_cut
   - 에너지 완만 변화 시: crossfade 또는 dissolve

3. **클립 속도 조절 (선택)**
   - 클립이 해당 구간보다 짧으면: speed_factor < 1.0 (슬로모션)
   - 클립이 해당 구간보다 길면: clip_in/clip_out으로 잘라내기 우선, 부족하면 speed_factor > 1.0

4. **music-analysis.json이 없을 때 (드라마/단편 모드)**
   - 비트 싱크 비활성: `on_beat: false` 고정
   - 컷 전환 타이밍은 서사 전환점(ACT 경계, 감정 전환점)에 맞춤
   - 에너지 매칭은 콘티의 narrative.emotion 기반으로 추론

### 5.3 전환 효과 선택 기준

| 음악 변화 | 감정 변화 | 추천 전환 |
|----------|----------|----------|
| 구간 전환 (verse→chorus) | 긍정→더 긍정 | match_cut |
| 구간 전환 | 긍정→부정 | dissolve (길게, 1.5s) |
| 같은 구간 내 | 동일 감정 | crossfade (짧게, 0.5s) |
| 브릿지 진입 | 전환/반전 | fade_to_black → fade_in |
| 클라이맥스 | 최고조 | sharp_cut (0.1s 이하) |
| 아웃트로 | 여운 | slow dissolve (2.0s) |
| 첫 장면 | - | fade_in from black (1.5s) |
| 마지막 장면 | - | fade_out to black (2.0s) |

### 5.4 오디오 트랙 설계

```json
{
  "audio_tracks": [
    {
      "track_id": "bgm",
      "type": "music",
      "file": "input/music/song.mp3",
      "start_sec": 0,
      "end_sec": 210,
      "volume_db": 0,
      "fade_in_sec": 0,
      "fade_out_sec": 2.0
    },
    {
      "track_id": "sfx-layer",
      "type": "sfx",
      "events": [
        {
          "time_sec": 5.0,
          "sfx": "ambient_cafe",
          "volume_db": -12,
          "duration_sec": 8.0
        }
      ]
    }
  ],
  "clip_audio_policy": "mute_all"
}
```

**자동 생성 (v4 추가):**

- E3 타임라인 생성 시, `conti-script.json` 각 씬의 `audio_direction.sfx` 필드를 읽는다.
- 해당 필드에 텍스트가 있을 경우 (null이 아님), 타임라인의 `sfx-layer` 이벤트 목록을 자동 생성한다 (`time_sec`는 해당 컷 시작 시점 동기화).

클립 원본 오디오 처리:

- **기본**: 전체 mute (음악이 주 오디오)
- **예외**: 클립에 의미 있는 대사/효과음이 있으면 volume_db 조절하여 믹싱
- 유저에게 클립 오디오 처리 방식 사전 확인

### 5.5 산출물

- `work/E3-timeline/edit-timeline.json` — 전체 타임라인
- `work/E3-timeline/timeline-visual.md` — 텍스트 시각화 (아래 참조)
- `work/E3-timeline/TASK-REPORT.md`

**timeline-visual.md 포맷:**

```
음악: |===intro===|====verse1====|==pre-ch==|=====chorus1=====|...
시간: 0s          15s            32s        40s                65s
클립: |--clip-001--|---clip-002---|--clip-03-|-----clip-004-----|...
전환:       fade_in    crossfade    match_cut    sharp_cut
에너지: ▁▂▃▃▃▃▃▃▃▃▃▄▄▄▅▅▅▅▅▅▅▅▆▆▆▇▇▇▇▇▇▇▇█████████████
의상:  [default]  [default]  [default]  [+apron]  [+apron]  [+apron]  [default]...
```

### Gate-E3

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| 타임라인 연속성 | 갭/오버랩 없음 | 수정 |
| 비트 싱크 (뮤비 모드) | 전환점 오차 ≤ 50ms | 재스냅 |
| 전체 길이 | 음악 길이 ± 2초 이내 (뮤비) | 조정 |
| 전환 효과 | 모든 컷에 지정 | 보완 |
| edit-timeline.json | JSON 유효 + `$schema == "edit-timeline-v4"` | 수정 |
| sheet_id 연속성 | 시트 순서 유지 | 수정 |

---

## 6. 어셈블리 지시서 + 스크립트 생성 (E4-assembly)

**쓰기 권한**: `work/E4-assembly/` 만

### 6.1 편집 지시서 (사람이 읽는 문서)

파일명: `work/E4-assembly/edit-direction.md`

```markdown
# 편집 지시서: {프로젝트명}

## 개요
- 음악: {곡명} ({길이})
- 총 장면: {N}개 (시퀀스 시트 {S}장)
- 매칭된 클립: {M}개
- 총 컷 전환: {K}회
- 예상 최종 영상 길이: {초}s
- 매칭 자동 확정률: {auto_confirmed / total}%

## 의상 변화 타임라인
| 구간 | 씬 범위 | 의상 상태 | 비고 |
(outfit-timeline.json 기반 — 없으면 이 섹션 생략)

## 컷 시트

### CUT 1 (0:00 ~ 0:14) — SEQ-01 [1-1]
- **클립**: clip-001 (01_cafe_enter.mp4)
- **매칭 스코어**: 85/100 (high)
- **사용 구간**: 0.5s ~ 11.8s
- **음악 구간**: intro
- **전환 IN**: fade in from black (1.0s)
- **전환 OUT**: crossfade to CUT 2 (0.8s)
- **속도**: 1.0x
- **오디오**: mute clip audio
- **컬러**: 원본 유지
- **의상**: default (gray tank top + black hoodie)
- **비고**: 비트 0:00에 맞춰 시작

### CUT 2 (0:14 ~ 0:32) — SEQ-01 [1-2]
...

## 특수 편집 노트
- {클라이맥스 구간 강조 편집 등}
- {B-roll 삽입 위치 등}
- {의상 변화 포인트 주의사항}

## 렌더 설정 (권장)
- 해상도: 1920x1080
- FPS: 30
- 코덱: H.264 (CRF 18)
- 오디오: AAC 320kbps
```

### 6.2 ffmpeg 실행 스크립트

파일명: `work/E4-assembly/assemble.sh`

**스크립트 생성 규칙:**

1. 각 클립의 trim + scale + 전환을 하나의 filter_complex로 구성
2. 음악을 별도 오디오 입력으로 병합
3. 주석으로 각 단계 설명
4. 실패 시 중간 파일 보존 (임시 파일 자동 삭제하지 않음)

**스크립트 구조 (예시):**

```bash
#!/bin/bash
# Auto-generated by SKILL-2 v4 Edit Pipeline
# Project: {project_name}
# Generated: {timestamp}
# Scenes: {N}, Sheets: {S}, Clips matched: {M}

set -e  # 에러 시 중단

# === 변수 ===
MUSIC="input/music/song.mp3"
OUTPUT="output/final.mp4"
TEMP_DIR="work/E4-assembly/temp"
mkdir -p "$TEMP_DIR"

# === Step 1: 각 클립 트림 ===
# CUT 1: clip-001 (scene-01, SEQ-01 [1-1]) — score: 85, confidence: high
ffmpeg -y -i "input/clips/01_cafe_enter.mp4" \
  -ss 0.5 -to 11.8 \
  -c:v libx264 -crf 18 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1" \
  -an \
  "$TEMP_DIR/cut-01.mp4"

# CUT 2: clip-002 (scene-02, SEQ-01 [1-2]) — score: 78, confidence: medium
# ... (각 클립 반복)

# === Step 2: 전환 효과 적용 + 연결 ===
ffmpeg -y \
  -i "$TEMP_DIR/cut-01.mp4" \
  -i "$TEMP_DIR/cut-02.mp4" \
  -i "$TEMP_DIR/cut-03.mp4" \
  # ... 모든 컷 입력
  -i "$MUSIC" \
  -filter_complex "
    [0:v]fade=t=in:st=0:d=1.0[v0];
    [v0][1:v]xfade=transition=fade:duration=0.8:offset=13.7[v01];
    [v01][2:v]xfade=transition=wipeleft:duration=0.5:offset=31.2[v012];
    # ... 전체 전환 체인
    [v_final]fade=t=out:st=208:d=2.0[vout]
  " \
  -map "[vout]" -map "{N}:a" \
  -c:v libx264 -crf 18 -preset medium \
  -c:a aac -b:a 320k \
  -shortest \
  "$OUTPUT"

echo "=== Assembly complete: $OUTPUT ==="
echo "Duration: $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $OUTPUT)s"
```

### 6.3 검증 스크립트

파일명: `work/E4-assembly/verify.sh`

```bash
#!/bin/bash
# 어셈블리 결과 검증

OUTPUT="output/final.mp4"

echo "=== Verification ==="

# 파일 존재
[ -f "$OUTPUT" ] && echo "✅ File exists" || echo "❌ File missing"

# 길이 확인
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT")
echo "Duration: ${DURATION}s"

# 해상도 확인
RES=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$OUTPUT")
echo "Resolution: $RES"

# 코덱 확인
VCODEC=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$OUTPUT")
ACODEC=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$OUTPUT")
echo "Video codec: $VCODEC"
echo "Audio codec: $ACODEC"

# 파일 크기
SIZE=$(du -h "$OUTPUT" | cut -f1)
echo "File size: $SIZE"
```

### 6.4 산출물

- `work/E4-assembly/edit-direction.md` — 편집 지시서 (사람용)
- `work/E4-assembly/assemble.sh` — ffmpeg 실행 스크립트
- `work/E4-assembly/verify.sh` — 검증 스크립트
- `work/E4-assembly/TASK-REPORT.md`

### Gate-E4

| 항목 | 기준 | 실패 시 |
|------|------|---------|
| edit-direction.md | 모든 CUT에 필수 필드 (스코어, 의상, 전환) | 보완 |
| assemble.sh | bash -n 문법 검사 통과 | 수정 |
| ffmpeg 명령어 | 입력 파일 경로 전부 실존 확인 | 수정 |
| 전환 offset | 이전 컷 종료 시간과 일치 | 재계산 |

---

## 7. 최종 패키징 (E5-package)

**쓰기 권한**: `output/`

### 산출물 구조

```
output/
├── edit-direction.md           ← 편집 지시서
├── edit-timeline.json          ← 타임라인 데이터 (v4 스키마)
├── timeline-visual.md          ← 시각화
├── assemble.sh                 ← ffmpeg 스크립트
├── verify.sh                   ← 검증 스크립트
├── analysis/
│   ├── clip-manifest.json      ← 클립 분석 결과
│   ├── mood-scores.json        ← 무드 스코어 (confidence 포함)
│   ├── score-matrix.json       ← N×M 매칭 스코어 매트릭스
│   ├── match-table.json        ← 매칭 결과
│   └── outfit-check.json       ← 의상 검증 데이터 (있을 때만)
└── FINAL-REPORT.md
```

### FINAL-REPORT.md

```markdown
# Final Report: Clip Edit & Assembly (v4)

## 요약
- 입력 클립: {N}개
- 총 장면 (SKILL-1): {M}개 (시퀀스 시트 {S}장)
- 매칭 성공: {K}/{M}
- 매칭 자동 확정(high): {H}개
- 매칭 유저 확인(medium+low): {L}개
- 미매칭: {U}개
- 총 컷 전환: {T}회
- 예상 최종 길이: {초}s
- 비트 싱크 정확도: {%} (뮤비 모드)
- 의상 변화 포인트: {C}회

## 실행 방법
1. output/ 폴더에서 assemble.sh 확인
2. 필요 시 edit-direction.md로 수동 조정
3. `bash assemble.sh` 실행
4. `bash verify.sh`로 결과 검증

## 주의사항
- ffmpeg 4.4+ 필요 (xfade 필터 지원)
- 클립 원본 파일 위치가 input/clips/에 있어야 함
- 음악 파일 위치가 input/music/에 있어야 함

## Graceful Degradation 상태
| 기능 | 상태 | 사유 |
(입력 검증에서 비활성화된 기능 목록)
```

---

## 8. 실패 처리 매트릭스

| 실패 지점 | 제공 가능 산출물 | 조치 |
|----------|----------------|------|
| E1 실패 | 없음 | 클립 파일 형식/코덱 확인 요청 |
| E2 실패 | 클립 분석 결과 + 스코어 매트릭스 | 유저에게 매트릭스 제공 + 수동 매칭 요청 |
| E3 실패 | 매칭 테이블 | 수동 타임라인 작성용 데이터 제공 |
| E4 실패 | 타임라인 + 편집 지시서 | 지시서 기반 수동 편집 가능 |

모든 실패 시 `work/` 폴더 전체 보존. 유저에게 빈 손 없음.

---

## 9. SKILL-1 v4 산출물 의존 명세 (완전판)

### 9.1 필수 파일 (없으면 스킬 실행 불가 또는 기능 대폭 저하)

| SKILL-1 파일 | 이 스킬에서 읽는 필드 | 소비 단계 | 용도 |
|-------------|-------------------|----------|------|
| conti-script.json | `scenes[].scene_id` | E1, E2 | 클립 매칭 키 |
| conti-script.json | `scenes[].sheet_id` | E2 | 시트 단위 그루핑, N컷 대응 |
| conti-script.json | `scenes[].grid_position` | E2 | 시트 내 순서 결정 |
| conti-script.json | `scenes[].timecode` | E3 | 타임라인 배치 |
| conti-script.json | `scenes[].duration_sec` | E1, E3 | 클립 길이 대조, 매칭 스코어 요소 3 |
| conti-script.json | `scenes[].visual.*` | E1 | 파일명 키워드 매칭 대조, 매칭 스코어 요소 2 |
| conti-script.json | `scenes[].transition` | E3 | 전환 효과 힌트 |
| conti-script.json | `scenes[].narrative.emotion` | E1 | 무드 매칭, 매칭 스코어 요소 4 |
| conti-script.json | `scenes[].narrative.action` | E1 | 파일명 키워드 매칭, 매칭 스코어 요소 2 |
| conti-script.json | `scenes[].character_direction` | E1 | 캐릭터/의상 검증 |
| conti-script.json | `total_scenes` | E2 | 커버리지 분모 |
| conti-script.json | `total_sheets` | E2 | 시트 수 검증 |
| music-analysis.json | `bpm` | E3 | 비트 간격 계산 (60/bpm초) |
| music-analysis.json | `sections[].name` | E2, E3 | 구간명 매칭 |
| music-analysis.json | `sections[].start_sec`, `end_sec` | E3 | 타임라인 구간 경계 |
| music-analysis.json | `sections[].energy` | E1, E2, E3 | 에너지 매칭/곡선, 매칭 스코어 요소 5 |
| music-analysis.json | `sections[].mood[]` | E1, E2 | 무드 매칭 |
| music-analysis.json | `climax_section` | E3 | 클라이맥스 편집 강조 |
| music-analysis.json | `pivot_points[]` | E3 | 전환 효과 강제 포인트 |

### 9.2 보조 파일 (없어도 진행 가능, 해당 기능만 비활성)

| SKILL-1 파일 | 이 스킬에서 읽는 필드 | 소비 단계 | 용도 | 없을 때 |
|-------------|-------------------|----------|------|---------|
| story.md | ACT 구분, 서사 요약 | E2 | 서사 순서 검증 | 순서 검증 생략 |
| prompt-index.json | `sheets[].scenes[].emotion` | E1 | 감정 보조 참조 | 콘티 emotion만 사용 |
| character-profile.json | `character_id`, `default_outfit`, `available_expressions[]` | E1 | 캐릭터/의상 검증 기준 | 캐릭터 검증 생략 |
| character-anchor-tag.md | 1줄 축약 텍스트 | E1 | 캐릭터 식별 기준 | 식별 검증 생략 |
| conti-summary.md | 시트별 요약 테이블 | E2 | 빠른 매칭 참조 | conti-script.json에서 직접 추출 |
| outfit-timeline.json | `changes[].applies_to[]`, `outfit_delta` | E1 | 의상 변화 추적/검증 | 의상 검증 생략 |

### 9.3 SKILL-1 산출물이 없는 경우

- 유저가 직접 콘티/대본/음악정보를 텍스트로 제공하면 동일 포맷으로 파싱 시도
- **최소 필수**: conti-script.json 동등 데이터 (장면 목록 + 순서) — 이것 없으면 스킬 실행 불가
- music-analysis.json 없이도 실행 가능 (비트 싱크 비활성, 에너지 매칭은 콘티 emotion 기반 추론)

---

## 10. outfit-timeline.json 규격 (SKILL-1에서 생성, SKILL-2에서 소비)

**이 섹션은 SKILL-1과 SKILL-2 양쪽에서 참조하는 공유 규격이다.**

### 10.1 스키마

```json
{
  "$schema": "outfit-timeline-v1",
  "character_id": "char_01",
  "default_outfit": {
    "top": "gray tank top",
    "outerwear": "black zip-up hoodie",
    "bottom": "blue denim shorts",
    "shoes": "white sneakers",
    "accessories": []
  },
  "changes": [
    {
      "change_id": "outfit-change-01",
      "trigger_scene": "scene-04",
      "trigger_reason": "카페 근무 시작 — 스토리상 에이프런 착용",
      "outfit_delta": {
        "add": ["brown cafe apron"],
        "remove": [],
        "replace": {}
      },
      "applies_to": ["scene-04", "scene-05", "scene-06"],
      "description": "기본 의상 위에 카페 에이프런 추가"
    },
    {
      "change_id": "outfit-change-02",
      "trigger_scene": "scene-07",
      "trigger_reason": "퇴근 후 외출",
      "outfit_delta": {
        "add": [],
        "remove": ["brown cafe apron"],
        "replace": {
          "outerwear": "black zip-up hoodie (다시 착용)"
        }
      },
      "applies_to": ["scene-07", "scene-08", "scene-09"],
      "description": "에이프런 벗고 기본 의상으로 복귀"
    }
  ]
}
```

### 10.2 SKILL-1에서의 생성 규칙

- **생성 시점**: S3(콘티) 완료 시
- **생성 로직**: conti-script.json의 모든 씬에서 `character_direction.outfit` 값을 순차 스캔
  - `outfit == "default"` → 변화 없음
  - `outfit != "default"` 또는 `outfit_note`에 의상 변경 정보 → `changes[]` 항목 생성
- **변화 없음인 경우**: `changes: []` (빈 배열) — 파일 자체는 생성하되 changes가 비어있음
- **다중 캐릭터**: 캐릭터별 별도 파일 → `outfit-timeline-{character_id}.json`

### 10.3 SKILL-2에서의 소비 규칙

- E1 단계에서 읽기
- 각 클립의 예비 매칭 씬을 기준으로 `applies_to[]` 조회
- `expected_outfit` 필드로 기록 (3.5절 참조)
- **의상 변화가 있는 씬은 중간확인 #1에서 별도 표시** — 유저가 해당 클립의 의상이 맞는지 직접 확인
- 에이전트가 프레임을 볼 수 있는 환경이면 시각 검증 수행, 볼 수 없으면 `"cannot_verify_visually"` 기록

---

## 부록 A: 전환 효과 ffmpeg 매핑

| 전환 이름 | ffmpeg xfade transition | 비고 |
|----------|------------------------|------|
| crossfade | fade | 기본 |
| dissolve | dissolve | crossfade보다 부드러움 |
| sharp_cut | - (트림으로 처리) | 전환 없이 바로 연결. `smash_cut`도 동일 처리 |
| match_cut | fade (duration=0.2) | 짧은 crossfade로 근사 |
| fade_to_black | fadeblack | |
| wipe_left | wipeleft | |
| wipe_right | wiperight | |
| fade_in | fade=t=in (첫 클립만) | 전체 영상 시작 |
| fade_out | fade=t=out (마지막만) | 전체 영상 종료 |
| white_flash | fade=white | GUIDE 전환 추가 (밝은 섬광 효과) |

> **참고 (J-cut)**: `J-cut`/`L-cut`은 영상을 자르면서 오디오는 먼저 진입/나중에 겹쳐 빠지는 **오디오 중심 전환 기법**이다. ffmpeg xfade 범위를 벗어나므로 오디오 채널 분리·레이어 믹싱이 별도 필요하며, 이 스크립트 엔진에서는 영상 타임라인 내 매핑을 기본으로 처리하지 않고 수동 처리 대상으로 둔다.

## 부록 B: 클립 파일명 규칙 (권장)

유저에게 아래 파일명 규칙을 제안하라 (강제 아님):

```
{순번}_{장소}_{액션}.mp4

예시:
01_cafe_exterior_enter.mp4
02_cafe_interior_meet.mp4
03_cafe_counter_interview.mp4
...
```

순번이 있으면 E2 매칭 스코어에서 최대 30점 가산. 키워드가 있으면 추가 15점.

## 부록 C: 에너지 레벨 → 편집 속도 가이드

| 에너지 (1-10) | 평균 컷 길이 | 전환 스타일 | 카메라 특성 |
|-------------|------------|-----------|-----------|
| 1-3 (low) | 8-15초 | dissolve, slow crossfade | 정적, 느린 움직임 |
| 4-6 (mid) | 4-8초 | crossfade, match_cut | 보통 속도 |
| 7-8 (high) | 2-4초 | sharp_cut, fast crossfade | 빠른 전환 |
| 9-10 (peak) | 0.5-2초 | sharp_cut 연속 | 매우 빠른 몽타주 |

이 가이드는 참고용. 음악의 실제 비트와 에너지가 우선.

## 부록 D: 무드 태그 valence 분류표

이 표는 매칭 스코어 요소 4(무드 벡터 일치)에서 valence 비교 시 사용한다.

| 무드 태그 | valence |
|----------|---------|
| hopeful | positive |
| tender | positive |
| energetic | positive |
| euphoric | positive |
| triumphant | positive |
| playful | positive |
| whimsical | positive |
| romantic | positive |
| cathartic | positive |
| serene | positive |
| peaceful | positive |
| melancholic | negative |
| nostalgic | negative |
| ominous | negative |
| tense | negative |
| fierce | negative |
| longing | negative |
| angry | negative |
| lonely | negative |
| fearful | negative |
| dreamy | positive (ambiguous) |
| mysterious | positive (ambiguous) |
| bittersweet | positive (ambiguous) |
| rebellious | positive (ambiguous) |

ambiguous 태그는 positive로 간주하되, 매칭 상대가 정확히 같은 태그면 20점, positive 그룹이면 12점.

## 부록 E: ffprobe로 알 수 있는 것 vs 알 수 없는 것

에이전트의 시각 분석 능력 한계를 정확히 인지하기 위한 참조표.

| ffprobe로 알 수 있는 것 | 용도 | 매칭 스코어 기여 |
|----------------------|------|----------------|
| duration_sec | 씬 길이 대조 | 요소 3 (최대 15점) |
| resolution | 기술 호환성 | 스코어에 직접 기여 안 함 |
| fps | 기술 호환성 | 스코어에 직접 기여 안 함 |
| codec | 기술 호환성 | 스코어에 직접 기여 안 함 |
| audio_present | 오디오 처리 결정 | 스코어에 직접 기여 안 함 |

| ffprobe로 알 수 없는 것 | 의존 대안 | 신뢰도 |
|----------------------|----------|--------|
| 장면 내용 (무엇이 촬영됐는지) | 파일명 파싱 + 콘티 크로스레퍼런스 | 파일명 품질에 전적 의존 |
| 캐릭터 존재 여부 | 파일명 + 콘티 character_direction | 낮음 |
| 조명/색조 | 콘티 visual.lighting 참조만 가능 | 검증 불가 |
| 표정/포즈 | 콘티 character_direction 참조만 | 검증 불가 |
| 의상 | outfit-timeline.json 기대값만 제공 | 검증 불가, 유저 확인 필요 |

**결론**: 파일명이 무의미한 경우(`IMG_0234.mp4` 등), 자동 매칭 최대 스코어는 35점(duration 15 + energy 10 + position 10)에 불과하다. 이는 `"low"` 등급으로, 유저 수동 매핑이 사실상 필수가 된다.
