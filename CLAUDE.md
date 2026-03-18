# CLAUDE.md — sae__haha 저장소 가이드

> 이 파일은 Claude Code AI가 저장소 전체 구조와 작업 규칙을 이해하기 위한 기준 문서입니다.

---

## 저장소 개요

이 저장소는 두 개의 독립적이지만 연관된 AI 시스템으로 구성됩니다:

| 시스템 | 경로 | 버전 | 목적 |
|--------|------|------|------|
| **Harness Skills** | `harness/` | v3 (Agent Teams) | 자동 스킬 생성 오케스트레이션 파이프라인 |
| **Prompts Pipeline** | `prompts_claude/` | v5 (3-Phase) | crack.wrtn.ai용 스토리챗·캐릭터챗 프롬프트 자동 생성 |
| **검증 스킬 러너** | `verify-implementation/` | — | 등록된 verify-* 스킬 일괄 실행 + 통합 보고 |

---

## 디렉토리 구조

```
sae__haha/
├── CLAUDE.md                        ← 이 파일 (루트 가이드)
├── .gitignore
├── harness/                         ← Harness Skills v3
│   ├── CLAUDE.md                    ← 하네스 전용 가이드
│   ├── harness-orchestrator/        ← 파이프라인 메인 런너 (Leader)
│   │   ├── SKILL.md
│   │   ├── skills/                  ← 6개 파이프라인 스테이지
│   │   │   ├── 00-preflight.md
│   │   │   ├── 01-complexity.md
│   │   │   ├── 02-analyze.md
│   │   │   ├── 03-forge.md
│   │   │   ├── 04-verify.md
│   │   │   └── 05-graceful-exit.md
│   │   ├── references/              ← 세부 가이드 (tot-guide.md 등)
│   │   └── templates/               ← PIPELINE-LOG, FINAL-REPORT 등
│   ├── token-guard/                 ← 토큰 추적 + 체크포인트 관리
│   ├── mcp-router/                  ← MCP 서버 추천 (2596개 카탈로그)
│   ├── instruction-gen/             ← system prompt 생성
│   ├── skill-forge/                 ← SKILL.md 자동 생성
│   ├── verification-layer/          ← 3단계 품질 검증
│   ├── references/                  ← interface-spec.md 등
│   ├── tests/                       ← E2E 테스트 시나리오
│   └── Awesome-MCP-Servers-한국어-가이드.md  ← 2596개 MCP 카탈로그
├── prompts_claude/                  ← Prompts Pipeline v5
│   ├── CLAUDE.md                    ← 프롬프트 파이프라인 전용 가이드
│   ├── 01_creation/                 ← Phase 1: 세계관·캐릭터 생성
│   │   ├── SKILL.md
│   │   ├── resources/               ← world_builder.md, personality_designer.md, romance_guide.md
│   │   └── scripts/config.py
│   ├── 02_production/               ← Phase 2: 부속품 생성
│   │   ├── SKILL.md
│   │   ├── resources/               ← 6개 에이전트 지침
│   │   └── scripts/config.py
│   ├── 03_condenser/                ← Phase 3: 축약 + 품질 심사
│   │   ├── SKILL.md
│   │   ├── resources/               ← prompt_condenser.md, condenser_reviewer.md
│   │   ├── scripts/config.py
│   │   └── outputs/                 ← 모든 파이프라인 산출물 (1~10단계)
│   │       ├── 1_full_prompt.md
│   │       ├── 2_personality_prompt.md
│   │       ├── 4_condensed_prompt.md   ← 실제 크랙 삽입용 (≤4,800자)
│   │       ├── 5_keyword_books.md
│   │       ├── 6_opening_scenario.md
│   │       ├── 7_example_dialogue.md
│   │       ├── 8_play_guide.md
│   │       └── 10_condenser_review.md
│   ├── shared/                      ← model_profiles.md, safety_rules.md
│   ├── pipeline_schema.json         ← v3 레거시 스키마 (읽기전용)
│   ├── guide_data.json              ← v5 메타데이터
│   └── guide_korean.json            ← 한글 사용설명서
└── verify-implementation/
    └── SKILL.md                     ← verify-* 스킬 일괄 실행기
```

