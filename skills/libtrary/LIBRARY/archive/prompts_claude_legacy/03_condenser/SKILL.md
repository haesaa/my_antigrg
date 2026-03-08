---
name: 03_condenser
description: "크랙 프롬프트 파이프라인 Phase 3 — 축약 + 축약 품질심사. 4단계(축약기)+10단계(축약QA). 1·2단계 산출물을 4,800자 이내로 압축 후 손실 여부를 검증한다."
version: 5.0.0
author: Antigravity
tags: [crack, phase4, phase10, condenser, compression, qa]
---

# Phase 3: Condenser — 실행기 (Executor)

> **이 파일은 AI 에이전트 실행 지침서입니다.**  
> SKILL.md를 읽은 에이전트는 아래 프로토콜에 따라 4단계 → 10단계를 순서대로 실행합니다.

---

## 1. 사전 조건 (Pre-flight Check)

이 스킬을 실행하기 전에 반드시 확인:

| 체크 | 파일 | 상태 확인 방법 |
|------|------|--------------|
| ✅ | `outputs/1_full_prompt.md` | 파일 존재 + 비어있지 않음 |
| ✅ | `outputs/2_personality_prompt.md` | 파일 존재 + 비어있지 않음 |

> **위 두 파일이 없으면 실행 중단.** `01_creation` 스킬을 먼저 완료하세요.

---

## 2. 에이전트 목록

| 단계 | ID | 에이전트 파일 | 산출물 | 글자제한 |
|------|----|-------------|--------|---------|
| **4** | `prompt_condenser` | `resources/prompt_condenser.md` | `outputs/4_condensed_prompt.md` | **≤4,800자** (공백 포함) |
| **10** | `condenser_reviewer` | `resources/condenser_reviewer.md` | `outputs/10_condenser_review.md` | — |

---

## 3. 실행 프로토콜

### STEP 4 — 프롬프트 축약기 (prompt_condenser)

**에이전트 로드**: `resources/prompt_condenser.md`를 읽어 역할·규칙·출력 형식을 이해한다.

**입력 읽기**:

1. `outputs/1_full_prompt.md` — 세계관 + 캐릭터 전체 프롬프트
2. `outputs/2_personality_prompt.md` — 성격유형 통합 프롬프트

**실행 지침**:

- 두 입력을 통합하여 **4,800자 이내(공백 포함)**로 압축
- 출력 섹션 순서 고정: `<world>` → `<user_setting>` → `<characters>` → `<relations>` → `<writing>` → `<caution>` → `<rules>` → `<status_format>` → `<opening>`
- MODEL_TARGET 확인 → `shared/model_profiles.md`의 해당 모델 방어구문 삽입

**출력 직후 셀프체크** (압축 완료 후 즉시 실행):

```
1. 총 글자 수(공백 포함) 카운트 → 4,800자 초과 시 재압축
2. MUST PRESERVE 9개 항목 체크리스트 대조
3. {char}, {user} 변수 정상 여부 확인
4. 한국어 유지 대상(고유명사·상태창·info 항목) 영문화 여부 확인
5. 상태창 포맷 유지 확인
```

**FAIL 처리**: 4,800자 초과 시 → 재압축. 최대 3회. 3회 후에도 초과 시 경고 메시지 포함 저장.

**저장**: `outputs/4_condensed_prompt.md`

---

### STEP 10 — 축약 품질 심사관 (condenser_reviewer)

> **4단계 완료 후에만 실행** (4_condensed_prompt.md 파일 존재 확인)

**에이전트 로드**: `resources/condenser_reviewer.md`를 읽어 채점 기준·출력 형식을 이해한다.

**입력 읽기**:

1. `outputs/4_condensed_prompt.md` — 검증 대상
2. `outputs/1_full_prompt.md` — 원본 비교용
3. `outputs/2_personality_prompt.md` — 원본 비교용

**채점표**:

| 항목 | 배점 | 기준 |
|------|------|------|
| 글자 수 | 20 | ≤4,800자 달성 (미달 시 0점) |
| 필수 9요소 보존 | 30 | Depth/Speech/성격유형/Relations/Writing/CAUTION/상태창/사칭방지/Opening |
| 한국어 유지 | 15 | 고유명사·상태창·info 항목 한국어 유지 |
| CAUTION 영문 | 10 | 영문 금제 블록 존재+완전성 |
| 크랙 호환성 | 15 | {char}/{user} 변수 정상, 마크다운 포맷, 바로 붙여넣기 가능 |
| 모델 방어구문 | 10 | MODEL_TARGET에 맞는 모델별 방어구문 존재 |

**판정**:

- **80점 이상** → PASS. 검증 완료.
- **80점 미만** → 개선점 명시. "재축약 필요: [항목명]" 형식으로 출력.

**출력 형식**: `resources/condenser_reviewer.md`의 OUTPUT FORMAT 그대로 사용.

**저장**: `outputs/10_condenser_review.md`

---

## 4. 개별 단계 실행

두 단계를 따로 실행해야 할 경우:

```bash
# 4단계만 실행 (축약)
python scripts/config.py --phases 4

# 10단계만 실행 (검증) — 4_condensed_prompt.md 존재 필요
python scripts/config.py --phases 10

# 두 단계 연속 실행
python scripts/config.py --phases 4,10
```

---

## 5. 압축 규칙 요약

| 허용 | 금지 |
|------|------|
| 영어 약어 (Spell, Conflict, Depth, Speech, Relations, BG, Trait) | 캐릭터 이름·별명 영문화 |
| 기호 (→, ↔, =, \|, #, w/, +, ★, ↑, ↓, ~, &) | 지명·조직명 영문화 |
| 숫자 축약 (29M=29세남성, 24F=24세여성) | 상태창/info 항목명 영문화 |
| 동양풍: 중국어 한자 (원작 술법명·지명) | 장르 특수 용어 로마자 표기 |
| 현대물: 영문 브랜드명·외래어 | — |
| SF: 영문 기술 용어 | — |

---

## 6. 의존성 맵

```
inputs/concept.md ──→ [01_creation] ──→ outputs/1_full_prompt.md
                                    └──→ outputs/2_personality_prompt.md
                                              │
                                              ▼
                                      [03_condenser STEP 4]
                                              │
                                              ▼
                                   outputs/4_condensed_prompt.md
                                              │
                            ┌─────────────────┘
                            │
                            ▼
                    [02_production] (5·6·7·8단계 입력으로 사용)
                            │
                            ▼
                    [03_condenser STEP 10] ──→ outputs/10_condenser_review.md
```

---

## 7. 공유 리소스

| 파일 | 용도 |
|------|------|
| `shared/model_profiles.md` | MODEL_TARGET별 방어구문·최적화 규칙 |
| `shared/safety_rules.md` | 전 에이전트 공통 안전장치 |

**MODEL_TARGET 변경** (기본: `SC25_PC25`):

```bash
MODEL_TARGET=HC_ONLY python scripts/config.py --phases 4,10
```

---

## 8. 제약 (Hard Limits)

| 항목 | 값 |
|------|-----|
| max_tokens (에이전트 입력) | 6,000 (prompt_condenser: 8,000) |
| 출력 글자 수 상한 | 4,800자 (공백 포함, 엄격 적용) |
| 품질 기준 | 80점 이상 PASS |
| 최대 재시도 | 3회 |
| 의존 완료 조건 | 01_creation 산출물 존재 필수 |
