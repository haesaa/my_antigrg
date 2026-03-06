---
name: 05-package
description: >
  S3 콘티, S4 TTS 음성, SFX 프롬프트를 하나의 패키지로 묶어 output/ 디렉토리에 최종 산출물을 배치합니다.
---

# 05-package: S5 최종 패키징 스킬

> **실행자**: Editor (Teammate 3)
> **실행 시점**: S3 + S4 모두 완료 후
> **쓰기 권한**: `work/S5-package/`, `output/`

## 목적

생성된 콘티(Storyboard), SFX 프롬프트, TTS 음성 파일들을 통합하여 유저가 바로 활용할 수 있는 형태의 **최종 패키지**를 구성합니다.

## 워크플로우

### Step 1: 에셋 수집 및 정리

- `work/S3-storyboard/`에서 콘티, SFX, TTS 대본 JSON 복사
- `work/S4-tts/`에서 생성된 WAV 파일 전체 복사
- 각 파일의 존재 및 무결성 확인

### Step 2: 타임라인 통합

- `storyboard.json`과 `tts_script.json`을 병합하여 `timeline.json` 생성
- 각 씬에 해당하는 음성 파일 경로를 매핑
- 음성 파일의 실제 길이를 반영하여 타임코드 보정

### Step 3: output/ 디렉토리 구성

```
output/
├── storyboard.json          ← 완성된 콘티
├── sfx_prompts.json         ← SFX 프롬프트 모음
├── tts_script.json          ← TTS 대본 원본
├── timeline.json            ← 통합 타임라인
├── voices/                  ← 씬별 TTS 음성 파일
│   ├── voice_line_001.wav
│   ├── voice_line_002.wav
│   └── ...
└── FINAL-REPORT.md          ← 프로젝트 요약 보고서
```

### Step 4: FINAL-REPORT.md 작성

- 프로젝트 ID, 생성 일시
- 스토리 요약
- 총 씬 수, 유효 TTS 라인 수, 총 음성 길이
- 사용된 모델 및 설정값
- SFX 프롬프트 요약

### Step 5: 완료 기록

- `PIPELINE-LOG.md`에 S5 완료 및 산출물 목록 기록
- QC 검증(06) 단계 활성화

## 관련 파일

| File | Purpose |
|------|---------|
| `04-tts-generate.md` | TTS 음성 파일을 제공하는 선행 단계 |
| `06-qc-validate.md` | 패키징된 결과물의 무결성을 검수하는 다음 단계 |

## 예외사항

1. 부분 TTS 실패: 실패한 라인은 대본 텍스트만 남기고 음성은 `(생성 실패)` 표기
2. 빈 SFX: SFX 프롬프트가 없는 씬은 `"sfx_layers": []`로 처리
