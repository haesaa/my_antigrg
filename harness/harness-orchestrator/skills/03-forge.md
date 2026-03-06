---
name: harness-03-forge
description: >
  분석 결과를 기반으로 SKILL.md + 번들 리소스를 자동 생성한다(Skill Forge). 복잡도에 따라 simple(단일 SKILL.md)과 composite(Agent Teams 패턴) 두 가지 템플릿으로 분기한다.
---

# 03-forge: 스킬 생성 (Skill Forge)

> **실행자**: Builder (Teammate 2)
> **실행 시점**: 02-analyze 완료 후
> **쓰기 권한**: `work/forge/` 만
> **최대 출력**: SKILL.md 500줄; 초과 시 references/ 분리

## 목적

02-analyze의 MCP 결과 + 시스템 프롬프트를 바탕으로 Antigravity 표준에 맞는 스킬 패키지를 생성한다.
복잡도에 따라 two-tier 템플릿으로 분기한다.

## 실행 시점

- 02-analyze 완료 후 Leader가 Builder를 호출하면 실행.
- "스킬 만들어줘", "자동화 스킬 생성", "새 SKILL.md" 등의 요청이 최종 실행 단계에서 이 부분을 트리거.

## 워크플로우

### Step 1: Intent Extraction

1. 유저 요청에서 추출:
   - 도메인, 트리거 조건(3개 이상), 기대 출력
   - `skill_name` = kebab-case
2. `view_file("../../skill-forge/SKILL.md")` 동적 로딩

### Step 2: Registry Search + Fork

```
find_by_name("SKILL.md", working_dir) — 유사 스킬 탐색
→ 유사 스킬 존재: Fork (기존 구조 기반 수정)
→ 없음: 아래 템플릿에서 시작
```

### Step 3: 복잡도별 생성 분기

#### 3a. Simple 스킬 템플릿

```
{skill-name}/
├── SKILL.md     ← 단일 파일로 충분
└── references/  ← 300줄 초과 시만
```

SKILL.md 필수 구조:

```yaml
---
name: {skill-name}
description: >
  {기능 설명}. {트리거1}, {트리거2}, {트리거3} 등에 활성화됩니다.
---
## 목적
## 실행 시점
## 워크플로우 (Step 1, 2, 3...)
## 관련 파일 (테이블)
## 예외사항
```

#### 3b. Composite/Research 스킬 템플릿 (Agent Teams 패턴)

```
{skill-name}/
├── SKILL.md                  ← 진입점: 팀 구성, 흐름, 전역 룰
├── skills/
│   ├── 00-preflight.md
│   ├── 01-{step}.md
│   ├── ...
│   └── XX-graceful-exit.md
├── templates/
│   ├── PIPELINE-LOG.template.md
│   └── TASK-REPORT.template.md
└── config/                   (MCP 폴백 등 필요 시)
```

생성되는 SKILL.md 필수 포함 항목:

- 팀 구성 (Leader + 팀원 역할)
- 작업 종속성 그래프 (어떤 순서로, 병렬 가능 여부)
- 전역 룰 (보존 정책, 쓰기 격리, 키 보호)
- Graceful Degradation Matrix
- Resume 안내 ("N단계부터 재실행해줘")

### Step 4: 파일 생성

`write_to_file`로 스킬 패키지를 `work/forge/{skill_name}/`에 작성한다.
결과를 `work/forge/forge-result.json`에 기록:

```json
{
  "skill_name": "...",
  "output_dir": "work/forge/{skill_name}",
  "template_used": "simple | composite",
  "files": ["SKILL.md", "skills/00-preflight.md", ...]
}
```

### Step 5: PIPELINE-LOG 기록

```
## T2: 스킬 생성 (Builder)
- 스킬명: {skill_name}
- 템플릿: {simple | composite}
- 파일 수: {N}
- 완료: {시각}
```

## 관련 파일

| File | Purpose |
|------|---------|
| `../../skill-forge/SKILL.md` | 스킬 생성 상세 가이드 |
| `work/analysis/mcp-result.json` | 02-analyze의 MCP 추천 결과 |
| `work/analysis/system-prompt.md` | 02-analyze의 생성 지침 |
| `04-verify.md` | 다음 단계 (Reviewer) |

## 예외사항

1. **파일 생성 실패**: 즉시 에러 기록 → 유저에게 알림 → 05-exit으로 이동
2. **300줄 초과 SKILL.md**: 일부 내용을 `references/detail.md`로 분리하고 SKILL.md에서 참조
3. **Simple 스킬인데 MCP가 필요한 경우**: config/ 폴더를 추가해 mcp-fallback.json만 생성
