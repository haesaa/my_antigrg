---
name: skill_writer
description: Skill Factory Pipeline을 통해 새로운 Skill Blueprint를 작성하고 검증하는 Skill
---

# Skill Skill Writer

entry_instruction

write_blueprint

---

## Guide Rules

> Do not open guide files directly.
> Always read section index first.
> guide <= 300 tokens

**Namespace 충돌 방지** - 아래 파일명은 library 전역 예약어로 사용 금지:

- `writing_style.md`
- `rules_security.md`
식으로 작성할 것

---

## Guides

- blueprint_writing_guide
- validation_rules_guide

---

## Tools

- file_write
- json_validate

---

## Instructions

### write_blueprint

1. 사용자로부터 Skill 요구사항을 입력받는다
2. `skill_blueprint_schema.json`을 참조하여 Blueprint를 작성한다
3. `validate_blueprint.py`를 통해 검증한다
4. 검증 통과 시 `FACTORY/blueprints/`에 저장한다

**Rule**: Blueprint는 반드시 `skill_blueprint_schema.json` 스키마를 따른다.  
**Rule**: LLM은 직접 SKILL.md를 생성하지 않는다. 반드시 Blueprint → Validator → Builder 파이프라인을 통한다.
