---
name: 05-generate-audio
description: >
  파이프라인 모드에 따라 오디오 트랙(BGM, 내레이션, 효과음)을 준비합니다. T1 완료 후 T4 영역에서 자동 활성화됩니다(T2/T3와 병렬 실행).
---

# 05-generate-audio: T4 오디오 생성 스킬

> **실행자**: Editor (Teammate 3)
> **실행 시점**: T1 완료 후 (T2와 **병렬** 실행)
> **쓰기 권한**: `work/T4-audio/` 만
> **MCP 폴백**: BGM(Mureka → Fal → Suno), 내레이션(ElevenLabs → Fish Audio)

## 목적

T1에서 분석된 메타데이터(BPM, Mood, 시놉시스 내레이션)를 기반으로 비디오에 씌울 오디오 트랙을 생성 혹은 추출합니다.
이미지/비디오 렌더링(T2, T3)과 완전히 독립적으로 병렬 실행하여 전체 파이프라인 처리 시간을 단축합니다.

## 실행 시점

- 02-analyze (T1) 단계가 완료된 즉시 자동 활성화됩니다.
- 모드에 따라 원본 음악을 패스스루 하거나, 새로운 BGM/보이스가 필요할 때 사용합니다.

## 워크플로우

### Step 1: P1 (MV Mode) 원본 오디오 복사

- P1 모드의 경우 음원 자체를 뮤직비디오로 만드는 것이 목적이므로, 생성 없이 `input/`의 원본을 `work/T4-audio/bgm.mp3`로 복사합니다.

### Step 2: P2 (Scene Mode) BGM 및 내레이션 생성

- **BGM 생성**: `analysis.json`의 무드 태그와 전체 길이를 바탕으로 Mureka(또는 폴백 MCP)에 음악 생성을 요청합니다.
- **내레이션 생성**: 시놉시스에 대사나 독백이 있을 경우 ElevenLabs/Fish Audio를 이용해 장면별 음성 파일(`narration-{NN}.mp3`)을 생성합니다.
- 필요 시 효과음(`sfx-{NN}.mp3`)도 생성합니다.

### Step 3: P3 (Animation Mode) 원본 영상 오디오 추출

- `ffmpeg`를 사용해 입력된 원본 영상에서 오디오 트랙을 추출(`original.mp3`)하여 보존합니다.
- 원본에 오디오가 없으면 무음 파일을 임시 생성합니다.

### Step 4: 무결성 검증 (Self-QC)

- 생성/추출된 오디오 파일들이 디코드 가능한 포맷(MP3/AAC/WAV)인지, 0바이트가 아닌지 검증합니다.
- 파일의 길이가 `analysis.json`에서 요구하는 길이와 오차 범위 내에서 일치하는지 확인합니다.

### Step 5: 결과 기록

- 사용한 MCP, 생성된 파일 목록 및 폴백 발생 여부를 `templates/TASK-REPORT.template.md` 포맷에 따라 작성하고 `PIPELINE-LOG.md`에 기록한 뒤 Editor에게 완료를 보고합니다.

## 관련 파일

| File | Purpose |
|------|---------|
| `02-analyze.md` | 오디오 생성의 기준이 되는 무드/비트 메타데이터 제공 |
| `06-edit-compose.md` | 생성된 오디오 파일들을 합성하는 최종 단계 스킬 |
| `templates/TASK-REPORT.template.md` | 단계 완료 보고서 작성 기준 포맷 |

## 예외사항

1. P2 BGM 생성 3회 실패 시: 더 이상의 지연을 막기 위해 무음(Silence)으로 대치 후 파이프라인을 계속 진행합니다(PIPELINE-LOG에 ⚠️ 기록).
2. 내레이션 생성 실패 시: 자막 처리 모델로 내러티브 전달을 위임하고 오디오 믹싱에서는 제외합니다.
