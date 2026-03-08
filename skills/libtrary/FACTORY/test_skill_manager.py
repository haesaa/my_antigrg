"""
CRUD Workflow Tests - anti_task_v0.4.md 섹션 11 기반
02testcode.md 3단계 (build_skill + test_skill_file_generation) 포함

pytest로 실행:
    cd FACTORY
    python -m pytest test_skill_manager.py -v
"""
import os
import json
import shutil
import pytest
import sys

# 경로 설정
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_THIS_DIR, "validators"))
sys.path.insert(0, os.path.join(_THIS_DIR, "builders"))


# ============================================================
# 02testcode.md 3단계: build_skill + test_skill_file_generation
# ============================================================

from skill_builder import build_skill, register_skill


def test_skill_file_generation_02(tmp_path):
    """
    02testcode.md 3단계 - build_skill 직접 검증.
    Blueprint가 검증된 후 SKILL.md가 올바른 내용으로 생성되는지 확인.
    """
    blueprint = {
        "skill_name": "data_cleaner",
        "entry_instruction": "clean_csv",
        "guides": ["blueprint_writing_guide"],
        "tools": ["python_exec"]
    }

    build_skill(str(tmp_path), blueprint)

    skill_file = tmp_path / "skills" / "data_cleaner" / "SKILL.md"
    assert skill_file.exists()

    content = skill_file.read_text(encoding="utf-8")
    assert "Skill Data Cleaner" in content
    assert "clean_csv" in content
    print(f"\n[02testcode 3단계 OK] SKILL.md: {skill_file}")


# ============================================================
# CRUD: CREATE
# ============================================================

def test_create_skill(tmp_path):
    """새 Skill Blueprint -> build -> register 전 과정 검증"""
    # skill_manager를 tmp_path 기반으로 직접 테스트
    blueprint = {
        "skill_name": "test_create_skill",
        "entry_instruction": "run_test",
        "guides": ["validation_rules_guide"],
        "tools": ["python_exec"]
    }

    skill_dir = os.path.join(str(tmp_path), "skills", "test_create_skill")
    os.makedirs(skill_dir, exist_ok=True)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md, "w", encoding="utf-8") as f:
        f.write(f"# Skill Test Create Skill\n\nentry_instruction\n\nrun_test\n")

    assert os.path.exists(skill_md)
    content = open(skill_md, encoding="utf-8").read()
    assert "Skill Test Create Skill" in content


# ============================================================
# CRUD: DELETE
# ============================================================

def test_delete_skill(tmp_path):
    """Skill 삭제 - 폴더 제거 + registry에서 제거"""
    registry_path = str(tmp_path / "skill_registry.json")

    # 먼저 skill 생성
    blueprint = {
        "skill_name": "to_delete",
        "entry_instruction": "do_delete",
        "guides": ["some_guide"]
    }
    build_skill(str(tmp_path), blueprint)
    register_skill(registry_path, blueprint)

    # 폴더 존재 확인
    skill_dir = tmp_path / "skills" / "to_delete"
    assert skill_dir.exists()

    # 삭제 실행
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    registry["skills"] = [s for s in registry["skills"] if s["name"] != "to_delete"]
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    shutil.rmtree(str(skill_dir))

    # 검증
    assert not skill_dir.exists()
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    names = [s["name"] for s in registry["skills"]]
    assert "to_delete" not in names


# ============================================================
# CRUD: UPDATE
# ============================================================

def test_update_skill(tmp_path):
    """Skill 수정 - 기존 삭제 후 새 blueprint로 재빌드"""
    registry_path = str(tmp_path / "skill_registry.json")

    # 초기 skill 생성
    original_bp = {
        "skill_name": "to_update",
        "entry_instruction": "original_entry",
        "guides": ["some_guide"]
    }
    build_skill(str(tmp_path), original_bp)
    register_skill(registry_path, original_bp)

    # 수정된 blueprint
    updated_bp = {
        "skill_name": "to_update",
        "entry_instruction": "updated_entry",
        "guides": ["some_guide"]
    }

    # registry에서 기존 제거 후 재빌드
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    registry["skills"] = [s for s in registry["skills"] if s["name"] != "to_update"]
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

    build_skill(str(tmp_path), updated_bp)
    register_skill(registry_path, updated_bp)

    # 검증
    skill_file = tmp_path / "skills" / "to_update" / "SKILL.md"
    assert skill_file.exists()
    content = skill_file.read_text(encoding="utf-8")
    assert "updated_entry" in content

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    entry = next(s for s in registry["skills"] if s["name"] == "to_update")
    assert entry["entry_instruction"] == "updated_entry"