---

## 시스템 1: Harness Skills v3

### 아키텍처

6단계 파이프라인을 4인 팀(Leader / Analyst / Builder / Reviewer)이 실행합니다.

```
유저 요청
  → 00-preflight   (Leader)   환경 초기화, 보안 스캔, Resume 판정
  → 01-complexity  (Leader)   복잡도 판정, ToT 3분기 생성, ToC 채점
  → 02-analyze     (Analyst)  MCP Router + Instruction Generator
  → 03-forge       (Builder)  Skill Forge (SKILL.md + 번들 생성)
  → 04-verify      (Reviewer) Schema / Functional / Quality 3단계 검증
  → 05-exit        (Leader)   최종 보고, Graceful Degradation
```

### 스킬 목록

| 스킬 | 진입 역할 | 핵심 기능 |
|------|----------|---------|
| `harness-orchestrator` | Leader | 파이프라인 메인 런너, 복잡도 판정, ToT/ToC |
| `token-guard` | Leader 참조 | 토큰 추적 (80%/90%/95% 임계점), 체크포인트 |
| `mcp-router` | Analyst | MCP 서버 매칭 → `mcp-result.json` |
| `instruction-gen` | Analyst | system prompt 조합 → `system-prompt.md` |
| `skill-forge` | Builder | SKILL.md + 번들 생성 → `forge-result.json` |
| `verification-layer` | Reviewer | 3단계 검증 + auto-fix → `verify-report.json` |

### 토큰 임계점

| 단계 | 토큰 | 동작 |
|------|------|------|
| ⚠️ 경고 | 80% (8,000) | 게이지 표시, 우선순위 조정 |
| 🔶 강제 저장 | 90% (9,000) | checkpoint.json + CHECKPOINT.md 자동 저장 |
| 🔴 즉시 중단 | 95% (9,500) | 중단 → 저장 → 다음 세션 Resume |

**토큰 자기 추정 공식 (외부 API 없음):**
- 한국어: 1자 ≈ 2~3 토큰
- 영어: 1단어 ≈ 1.3 토큰
- 코드: 1줄 ≈ 10~15 토큰
- 마크다운: 1줄 ≈ 8~12 토큰

### ToT/ToC/Reflection 프레임워크

**ToT (Tree-of-Thought):** 단일 프롬프트에서 A/B/C 3분기 동시 생성 (API 추가 호출 없음)

**ToC 채점 공식:**
```
Score = Feasibility(0.40) + Quality(0.35) + TokenEfficiency(0.25)
토큰 효율 역산: 1,000토큰=10점, 8,000토큰=1점
```

**Reflection:**
- simple → Skip
- composite → 인라인 자기 검토
- research → verification-layer 별도 호출

### Graceful Degradation 매트릭스

| 실패 지점 | 저장 산출물 | 상태 |
|---------|-----------|------|
| 01-complexity 실패 | 복잡도 분석 | 🔴 FAIL |
| 02-analyze 실패 | MCP 목록 + 기본 지침 | ⚠️ PARTIAL |
| 03-forge 실패 | 분석 + 프롬프트 텍스트 | ⚠️ PARTIAL |
| 04-verify 2회 실패 | 미검증 스킬 (경고 라벨) | ⚠️ PARTIAL |
| 토큰 80% 도달 | checkpoint.json + 현재 최선 결과 | 🟡 PAUSE |

### 핵심 제약

- **외부 API 절대 금지** — Antigravity + 로컬 도구만 사용
- **MAX_TOKENS: 10,000** (세션 하드 리밋)
- **SKILL.md ≤500줄** (초과 시 `references/`로 분리)
- **보안 스캔**: "ignore previous", "system prompt" 등 인젝션 패턴 탐지
- **Auto-fix**: 크리티컬 이슈만, 최대 2회 반복

---

## 시스템 2: Prompts Pipeline v5

