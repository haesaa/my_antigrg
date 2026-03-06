---
name: harness-01-complexity
description: >
  유저 요청을 분석하여 복잡도(simple/composite/research)를 판정하고, composite 이상에 대해 ToT 3분기와 ToC 채점으로 최적 실행 전략을 선택한다.
---

# 01-complexity: 복잡도 판정 + ToT 분기

> **실행자**: Leader (직접 실행)
> **실행 시점**: 00-preflight 통과 후
> **쓰기 권한**: checkpoint.json, PIPELINE-LOG.md

## 목적

유저 요청의 복잡도를 세 단계로 분류하여 이후 파이프라인 실행 경로를 결정한다.

- **simple**: ToT 스킵 → 03-forge 직행
- **composite/research**: ToT 3분기 + ToC 채점으로 최적 전략 선택

## 실행 시점

- 00-preflight 완료 후 항상 실행.
- 유저 요청에서 도메인 수, 연동 키워드, 탐색 키워드를 분석해야 할 때.

## 워크플로우

### Step 1: 키워드 추출 및 도메인 카운트

도메인 분류:

```
code        = 코드, 스크립트, 함수, 클래스, API, 프레임워크
analysis    = 분석, 데이터, 통계, 리포트, 시각화
writing     = 문서, 글, 번역, 요약
integration = MCP, Slack, Gmail, GitHub, 연동, 외부
skill       = 스킬, SKILL.md, 자동화
```

### Step 2: 복잡도 분류

```
IF 도메인 1개 AND 출력이 명확:          → simple
ELSE IF 도메인 2개+ OR "연동" 포함:     → composite
ELSE IF "어떻게", "방법", "비교", "탐색": → research
```

| 분류 | 후속 흐름 |
|------|----------|
| **simple** | ToT 스킵 → 02-analyze를 거쳐 03-forge 직행 |
| **composite** | ToT 3분기 실행 → Branch 선택 → 02-analyze → 03-forge |
| **research** | ToT 3분기 실행 → Branch 선택 → 02-analyze → 03-forge |

### Step 3: ToT 3분기 생성 (composite/research만)

`references/tot-guide.md`를 읽어 아래 프레임워크로 인라인 ToT를 수행한다:

```markdown
### 사고 분기 A — [전략명]
핵심 아이디어: ...
장점: ...  / 단점: ...
예상 토큰: ~X

### 사고 분기 B — [전략명]
...

### 사고 분기 C — [전략명]
...
```

### Step 4: ToC 채점 및 확정

```
총점 = 실현가능성 × 0.40 + 품질 × 0.35 + 토큰효율 × 0.25

| 분기 | 실현 | 품질 | 비용 | 총점 |
|------|------|------|------|------|
|  A   | ?/10 | ?/10 | ?/10 | ?.?? |
|  B   |  ... |  ... |  ... |  ... |
|  C   |  ... |  ... |  ... |  ... |

→ 선택: Branch {X} (총점 {Y}점)
→ 사유: {1줄}
```

**예외**: 전 분기 5점 미만이면 유저에게 요청을 좁혀달라고 안내 후 중단.

### Step 5: 결과 기록

- checkpoint.json의 `complexity` 필드 업데이트
- PIPELINE-LOG.md에 `## 복잡도 판정` 섹션 append

## 관련 파일

| File | Purpose |
|------|---------|
| `references/tot-guide.md` | ToT/ToC/Reflection 상세 프레임워크 |
| `checkpoint.json` | 복잡도 결과 저장 |
| `02-analyze.md` | 다음 단계 (Analyst 팀원 실행) |

## 예외사항

1. **simple 태스크에 ToT 강제 요청**: 불필요. Step 3/4를 스킵하고 Step 5로 바로 이동
2. **동점 발생**: 토큰 효율이 높은 분기 선택
