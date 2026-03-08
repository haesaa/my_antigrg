# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

**Antigravity Pipeline v5** — crack.wrtn.ai 스토리챗·캐릭터챗용 프롬프트를 10단계로 자동 생성하는 파이프라인.

- 입력: `inputs/concept.md` + `inputs/user_setting.md`
- 출력: `outputs/1~10단계 결과물.md`
- 모델 타겟: `MODEL_TARGET` 환경변수 (기본: `SC25_PC25`)

## skills/ 구조

```
prompts/
├── 01_creation/       Phase 1 — 단계 1,2  (max_tokens: 8000)
├── 02_production/     Phase 2 — 단계 3,5,6,7,8,9  (max_tokens: 6000, 에이전트 .md는 8000)
├── 03_condenser/      Phase 3 — 단계 4,10  (max_tokens: 6000, prompt_condenser.md는 8000)
└── shared/            model_profiles.md · safety_rules.md
```

각 폴더는 `SKILL.md` + `resources/*.md` + `scripts/config.py` 로 구성.

## 실행 순서

```bash
# Phase 1: 세계관·캐릭터
python 01_creation/scripts/config.py --phases 1,2

# Phase 3 (4단계): 축약 — 5~9단계 전 먼저 실행
python 03_condenser/scripts/config.py --phases 4

# Phase 2: 부속품 전체
python 02_production/scripts/config.py --phases 3,5,6,7,8,9

# Phase 3 (10단계): 축약 품질 검증
python 03_condenser/scripts/config.py --phases 10
```

## 환경 설정

`.env.example`을 복사해 `.env` 생성:

```bash
MODEL_TARGET=SC25_PC25   # 기본값, 변경 시 아래 참조
```

### 모델 코드표

| 코드 | 모델명 | 엔진 |
|------|--------|------|
| `HC` | 하이퍼챗 | Opus 4.6 |
| `SC25` | 슈퍼챗 2.5 | Sonnet 4.6 |
| `SC20` | 슈퍼챗 2.0 | Sonnet 4.5 |
| `SC15` | 슈퍼챗 1.5 | Sonnet 4.0 |
| `PC25` | 프로챗 2.5 | Gemini 3.1 Pro |
| `PC20` | 프로챗 2.0 | Gemini 3.0 Pro |
| `PC10` | 프로챗 1.0 | Gemini 2.5 Pro |

## 핵심 아키텍처 규칙

### 문체 레이어 (수정 금지)

- `01_creation/resources/romance_guide.md` — Layer 1, 기법 32개 정의 사전. **읽기전용.**
- `01_creation/resources/world_builder.md` — Layer 2, 기법을 `[코드]`로만 참조. 재정의 금지.

### 변수 규칙

- `{user}` 성별·신분 하드코딩 금지 — 항상 `inputs/user_setting.md`에서 읽어야 함
- `{char}`, `{user}` 변수는 크랙 프롬프트에 그대로 유지
- `CAUTION` 블록은 반드시 **영문**으로 작성

### 글자 수 제한 (하드 리밋)

| 에이전트 | 제한 |
|---------|------|
| `prompt_condenser` | 4,800자 (공백 포함) |
| `keyword_creator` | 키워드당 400자 |
| `scenario_writer` | 시나리오당 900자 |
| `example_dialogue` | 칸당 500자 |
| `play_guide` | 400자 |
| 제목 후보 | 30자 |

### 품질 게이트

- 9단계 품질심사: 80점 이상 PASS, 미만 시 최대 3회 자동 재시도
- 10단계 축약심사: 4,800자 + 필수 9요소 보존 검증

## 참조 파일

| 파일 | 용도 |
|------|------|
| `pipeline_v5_architecture.md` | 전체 설계 원본 문서 |
| `guide_data.json` | v5 메타데이터 (에이전트·출력·글자제한) |
| `guide_korean.json` | 한글 사용설명서 (단계별 상세) |
| `pipeline_schema.json` | v3 레거시 스키마 (읽기전용) |
| `shared/model_profiles.md` | 모델별 최적화 규칙 |

## 언어 규칙 (GEMINI.md 준용)

- 복잡한 추론은 영어로 내부 처리
- 사용자 출력은 한국어
- 기술 용어: `한국어(English)` 병기 형식 유지
