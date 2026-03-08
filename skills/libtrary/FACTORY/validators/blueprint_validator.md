# Blueprint Validator

Blueprint를 검증하는 5가지 규칙.  
모든 규칙을 통과해야 Build 단계로 이동한다.

---

## Validation Rules

| # | Rule | Check |
|---|------|-------|
| 1 | **skill_name must be unique** | `skill_registry.json`에 동일한 이름이 없어야 한다 |
| 2 | **entry_instruction must exist** | `blueprint["entry_instruction"]`이 비어있지 않아야 한다 |
| 3 | **guides must exist in guide_graph** | `blueprint["guides"]`가 비어있지 않아야 한다 |
| 4 | **instructions must exist in instruction_graph** | `blueprint["instructions"]`의 각 항목이 등록된 instruction이어야 한다 |
| 5 | **tools must exist in tool_registry** | `blueprint["tools"]`의 각 항목이 tool_registry에 존재해야 한다 |

---

## Validation Flow

```
Blueprint JSON
     ↓
[Rule 1] skill_name unique?  → FAIL → "Skill name must be unique"
     ↓ PASS
[Rule 2] entry_instruction?  → FAIL → "Entry instruction must exist"
     ↓ PASS
[Rule 3] guides?             → FAIL → "Guides must exist"
     ↓ PASS
[Rule 4] instructions valid? → FAIL → "Invalid instruction: {name}"
     ↓ PASS
[Rule 5] tools valid?        → FAIL → "Invalid tool: {name}"
     ↓ PASS
  ✅ VALID → Proceed to Builder
```

---

## Usage

```python
from validate_blueprint import validate_blueprint

is_valid, message = validate_blueprint(blueprint, existing_skills)
if not is_valid:
    raise ValueError(f"Blueprint invalid: {message}")
```