### 실행 순서

```bash
# Phase 1: 세계관·캐릭터 (먼저 실행)
python 01_creation/scripts/config.py --phases 1,2

# Phase 3 Step 4: 축약 (Phase 2 전에 반드시 실행)
python 03_condenser/scripts/config.py --phases 4

# Phase 2: 부속품 전체
python 02_production/scripts/config.py --phases 3,5,6,7,8,9

# Phase 3 Step 10: 축약 품질 심사
python 03_condenser/scripts/config.py --phases 10
```

### 10단계 파이프라인

| 단계 | 에이전트 | 산출물 | 제한 |
|------|---------|--------|------|
| 1 | `world_builder` | `1_full_prompt.md` | 8,000 토큰 |
| 2 | `personality_designer` | `2_personality_prompt.md` | 8,000 토큰 |
| 3 | `visual_designer` | `3_visual_prompts.md` | 6,000 토큰 |
| **4** | **`prompt_condenser`** | **`4_condensed_prompt.md`** | **≤4,800자** |
| 5 | `keyword_creator` | `5_keyword_books.md` | 키워드당 400자 |
| 6 | `scenario_writer` | `6_opening_scenario.md` | 시나리오당 900자 |
| 7 | `example_dialogue` | `7_example_dialogue.md` | 칸당 500자 |
| 8 | `play_guide` | `8_play_guide.md` | 400자 |
| 9 | `quality_reviewer` | `9_review.md` | 80점↑ PASS, 최대 3회 재시도 |
| 10 | `condenser_reviewer` | `10_condenser_review.md` | 필수 9요소 보존 검증 |

**모든 산출물 위치:** `prompts_claude/03_condenser/outputs/`

### 글자 수 하드 리밋 (공백 포함)

| 산출물 | 제한 | 위반 시 |
|--------|------|--------|
| `4_condensed_prompt.md` | **4,800자** | 재압축 (최대 3회) |
| 키워드 1개 | 400자 | 항목 축약 |
| 시나리오 1개 | 900자 | 씬 압축 |
| 예시대화 1칸 | 500자 | 대사 정리 |
| 플레이가이드 | 400자 | 내용 축약 |
| 제목 후보 | 30자 | 단어 정리 |

### 문체 레이어 시스템 (수정 금지)

| 레이어 | 파일 | 규칙 |
|--------|------|------|
| **Layer 1** | `01_creation/resources/romance_guide.md` | **읽기 전용.** 32개 기법 정의 사전. 절대 수정·재정의 금지. |
| **Layer 2** | `01_creation/resources/world_builder.md` | `[코드]`로만 Layer 1 기법 참조. 재정의 금지. |

### 장르별 문체 프리셋

| 장르 | 비율(대화/행동/내면) | 뼈대 기법 |
|------|-------------------|---------|
| romance | 50/25/25 | `[SDT]` + `[FID]` |
| BL | 45/25/30 | `[FID]` + `[SIL]` |
| fantasy/무협 | 40/35/25 | `[OMIT]` + `[PATH]` |
| 일상물 | 55/25/20 | `[SDT]` + `[PATH]` |
| 스릴러 | 35/45/20 | `[ICE]` + `[SIL]` |
| 서바이벌 | 30/50/20 | `[IMR]` + `[SEN]` |
| 시뮬레이션 | 45/35/20 | `[IMR]` + `[DRP]` |

### 모델 타겟 코드

| 코드 | 모델명 | 엔진 | 특이사항 |
|------|--------|------|--------|
| `HC` | 하이퍼챗 | Opus 4.6 | 출력량↓, 예시 1.5배, 최소 4문단 |
| `SC25` | 슈퍼챗 2.5 | Sonnet 4.6 | 프롬프트 문구 직접 출력 방지 |
| `SC20` | 슈퍼챗 2.0 | Sonnet 4.5 | SC25와 유사 |
| `SC15` | 슈퍼챗 1.5 | Sonnet 4.0 | 긍정편향 방지 2배 강화 |
| `PC25` | 프로챗 2.5 | Gemini 3.1 Pro | 유저 사칭 방지 3중 |
| `PC20` | 프로챗 2.0 | Gemini 3.0 Pro | PC25 동일 적용 |
| `PC10` | 프로챗 1.0 | Gemini 2.5 Pro | 유저 사칭 방지 3중 |
| `SC25_PC25` | 기본값 | 두 모델 동시 호환 | 기본 타겟 |

