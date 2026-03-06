---
name: 03-storyboard
description: >
  S2에서 생성된 스토리를 기반으로 영상 콘티(Storyboard), 사운드이펙트(SFX) 프롬프트, Qwen3 TTS용 목소리 대본을 구성합니다.
---

# 03-storyboard: S3 콘티 + SFX + TTS 대본 스킬

> **실행자**: Creator (Teammate 2)
> **실행 시점**: S2 완료 후
> **쓰기 권한**: `work/S3-storyboard/` 만

## 목적

S2에서 생성된 스토리(`story.json`)와 캐릭터 프로필(`character_profile.json`)을 바탕으로, 유저가 제공한 3×4 표정시트와 캐릭터시트 사진을 보고 영상의 **세부 콘티(Storyboard)**, **사운드이펙트(SFX) 프롬프트**, **Qwen3 TTS에 넣을 목소리 대본**을 작성합니다.

## 워크플로우

### Step 1: 콘티(Storyboard) 구성

스토리의 각 Act > Section을 **씬(Scene)** 단위로 분해합니다. 각 씬에 대해 다음을 상세 기술합니다:

| 항목 | 설명 | 예시 |
|------|------|------|
| **씬 ID** | 고유 식별자 | `scene_01` |
| **시간 범위** | 음악 구간 매핑 | `0:00-0:30` |
| **카메라 앵글** | 샷 타입 | `클로즈업`, `미디엄 샷`, `버드아이` |
| **캐릭터 표정** | 표정시트 매칭 | `frame_03 (슬픔)` |
| **캐릭터 동작** | 제스처/움직임 | `천천히 고개를 돌리며 창밖을 응시` |
| **배경** | 장소/환경 | `비 내리는 도시 거리, 네온사인 반사` |
| **조명** | 라이팅 무드 | `역광, 블루톤 쿨라이팅` |
| **트랜지션** | 이전 씬과의 연결 | `Dissolve 1.5s` |
| **연출 노트** | 추가 지시어 | `감정이 고조되는 부분, 슬로우모션 효과` |

출력: `work/S3-storyboard/storyboard.json`

```json
[
  {
    "scene_id": "scene_01",
    "act": 1,
    "section": 1,
    "time_range": "0:00-0:30",
    "camera": {
      "angle": "wide_shot",
      "movement": "slow_dolly_in"
    },
    "character": {
      "expression": "frame_01 (무표정, 약간 우울)",
      "action": "혼자 걸어가며 주변을 둘러본다",
      "outfit": "기본 의상 (캐릭터시트 참조)"
    },
    "background": "안개 낀 새벽 도시, 인적 없는 골목",
    "lighting": "로우키 라이팅, 청회색 톤",
    "transition_in": "Fade from black (2s)",
    "direction_note": "분위기 잡기, 미스터리한 도입부"
  }
]
```

### Step 2: SFX(사운드이펙트) 프롬프트 생성

각 씬에 어울리는 환경음/효과음을 자연어 프롬프트로 생성합니다. 이 프롬프트는 추후 SFX 생성 도구(Elevenlabs SFX, Freesound 등)에 직접 입력할 수 있는 형태입니다.

출력: `work/S3-storyboard/sfx_prompts.json`

```json
[
  {
    "scene_id": "scene_01",
    "time_range": "0:00-0:30",
    "sfx_layers": [
      {
        "type": "ambient",
        "prompt": "이른 새벽 도시 골목길, 먼 곳에서 들리는 자동차 소리, 잔잔한 바람",
        "volume": "low"
      },
      {
        "type": "foley",
        "prompt": "느린 발걸음 소리, 콘크리트 바닥",
        "volume": "medium"
      }
    ]
  }
]
```

### Step 3: TTS 목소리 대본 작성

각 씬의 내레이션, 독백, 대사를 한국어 대본으로 작성합니다. 각 대본 라인에는 **감정 지시어(emotion_instruct)**를 반드시 포함하여 Qwen3 TTS가 감정을 실어 읽을 수 있도록 합니다.

출력: `work/S3-storyboard/tts_script.json`

```json
[
  {
    "scene_id": "scene_01",
    "line_id": "line_001",
    "time_range": "0:00-0:30",
    "speaker": "char_01",
    "text": "이곳은... 어디지? 낯선 거리, 낯선 사람들. 아무것도 기억나지 않는다.",
    "language": "Korean",
    "emotion_instruct": "혼란스럽고 불안한 목소리, 약간 떨리는 톤, 낮은 볼륨으로 독백",
    "voice_style": "내레이션 (1인칭 독백)",
    "pause_after_sec": 1.5
  },
  {
    "scene_id": "scene_01",
    "line_id": "line_002",
    "time_range": "0:20-0:30",
    "speaker": "char_01",
    "text": "...가야 해. 어딘가로.",
    "language": "Korean",
    "emotion_instruct": "결심한 듯 차분하지만 약간의 두려움이 섞인 목소리",
    "voice_style": "독백",
    "pause_after_sec": 2.0
  }
]
```

### Step 4: 크로스 검증 (Self-QC)

- **표정 매칭 검증**: 스토리보드의 `character.expression`이 실제 표정시트의 감정과 일치하는지 확인
- **시간 연속성 검증**: 씬 간 `time_range`가 겹침 없이 연속적인지 확인
- **대본-씬 정합성**: TTS 대본의 `scene_id`가 스토리보드에 존재하는 유효한 씬인지 확인
- **감정 지시어 품질**: `emotion_instruct`가 구체적이고 TTS 모델이 이해할 수 있는 형태인지 검수

### Step 5: 완료 확인

- 3개 JSON 파일(`storyboard.json`, `sfx_prompts.json`, `tts_script.json`)의 스키마 유효성 검증
- `PIPELINE-LOG.md`에 S3 완료 기록
- S4(TTS 생성) 단계 활성화 핸드오프

## 디벨롭 가이드 (살 붙이기)

> 콘티와 대본은 1차 초안 생성 후 반드시 **디벨롭(Develop)** 과정을 거쳐야 합니다.

1. **감정 곡선 보강**: 씬 간 감정 변화가 급격하지 않은지 확인하고, 자연스러운 그라데이션으로 보완
2. **대사 다듬기**: TTS가 자연스럽게 읽을 수 있도록 문장 길이 조절 (한 문장당 20~50자 권장)
3. **SFX 레이어링**: 단일 효과음이 아닌 2~3개의 레이어(ambient + foley + accent)로 구성
4. **빈 씬 방지**: 대사가 없는 씬이라도 `"(무음 - 영상만)"` 또는 환경음 지시 명시
5. **캐릭터 어조 일관성**: 같은 캐릭터의 `emotion_instruct`가 성격 설정과 모순되지 않는지 확인

## 관련 파일

| File | Purpose |
|------|---------|
| `02-analyze.md` | 스토리 및 캐릭터 프로필 데이터 제공 |
| `04-tts-generate.md` | TTS 대본을 음성 파일로 변환하는 다음 단계 |

## 예외사항

1. 스토리 없이 진행 요청: 음악 구간별 기본 감정 템플릿(도입→고조→절정→여운)으로 최소 콘티 자동 생성
2. 캐릭터 다중인 경우: 표정시트가 여러 캐릭터를 포함할 경우 각각 ID를 부여하여 별도 매핑
3. 대사 없는 인스트루멘탈 구간: SFX만 생성하고 TTS 대본은 빈 배열로 처리
