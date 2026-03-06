---
name: 04-tts-generate
description: >
  S3에서 작성된 TTS 대본(tts_script.json)을 Qwen3 TTS 모델로 로컬 음성 합성하여 씬별 WAV 파일을 생성합니다.
---

# 04-tts-generate: S4 Qwen3 TTS 음성 합성 스킬

> **실행자**: Editor (Teammate 3)
> **실행 시점**: S3 완료 후
> **쓰기 권한**: `work/S4-tts/` 만
> **의존성**: Python, CUDA GPU, `qwen-tts` 패키지

## 목적

S3에서 작성된 TTS 대본(`tts_script.json`)의 각 대사 라인을 **Qwen3 TTS** 모델로 로컬 음성 합성하여, 감정이 실린 고품질 WAV 파일을 생성합니다.

## 사전 요구사항

| 항목 | 요구 스펙 |
|------|-----------|
| Python | 3.10+ |
| GPU | CUDA 호환, VRAM 4GB+ (0.6B 모델) 또는 8GB+ (1.7B 모델) |
| PyTorch | 2.0+ with CUDA |
| qwen-tts | `pip install -U qwen-tts` |
| soundfile | `pip install soundfile` |

## 워크플로우

### Step 1: 환경 검증

- Python 버전 및 CUDA 가용성 확인
- `qwen-tts` 패키지 임포트 테스트
- GPU VRAM 확인 → 4GB 미만이면 경고 후 CPU 폴백 또는 중단

### Step 2: 모델 로드

사용 가능한 모드 3가지 중 하나를 선택합니다:

| 모드 | 모델 | 용도 | VRAM |
|------|------|------|------|
| **CustomVoice** (기본) | `Qwen3-TTS-12Hz-0.6B-CustomVoice` | 사전 정의 스피커 사용 | 4~6GB |
| **VoiceDesign** | `Qwen3-TTS-12Hz-1.7B-VoiceDesign` | 자연어로 목소리 설계 | 6~8GB |
| **VoiceClone** | `Qwen3-TTS-12Hz-1.7B-Base` | 레퍼런스 음성 클론 | 6~8GB |

```python
import torch
from qwen_tts import Qwen3TTSModel

MODEL_ID = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"

model = Qwen3TTSModel.from_pretrained(
    MODEL_ID,
    device_map="cuda:0",
    dtype=torch.bfloat16,
)
```

### Step 3: 대본 순회 및 음성 합성

`tts_script.json`을 로드하여 각 라인별로 WAV 파일을 생성합니다:

```python
import json
import soundfile as sf

with open("work/S3-storyboard/tts_script.json", "r", encoding="utf-8") as f:
    tts_script = json.load(f)

for line in tts_script:
    wavs, sr = model.generate_custom_voice(
        text=line["text"],
        language=line["language"],
        speaker="Vivian",          # 한국어 지원 여성 스피커
        instruct=line["emotion_instruct"],
    )
    
    output_path = f"work/S4-tts/voice_{line['line_id']}.wav"
    sf.write(output_path, wavs[0], sr)
    print(f"[OK] {output_path} ({len(wavs[0])/sr:.1f}s)")
```

### Step 4: VoiceDesign 모드 (대안)

CustomVoice 스피커가 원하는 감정 표현에 한계가 있을 경우, VoiceDesign 모드로 전환합니다:

```python
# VoiceDesign 모델 로드
model_design = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

wavs, sr = model_design.generate_voice_design(
    text=line["text"],
    language=line["language"],
    instruct=line["emotion_instruct"],
    # instruct에 목소리 자체 특성도 포함 가능:
    # "20대 여성, 낮고 허스키한 목소리, 혼란스럽고 약간 떨리는 톤"
)
```

### Step 5: 무결성 검증 (Self-QC)

생성된 모든 WAV 파일에 대해:

1. **파일 존재 및 크기 확인**: 0바이트가 아닌지 검증
2. **디코딩 가능 확인**: `soundfile.read()`로 정상 로드되는지 테스트
3. **길이 합리성 검사**: 텍스트 길이 대비 음성 길이가 합리적인지 (0.5초~60초 범위)
4. **매니페스트 작성**: 생성 결과를 `work/S4-tts/manifest.json`에 기록

```json
{
  "model": "Qwen3-TTS-12Hz-0.6B-CustomVoice",
  "total_lines": 15,
  "success": 15,
  "failed": 0,
  "total_duration_sec": 87.3,
  "files": [
    { "line_id": "line_001", "file": "voice_line_001.wav", "duration_sec": 5.2 }
  ]
}
```

### Step 6: 완료 확인 및 핸드오프

- `manifest.json` 유효성 검증
- `PIPELINE-LOG.md`에 S4 완료 기록 (모델명, 생성 건수, 실패 건수)
- S5(패키징) 단계 활성화

## 지원 스피커 목록 (CustomVoice)

| Speaker | 성별 | 언어 추천 | 설명 |
|---------|------|-----------|------|
| Vivian | 여성 | 중국어/한국어 | 부드럽고 차분한 여성 목소리 |
| Ryan | 남성 | 영어 | 또렷하고 따뜻한 남성 목소리 |
| (추가 스피커는 `model.get_supported_speakers()` 참조) |

## 관련 파일

| File | Purpose |
|------|---------|
| `03-storyboard.md` | TTS 대본 데이터를 제공하는 선행 단계 |
| `05-package.md` | 생성된 음성 파일을 최종 패키징하는 다음 단계 |

## 예외사항

1. GPU 부족/CUDA 미지원: CPU 모드로 폴백을 시도하되, 생성 속도가 매우 느려질 수 있음을 로그에 경고합니다.
2. 특정 라인 생성 실패: 해당 라인을 스킵하고 `manifest.json`에 실패로 기록한 뒤 나머지를 계속 진행합니다.
3. 모델 다운로드 실패: HuggingFace 미러 또는 수동 다운로드 가이드를 유저에게 안내합니다.
4. 한국어 발음 이슈: `language`를 `"Korean"`으로 명시적 지정하고, 영어 혼용 대사의 경우 `"Auto"`로 설정합니다.
