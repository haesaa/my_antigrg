---
name: 02-analyze
description: >
  음악 메타데이터를 분석하고, 입력된 이미지 에셋(표정시트, 캐릭터시트)을 참고하여 기승전결 구조의 스토리를 자동 생성합니다.
---

# 02-analyze: S2 음악 분석 + 스토리 생성 스킬

> **실행자**: Analyzer (Teammate 1)
> **실행 시점**: 01-input-gate 통과 후
> **쓰기 권한**: `work/S2-story/` 만
> **MCP 폴백**: 로컬 분석 (별도 MCP 불필요)

## 목적

음악 메타데이터(BPM, Key, 구간 구조, 비트 타이밍)를 정밀 파싱하고, 유저가 제공한 캐릭터 에셋(표정/외형)을 참고하여 음악의 무드·에너지 곡선에 맞는 **기승전결 스토리**를 자동 생성합니다.

## 실행 시점

- 01-input-gate가 MV-Story 모드를 확정한 후 자동 활성화됩니다.

## 워크플로우

### Step 0: music-meta.md 파싱 (T1-SKIP 포함)

- `input/music-meta.md`에서 아래 정보를 JSON으로 구조화합니다:

  ```json
  {
    "bpm": 94,
    "key": "F# minor",
    "duration_sec": 317.4,
    "total_beats": 261,
    "sections": [
      { "label": "Section 1", "start": "0:00", "end": "0:30", "beat_count": 42 }
    ],
    "beats": [3.200, 3.838, ...]
  }
  ```

- 출력: `work/S2-story/audio_meta.json`

### Step 1: 구간별 무드/에너지 추론

- 각 Section의 **beat_count**와 **위치(전반/중반/후반)**를 기반으로 에너지 레벨과 무드를 자동 추론합니다.
  - beat_count 높은 구간 → 고에너지 (클라이맥스, 액션)
  - beat_count 0인 구간 → 저에너지 (여운, 엔딩, 인스트루멘탈)
  - 곡 초반 → 도입/설정
  - 곡 중반 → 전개/갈등
  - 곡 후반 → 절정/해소
- 출력: 각 Section에 `mood`, `energy` 필드 추가

### Step 2: 캐릭터 에셋 분석

- **표정시트(3×4)**: 그리드를 분할하여 12개 표정 감정 태깅
  - 예: `frame_01: 미소`, `frame_02: 놀람`, `frame_03: 슬픔` ...
  - 이 감정 팔레트는 이후 콘티에서 씬별 표정 매칭에 사용됩니다.
- **캐릭터시트**: 캐릭터 외형을 텍스트로 기술
  - 헤어스타일, 의상, 색상 팔레트, 체형, 특징적 소품 등
- 출력: `work/S2-story/character_profile.json`

### Step 3: 스토리 자동 생성

- 입력: `audio_meta.json` + `character_profile.json` + (선택) `synopsis.md`
- **시놉시스가 제공된 경우**: 시놉시스를 기반으로 음악 구간에 맞게 스토리를 재배치합니다.
- **시놉시스가 없는 경우**: 음악의 무드/에너지 곡선과 캐릭터 정보만으로 오리지널 스토리를 창작합니다.
- 스토리 구조:
  - **기(起)**: 도입, 세계관/캐릭터 소개
  - **승(承)**: 전개, 갈등 또는 관계 심화
  - **전(轉)**: 전환점, 클라이맥스
  - **결(結)**: 해소, 여운, 엔딩
- 출력: `work/S2-story/story.json`

  ```json
  {
    "title": "자동 생성된 스토리 제목",
    "synopsis": "전체 줄거리 2~3문장 요약",
    "characters": [
      {
        "id": "char_01",
        "name": "주인공",
        "appearance": "캐릭터시트 기반 외형 설명",
        "personality": "추론된 성격",
        "expression_palette": ["미소", "놀람", "슬픔", "분노", ...]
      }
    ],
    "acts": [
      {
        "act": 1,
        "label": "기(起) - 도입",
        "sections": [1, 2],
        "time_range": "0:00-1:00",
        "mood": "mysterious, anticipation",
        "energy": "low-to-mid",
        "story_beat": "주인공이 낯선 도시에 홀로 도착한다"
      }
    ]
  }
  ```

### Step 4: 완료 확인 및 기록

- JSON 스키마 유효성 검증 (필수 필드 누락 체크)
- `PIPELINE-LOG.md`에 S2 완료 기록
- S3(콘티/대본 생성) 단계 활성화 핸드오프

## 관련 파일

| File | Purpose |
|------|---------|
| `01-input-gate.md` | 입력 파일 검증 및 모드 확정 |
| `03-storyboard.md` | 생성된 스토리를 기반으로 콘티/대본을 작성하는 다음 단계 |

## 예외사항

1. music-meta.md 파싱 실패: 구간 구조가 비표준일 경우 30초 단위 균등 분할로 폴백합니다.
2. 시놉시스 미제공: 음악 무드만으로 범용 서사(성장/여행/감정 변화 등)를 자동 생성합니다.
3. 표정시트 그리드 감지 실패: 균등 분할 로직으로 폴백하고 감정 태깅은 기본 세트를 적용합니다.
