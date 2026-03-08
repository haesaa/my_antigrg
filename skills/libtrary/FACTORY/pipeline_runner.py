"""
Pipeline Runner - Skill Factory 전체 파이프라인 실행기
anti_task_v0.4.md 섹션 9 기반

Flow: Blueprint → Validate → Build → Register → Memory Update

사용법:
    python pipeline_runner.py example_blueprint.json
"""
import os
import sys
import json
import datetime

# 경로 설정 - import 전에 path 삽입
_FACTORY_DIR = os.path.dirname(os.path.abspath(__file__))   # .../FACTORY
_LIBRARY_DIR = os.path.join(os.path.dirname(_FACTORY_DIR), "LIBRARY")

sys.path.insert(0, os.path.join(_FACTORY_DIR, "validators"))
sys.path.insert(0, os.path.join(_FACTORY_DIR, "builders"))

from validate_blueprint import validate_blueprint, validate_instructions, validate_tools
from skill_builder import build_skill, register_skill

# ROOT: library/ 폴더
ROOT = os.path.dirname(_FACTORY_DIR)
FACTORY = _FACTORY_DIR
LIBRARY = _LIBRARY_DIR


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_registry_names(root: str) -> list:
    registry_path = os.path.join(root, "skill_registry.json")
    if not os.path.exists(registry_path):
        return []
    registry = load_json(registry_path)
    return [s["name"] for s in registry.get("skills", [])]


def load_graph_names(graph_file: str, key: str) -> list:
    if not os.path.exists(graph_file):
        return []
    data = load_json(graph_file)
    return [item["name"] for item in data.get(key, [])]


def update_memory(root: str, blueprint: dict, success: bool, error: str = None) -> None:
    memory_path = os.path.join(root, "LIBRARY", "memory", "session_memory.json")
    if not os.path.exists(memory_path):
        memory = {"session": {}, "history": [], "errors": []}
    else:
        memory = load_json(memory_path)

    now = datetime.datetime.now().isoformat()
    memory["session"]["last_run"] = now
    memory["session"]["last_blueprint"] = blueprint.get("skill_name")

    if success:
        memory["session"]["last_skill_built"] = blueprint.get("skill_name")
        memory["history"].append({"skill": blueprint["skill_name"], "built_at": now})
    else:
        memory["errors"].append({"skill": blueprint.get("skill_name"), "error": error, "at": now})

    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)


def run_pipeline(blueprint_path: str) -> None:
    """전체 파이프라인 실행 (Blueprint JSON 경로를 입력받음)"""
    print(f"\n[FACTORY] Skill Factory Pipeline Starting...")
    print(f"   Blueprint: {blueprint_path}\n")

    # 1. Blueprint 로드
    blueprint = load_json(blueprint_path)
    print(f"[1] Blueprint loaded: {blueprint['skill_name']}")

    # 2. Validator 실행 (Rule 1~3)
    existing_skills = load_registry_names(ROOT)
    is_valid, msg = validate_blueprint(blueprint, existing_skills)
    if not is_valid:
        print(f"[2] FAIL Validation FAILED: {msg}")
        update_memory(ROOT, blueprint, success=False, error=msg)
        sys.exit(1)

    # Rule 4: instruction graph 검증
    instruction_graph_path = os.path.join(LIBRARY, "graph", "instruction_graph.json")
    instruction_names = load_graph_names(instruction_graph_path, "instructions")
    if instruction_names:
        is_valid, msg = validate_instructions(blueprint, instruction_names)
        if not is_valid:
            print(f"[2] FAIL Instruction validation FAILED: {msg}")
            update_memory(ROOT, blueprint, success=False, error=msg)
            sys.exit(1)

    # Rule 5: tool registry 검증
    tool_registry_path = os.path.join(LIBRARY, "tools", "tool_registry.json")
    tool_names = load_graph_names(tool_registry_path, "tools")
    if tool_names:
        is_valid, msg = validate_tools(blueprint, tool_names)
        if not is_valid:
            print(f"[2] FAIL Tool validation FAILED: {msg}")
            update_memory(ROOT, blueprint, success=False, error=msg)
            sys.exit(1)

    print(f"[2] OK Validation PASSED")

    # 3. Builder 실행
    skill_md_path = build_skill(ROOT, blueprint)
    print(f"[3] OK Skill built: {skill_md_path}")

    # 4. Registry 등록
    registry_path = os.path.join(ROOT, "skill_registry.json")
    register_skill(registry_path, blueprint)
    print(f"[4] OK Skill registered in skill_registry.json")

    # 5. Memory 업데이트
    update_memory(ROOT, blueprint, success=True)
    print(f"[5] OK Session memory updated\n")

    print(f"[DONE] Pipeline Complete: {blueprint['skill_name']}")
    print(f"   SKILL.md -> {skill_md_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline_runner.py <blueprint_json_path>")
        sys.exit(1)
    run_pipeline(sys.argv[1])
