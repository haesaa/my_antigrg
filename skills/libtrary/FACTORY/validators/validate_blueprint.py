"""
Blueprint Validator - anti_task_v0.4.md Section 5 기반
00testcode.md 1단계 로직 구현
"""


def validate_blueprint(blueprint: dict, existing_skills: list) -> tuple[bool, str]:
    """
    Blueprint의 유효성을 검증한다.

    Rules:
        1. skill_name must be unique
        2. entry_instruction must exist
        3. guides must exist (non-empty)

    Args:
        blueprint: 검증할 Blueprint dict
        existing_skills: 이미 등록된 skill 이름 목록

    Returns:
        (is_valid: bool, message: str)
    """
    # Rule 1: skill_name must be unique
    if blueprint.get("skill_name") in existing_skills:
        return False, "Skill name must be unique"

    # Rule 2: entry_instruction must exist
    if not blueprint.get("entry_instruction"):
        return False, "Entry instruction must exist"

    # Rule 3: guides must exist
    if not blueprint.get("guides"):
        return False, "Guides must exist"

    return True, "Valid"


def validate_instructions(blueprint: dict, instruction_graph: list) -> tuple[bool, str]:
    """Rule 4: instructions must exist in instruction_graph"""
    for inst in blueprint.get("instructions", []):
        if inst not in instruction_graph:
            return False, f"Invalid instruction: {inst}"
    return True, "Valid"


def validate_tools(blueprint: dict, tool_registry: list) -> tuple[bool, str]:
    """Rule 5: tools must exist in tool_registry"""
    for tool in blueprint.get("tools", []):
        if tool not in tool_registry:
            return False, f"Invalid tool: {tool}"
    return True, "Valid"
