# Skill Builder

Blueprint가 Validator를 통과한 후, 실제 Skill 파일을 생성한다.  
anti_task_v0.4.md 섹션 6, 7 기반.

---

## Builder Tasks

| # | Task | Description |
|---|------|-------------|
| 1 | `setup_factory_structure(root_path)` | FACTORY/LIBRARY 기본 폴더 생성 |
| 2 | `build_skill(root_path, blueprint)` | skill 디렉토리 및 `SKILL.md` 생성 |
| 3 | `register_skill(registry_path, blueprint)` | `skill_registry.json`에 skill 등록 |

---

## Builder Flow

```
Validated Blueprint
       ↓
[1] setup_factory_structure  →  FACTORY/, LIBRARY/ 폴더 보장
       ↓
[2] build_skill              →  skills/{skill_name}/SKILL.md 생성
       ↓
[3] register_skill           →  skill_registry.json 업데이트
       ↓
    ✅ Build Complete
```

---

## Generated SKILL.md Structure

```markdown
# Skill {Skill Name}

entry_instruction

{entry_instruction_value}
```

---

## Safety Rules

- Builder는 반드시 **검증된 Blueprint**만 처리한다.
- 실제 테스트는 `tmp_path` 격리 환경에서 진행한다 (`pytest`의 `tmp_path` fixture 사용).
- 기존에 존재하는 skill 폴더는 덮어쓰지 않는다 (`exist_ok=True`).

---

## Usage

```python
from skill_builder import setup_factory_structure, build_skill

root = "/path/to/skills-copy/library"
blueprint = {"skill_name": "kpi_manager", "entry_instruction": "calculate_kpi"}

setup_factory_structure(root)
build_skill(root, blueprint)
```