**환경변수 설정:**
```bash
MODEL_TARGET=SC25_PC25   # 기본값
MODEL_TARGET=HC_ONLY     # 프리미엄 작품
MODEL_TARGET=PC10_SC15   # 레거시
```

### 압축 규칙 (Step 4 축약 시)

| 허용 | 금지 |
|------|------|
| 영어 약어 (Spell, Conflict, Depth, Speech, Relations, BG, Trait) | 캐릭터 이름·별명 영문화 |
| 기호 (→ ↔ = \| # w/ + ★ ↑ ↓ ~ &) | 지명·조직명 영문화 |
| 숫자 축약 (29M=29세남성, 24F=24세여성) | 상태창·info 항목명 영문화 |
| 한자 (동양풍 원작 술법명·지명) | 장르 특수 용어 로마자 표기 |

### 필수 변수 규칙

- **`{user}`** — 성별·신분 하드코딩 절대 금지. 항상 `inputs/user_setting.md`에서 읽어야 함.
- **`{char}`** — 캐릭터 수 하드코딩 금지. 입력에서 읽어야 함.
- **CAUTION 블록** — 반드시 **영문**으로 작성.
- **MBTI·성격유형 메타정보** — 내러티브에 직접 출력 금지.

### 현재 작업 중인 프로젝트

`prompts_claude/03_condenser/outputs/`에 현재 저장된 산출물:

- **작품:** 로맨틱코미디 — 초저예산 웹드라마 현장 《피의 온도》
- **장르:** 로맨틱코미디 (개그 7 : 로맨스 3), 극중극 구조
- **버전:** 세이프 + 언세이프 양버전
- **공략 캐릭터:** 강도윤(28M, 뱀파이어 남주 역 배우), 차율(32M, 감독), 한재우(26M, 동료 배우)

---

## 시스템 3: verify-implementation

`verify-*` 이름의 스킬을 자동으로 찾아 순차 실행하고 통합 보고서를 생성합니다.

**실행 시점:**
- 새 기능 구현 후
- PR 생성 전
- 코드 리뷰 중

**현재 등록된 verify 스킬:**

| # | 스킬 | 설명 |
|---|------|------|
| 1 | `verify-outomidea-pipeline` | Outomidea V4 파이프라인 정합성 검증 |

---

## 파일·디렉토리 네이밍 컨벤션

### SKILL.md 표준 구조

```markdown
---
name: {kebab-case-name}
description: >
  {기능 1~2줄}. {활성화 트리거}.
version: {semantic}
author: {작성자}
tags: [tag1, tag2]
---

## 인터페이스 / Interface
## 목적 / Purpose
## 실행 시점 / When to Execute
## 워크플로우 / Workflow
  ### Step 1: ...
  ### Step 2: ...
## 관련 파일 / Related Files
## 예외사항 / Exceptions
```

### 파일 네이밍 패턴

| 패턴 | 용도 | 예시 |
|------|------|------|
| `SKILL.md` | 스킬·에이전트 정의 | `harness/token-guard/SKILL.md` |
| `CLAUDE.md` | AI 가이드 문서 | `/CLAUDE.md`, `/harness/CLAUDE.md` |
| `{N}_{description}.md` | 파이프라인 산출물 | `1_full_prompt.md`, `4_condensed_prompt.md` |
| `{NN}-{stage}.md` | 오케스트레이터 스테이지 | `00-preflight.md`, `03-forge.md` |
| `checkpoint.json` | 재개 상태 (기계) | — |
| `CHECKPOINT.md` | 재개 상태 (인간) | — |

### JSON 스키마 패턴

```json
{
  "schema_version": "1.0",
  "status": "pass | fail | partial",
  "timestamp": "ISO-8601"
}
```

**모듈 간 교환 파일 (I1~I7):**

| 파일 | 생성 | 소비 |
|------|------|------|
| `checkpoint.json` | 01-complexity / token-guard | 00-preflight (resume) |
| `mcp-result.json` | mcp-router | 03-forge |
| `system-prompt.md` | instruction-gen | 03-forge |
| `forge-result.json` | skill-forge | 04-verify |
| `verify-report.json` | verification-layer | 05-exit |

---

## 언어 규칙

- **복잡한 추론**: 영어로 내부 처리
- **사용자 출력**: 한국어
- **기술 용어 병기**: `한국어(English)` 형식
- **CAUTION 블록**: 영문 전용 (혼용 금지)
- **SKILL.md 기법 지시문**: 줄당 ≤100자

---

## 작업 시 주의사항

### 절대 금지

1. `romance_guide.md` (Layer 1) 수정 또는 기법 재정의
2. `{user}` 성별·신분·외형 하드코딩
3. `pipeline_schema.json` 수정 (v3 레거시, 읽기전용)
4. 외부 API 호출 (harness 시스템 내에서)
5. 4,800자 초과 상태로 `4_condensed_prompt.md` 저장
6. CAUTION 블록 한국어 혼용

### 파이프라인 의존성 순서

```
01_creation → 03_condenser(step4) → 02_production → 03_condenser(step10)
```

Step 4 완료 전에 02_production을 실행하면 안 됩니다.

### 품질 게이트

- **Step 9 품질심사**: 80점 미만 → 자동 재시도 (최대 3회)
- **Step 10 축약심사**: 4,800자 + 필수 9요소 보존 검증
- **harness verify**: Schema → Functional → Quality (자동 수정 최대 2회)

---

## 개발 워크플로우

### 새 작품 프롬프트 생성 시

1. `inputs/concept.md` + `inputs/user_setting.md` 작성
2. `python 01_creation/scripts/config.py --phases 1,2` 실행
3. `python 03_condenser/scripts/config.py --phases 4` 실행
4. `python 02_production/scripts/config.py --phases 3,5,6,7,8,9` 실행
5. `python 03_condenser/scripts/config.py --phases 10` 실행
6. `prompts_claude/03_condenser/outputs/4_condensed_prompt.md` → crack.wrtn.ai 삽입

### 새 하네스 스킬 생성 시

1. 유저 요청을 `harness-orchestrator`에 전달
2. 파이프라인이 자동으로 00→01→02→03→04→05 실행
3. `harness/output/{skill-name}/` 디렉토리에 결과 저장
4. 검증 실패 시 `verify-implementation` 스킬로 재검토

### 현재 브랜치

작업 브랜치: `claude/bl-romcom-game-design-kQUdQ`

---

## 참조 파일 색인

| 파일 | 위치 | 용도 |
|------|------|------|
| `romance_guide.md` | `prompts_claude/01_creation/resources/` | 32개 기법 사전 (Layer 1, 읽기전용) |
| `model_profiles.md` | `prompts_claude/shared/` | 모델별 최적화 규칙 |
| `safety_rules.md` | `prompts_claude/shared/` | 전 에이전트 공통 안전장치 |
| `tot-guide.md` | `harness/harness-orchestrator/references/` | ToT/ToC/Reflection 상세 가이드 |
| `interface-spec.md` | `harness/references/` | 모듈 간 인터페이스 스키마 (I1-I7) |
| `checkpoint-schema.md` | `harness/token-guard/references/` | 체크포인트 JSON 포맷 |
| `Awesome-MCP-Servers-한국어-가이드.md` | `harness/` | 2596개 MCP 서버 카탈로그 |
| `guide_korean.json` | `prompts_claude/` | 파이프라인 한글 사용설명서 |
| `pipeline_schema.json` | `prompts_claude/` | v3 레거시 스키마 (읽기전용) |
