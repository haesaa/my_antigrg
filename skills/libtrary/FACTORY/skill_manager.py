"""
Skill Manager - CRUD Workflow 완성
anti_task_v0.4.md 섹션 11 기반

새 Skill 생성: blueprint -> validator -> builder -> register
Skill 삭제:   skill_registry 수정 + skill 폴더 삭제
Skill 수정:   blueprint 수정 + builder 재실행
"""
import os
import sys
import json
import shutil

# 경로 설정
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_VALIDATORS_DIR = os.path.join(_THIS_DIR, "validators")
_BUILDERS_DIR = os.path.join(_THIS_DIR, "builders")
sys.path.insert(0, _VALIDATORS_DIR)
sys.path.insert(0, _BUILDERS_DIR)

ROOT = os.path.dirname(_THIS_DIR)

from validate_blueprint import validate_blueprint
from skill_builder import build_skill, register_skill


# ============================================================
# CREATE  (섹션 11: 새 Skill 생성)
# ============================================================
def create_skill(blueprint: dict) -> str:
    """
    Blueprint -> Validate -> Build -> Register

    Args:
        blueprint: Blueprint dict

    Returns:
        생성된 SKILL.md 경로

    Raises:
        ValueError: Validation 실패 시
    """
    registry_path = os.path.join(ROOT, "skill_registry.json")
    existing = _load_skill_names(registry_path)

    is_valid, msg = validate_blueprint(blueprint, existing)
    if not is_valid:
        raise ValueError(f"Blueprint validation failed: {msg}")

    skill_md_path = build_skill(ROOT, blueprint)
    register_skill(registry_path, blueprint)
    return skill_md_path


# ============================================================
# DELETE  (섹션 11: Skill 삭제)
# ============================================================
def delete_skill(skill_name: str) -> bool:
    """
    1. skill_registry.json에서 제거
    2. skills/{skill_name}/ 폴더 삭제

    Args:
        skill_name: 삭제할 skill 이름

    Returns:
        True if deleted, False if not found
    """
    registry_path = os.path.join(ROOT, "skill_registry.json")
    removed = _remove_from_registry(registry_path, skill_name)

    skill_dir = os.path.join(ROOT, "skills", skill_name)
    if os.path.exists(skill_dir):
        shutil.rmtree(skill_dir)

    return removed


# ============================================================
# UPDATE  (섹션 11: Skill 수정)
# ============================================================
def update_skill(skill_name: str, new_blueprint: dict) -> str:
    """
    1. 기존 등록 항목 제거
    2. 새 Blueprint로 build_skill 재실행
    3. Registry 재등록

    Args:
        skill_name: 수정할 기존 skill 이름
        new_blueprint: 수정된 Blueprint dict (skill_name 포함)

    Returns:
        업데이트된 SKILL.md 경로
    """
    registry_path = os.path.join(ROOT, "skill_registry.json")
    _remove_from_registry(registry_path, skill_name)

    skill_md_path = build_skill(ROOT, new_blueprint)
    register_skill(registry_path, new_blueprint)
    return skill_md_path


# ============================================================
# READ  - Registry 조회
# ============================================================
def list_skills() -> list:
    """skill_registry.json에서 등록된 skill 목록 반환"""
    registry_path = os.path.join(ROOT, "skill_registry.json")
    return _load_skill_names(registry_path)


def get_skill(skill_name: str) -> dict | None:
    """특정 skill 정보 반환. 없으면 None."""
    registry_path = os.path.join(ROOT, "skill_registry.json")
    registry = _load_json(registry_path)
    for s in registry.get("skills", []):
        if s["name"] == skill_name:
            return s
    return None


# ============================================================
# 내부 유틸
# ============================================================
def _load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {"skills": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_skill_names(registry_path: str) -> list:
    registry = _load_json(registry_path)
    return [s["name"] for s in registry.get("skills", [])]


def _remove_from_registry(registry_path: str, skill_name: str) -> bool:
    registry = _load_json(registry_path)
    original_count = len(registry.get("skills", []))
    registry["skills"] = [s for s in registry.get("skills", []) if s["name"] != skill_name]
    removed = len(registry["skills"]) < original_count
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    return removed
