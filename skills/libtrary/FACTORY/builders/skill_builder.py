"""
Skill Builder - anti_task_v0.4.md Section 6, 7, 12 기반
00testcode.md 2단계 로직 구현
"""
import os
import json


def setup_factory_structure(root_path: str) -> None:
    """
    FACTORY 및 LIBRARY 기본 디렉토리 구조를 생성한다.
    (00testcode.md 2단계 - test_factory_directory_creation 기반)

    Args:
        root_path: library 루트 경로
    """
    folders = [
        "FACTORY/blueprints",
        "FACTORY/validators",
        "FACTORY/builders",
        "LIBRARY/guides",
        "LIBRARY/instructions",
        "LIBRARY/graph",
        "LIBRARY/tools",
        "LIBRARY/memory",
    ]
    for folder in folders:
        os.makedirs(os.path.join(root_path, folder), exist_ok=True)


def build_skill(root_path: str, blueprint: dict) -> str:
    """
    Blueprint를 기반으로 skill 디렉토리와 SKILL.md를 생성한다.
    (00testcode.md 3단계 - test_skill_file_generation 기반)

    Args:
        root_path: library 루트 경로
        blueprint: 검증된 Blueprint dict

    Returns:
        생성된 SKILL.md의 절대 경로
    """
    skill_name = blueprint["skill_name"]
    skill_dir = os.path.join(root_path, "skills", skill_name)
    os.makedirs(skill_dir, exist_ok=True)

    skill_md_content = _generate_skill_md(blueprint)

    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(skill_md_content)

    return skill_md_path


def _generate_skill_md(blueprint: dict) -> str:
    """SKILL.md 내용을 생성한다."""
    name_title = blueprint["skill_name"].replace("_", " ").title()
    entry = blueprint["entry_instruction"]
    guides = blueprint.get("guides", [])
    tools = blueprint.get("tools", [])

    lines = [
        f"# Skill {name_title}",
        "",
        "entry_instruction",
        "",
        entry,
        "",
    ]

    if guides:
        lines += ["---", "", "## Guides", ""]
        for g in guides:
            lines.append(f"- {g}")
        lines.append("")

    if tools:
        lines += ["---", "", "## Tools", ""]
        for t in tools:
            lines.append(f"- {t}")
        lines.append("")

    return "\n".join(lines)


def register_skill(registry_path: str, blueprint: dict) -> None:
    """
    skill_registry.json에 새 skill을 등록한다.

    Args:
        registry_path: skill_registry.json 파일 경로
        blueprint: 등록할 Blueprint dict
    """
    if os.path.exists(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)
    else:
        registry = {"skills": []}

    entry = {
        "name": blueprint["skill_name"],
        "entry_instruction": blueprint["entry_instruction"]
    }
    registry["skills"].append(entry)

    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
