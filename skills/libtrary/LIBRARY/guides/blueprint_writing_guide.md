# Blueprint Writing Guide

> Blueprint를 올바르게 작성하기 위한 핵심 가이드.  
> anti_task_v0.4.md 섹션 3, 4 기반.

---

## 1. Blueprint 작성 원칙

- LLM은 **절대 SKILL.md를 직접 생성하지 않는다**
- 반드시 Blueprint → Validator → Builder 파이프라인을 따른다
- Blueprint는 `skill_blueprint_schema.json`을 준수해야 한다

---

## 2. 필수 필드

| 필드 | 타입 | 설명 | 필수 |
|------|------|------|------|
| `skill_name` | string | 유일한 snake_case 이름 | ✅ |
| `entry_instruction` | string | 최초 실행 instruction | ✅ |
| `guides` | array | 참조 가이드 목록 (1개 이상) | ✅ |
| `instructions` | array | 사용하는 instruction 목록 | 선택 |
| `tools` | array | 의존하는 tool 목록 | 선택 |

---

## 3. skill_name 규칙

- 소문자와 언더스코어만 사용: `^[a-z][a-z0-9_]*$`
- `skill_registry.json`에 이미 존재하는 이름은 사용 불가
- 예시: `kpi_manager`, `data_cleaner`, `report_generator`

---

## 4. 작성 예시

```json
{
  "skill_name": "report_generator",
  "entry_instruction": "generate_report",
  "instructions": ["generate_report", "format_output"],
  "guides": ["reporting_format", "output_rules"],
  "tools": ["python_exec", "file_write"]
}
```

---

## 5. Anti-Pattern (하지 말 것)

❌ SKILL.md를 먼저 생성하는 것  
❌ Validator 없이 Builder 실행  
❌ skill_name에 대문자 포함  
❌ guides를 빈 배열로 두는 것  

**이 외에 필요한 요소들이 있으면 검색해서 붙여오고, 알맞은 섹션에 append한다. must 신뢰할 수 있는 정보여야 한다**
