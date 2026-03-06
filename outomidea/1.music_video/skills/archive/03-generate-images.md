---
name: 03-generate-images
description: >
  T1 분석 결과를 기반으로 장면별 키프레임 이미지를 생성합니다. T1 완료 후 T2 단계에서 자동 활성화됩니다.
---

# 03-generate-images: T2 이미지 생성 스킬

> **실행자**: Creator (Teammate 2)
> **실행 시점**: T1 완료 후
> **쓰기 권한**: `work/T2-images/` 만
> **MCP 폴백**: Pixelle(ComfyUI) → comfy-pilot → Fal(FLUX) → Replicate

## 목적

T1에서 생성한 장면 구조, 프롬프트, 그리고 캐릭터 메타데이터를 결합해 키프레임용 이미지를 생성합니다.
유료 API를 금하고 무료 tier 중심의 MCP를 활용해 고품질 캐릭터 일관성을 유지하는 것이 최우선 목적입니다.

## 실행 시점

- 02-analyze (T1) 단계가 성공적으로 완료되고 데이터가 `work/T1-analysis`에 준비된 경우 활성화됩니다.
- 모션 비디오 작업을 진행하기 위한 고품질 키프레임들(시퀀스 컷)을 뽑아낼 때 사용합니다.

## 워크플로우

### Step 1: 생성 전략(Mode) 결정

- 분석된 메타데이터를 기반으로 최적화된 생성 모드를 설정합니다.
  - P2 (Scene): 원본 3x3 컷이 있으므로 **img2img** 베이스 + IP-Adapter 사용
  - P1 (MV): 이미지 레퍼런스가 제한적이므로 **txt2img** + IP-Adapter 사용
  - P3 (Animation): **ControlNet** 스피드/모션 전이제어 + 이미지 변환

### Step 2: 캐릭터 참조 이미지 병합

- `character-profiles` JSON을 순회하여 현재 Scene 컷에 등장하는 앵글별 레퍼런스 얼굴 이미지를 지정합니다.
- 토큰 낭비를 막기 위해 가장 적합한 단 **1장만**을 Reference/IP-Adapter용 이미지 인코딩에 첨부합니다.

### Step 3: Plan Approval (테스트 검증)

- 첫 번째 Scene의 이미지만 1건(Test Run) 생성합니다.
- 해상도, 캐릭터 유사도, 구도 유사도, 의상 정확성 여부를 자동 검사하고 반려 시 denoising 보정 후 재생성합니다.
- 위 검사를 통과한 경우에만 나머지 리스트 일괄 세팅(Batch Approval)을 전파합니다.

### Step 4: 장면별 일괄 생성 실행

- 승인된 가중치를 기준으로 n개의 나머지 씬(Scene)들에 대해 생성 명령을 MCP로 일괄/순차 송달합니다.
- 이때 의상 변경 로직 시점(Time Flow)에 맞게 프롬프트 블록을 교체해야 합니다.

### Step 5: 최종 일관성 셀프 체크 (Self-QC)

- 생성 완료된 전체 폴더(`T2-images`)를 순회하면서 캐릭터 얼굴의 워핑 유무, 장면 간 의상 매칭 오류를 교차 검증합니다.
- 일치하지 않는 소수 이미지에 대해서만 개별 핀포인트 재실행(Fix)을 트리거합니다.

## 관련 파일

| File | Purpose |
|------|---------|
| `02-analyze.md` | 키프레임 생성을 위한 프롬프트/가이드라인 참조 구조 제공 |
| `character-profiles/*.json` | 캐릭터의 의상과 얼굴 속성 검증 메타 참조 모델 |
| `04-generate-motion.md` | (다음 단계) 생성된 이미지를 바탕으로 비디오를 트리거하는 스킬 |

## 예외사항

1. Plan Approval 연속 실패 (3회 이상): Denoising이나 Controlnet 강도 문제를 무시하고 최대한 완화된 강도로 Fallback 생성 후 진행(Ken Burns 대비).
2. MCP 할당량 소진 방어: 가장 안정적인 오픈소스(ex. Pixelle) 로컬 모델을 1순위로 시도하고 이후 순차적인 폴백을 강제합니다.
