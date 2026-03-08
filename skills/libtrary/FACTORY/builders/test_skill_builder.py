"""
Skill Builder Tests - 00testcode.md 2단계, 3단계 기반
pytest tmp_path 격리 환경 사용 (실제 파일 시스템 보호)
pytest로 실행: python -m pytest test_skill_builder.py -v
"""
import os
import json
import pytest
from skill_builder import setup_factory_structure, build_skill, register_skill


# ===========================================================
# 2단계: 디렉토리 구조 생성 테스트 (Isolation)
# ===========================================================

def test_factory_directory_creation(tmp_path):
    """
    FACTORY/LIBRARY 폴더가 올바르게 생성되는지 확인.
    실제 폴더 대신 pytest tmp_path 임시 폴더 사용.
    """
    setup_factory_structure(str(tmp_path))

    assert os.path.exists(tmp_path / "FACTORY" / "blueprints")
    assert os.path.exists(tmp_path / "FACTORY" / "validators")
    assert os.path.exists(tmp_path / "FACTORY" / "builders")
    assert os.path.exists(tmp_path / "LIBRARY" / "guides")
    assert os.path.exists(tmp_path / "LIBRARY" / "instructions")
    assert os.path.exists(tmp_path / "LIBRARY" / "graph")
    assert os.path.exists(tmp_path / "LIBRARY" / "tools")
    assert os.path.exists(tmp_path / "LIBRARY" / "memory")

    print(f"\n[Safety Check] 실제 경로 대신 {tmp_path}에서 안전하게 검증됨.")


# ===========================================================
# 3단계: SKILL.md 파일 생성 테스트 (CRUD Workflow)
# ===========================================================

def test_skill_file_generation(tmp_path):
    """
    Blueprint로부터 SKILL.md가 올바른 내용으로 생성되는지 확인.
    """
    blueprint = {
        "skill_name": "data_cleaner",
        "entry_instruction": "clean_csv",
        "guides": ["data_guide"],
        "tools": ["python_exec"]
    }

    skill_md_path = build_skill(str(tmp_path), blueprint)

    skill_file = tmp_path / "skills" / "data_cleaner" / "SKILL.md"
    assert skill_file.exists()

    content = skill_file.read_text(encoding="utf-8")
    assert "Skill Data Cleaner" in content
    assert "clean_csv" in content
    assert "data_guide" in content
    assert "python_exec" in content

    print(f"\n[OK] SKILL.md 생성 확인: {skill_file}")


def test_build_skill_idempotent(tmp_path):
    """
    동일 Blueprint를 두 번 빌드해도 오류가 발생하지 않아야 한다."""
    blueprint = {
        "skill_name": "idempotent_skill",
        "entry_instruction": "run_once",
        "guides": ["some_guide"]
    }
    build_skill(str(tmp_path), blueprint)
    build_skill(str(tmp_path), blueprint)  # 두 번째 - 오류 없어야 함

    skill_file = tmp_path / "skills" / "idempotent_skill" / "SKILL.md"
    assert skill_file.exists()


# ===========================================================
# Registry 등록 테스트
# ===========================================================

def test_register_skill(tmp_path):
    """skill_registry.json에 skill이 올바르게 등록되는지 확인."""
    registry_path = str(tmp_path / "skill_registry.json")
    blueprint = {
        "skill_name": "kpi_manager",
        "entry_instruction": "calculate_kpi",
        "guides": ["sales_guide"]
    }

    register_skill(registry_path, blueprint)

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    assert len(registry["skills"]) == 1
    assert registry["skills"][0]["name"] == "kpi_manager"
    assert registry["skills"][0]["entry_instruction"] == "calculate_kpi"


def test_register_multiple_skills(tmp_path):
    """여러 skill이 registry에 누적 등록되는지 확인."""
    registry_path = str(tmp_path / "skill_registry.json")

    for name, entry in [("skill_a", "run_a"), ("skill_b", "run_b")]:
        register_skill(registry_path, {
            "skill_name": name,
            "entry_instruction": entry,
            "guides": ["guide"]
        })

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    assert len(registry["skills"]) == 2
