"""
Blueprint Validation Tests - 00testcode.md 1단계 기반
pytest로 실행: python -m pytest test_blueprint_validation.py -v
"""
import pytest
from validate_blueprint import validate_blueprint, validate_instructions, validate_tools


# ===========================================================
# Fixtures
# ===========================================================

@pytest.fixture
def valid_blueprint():
    """00testcode.md의 kpi_manager 예시 반영"""
    return {
        "skill_name": "kpi_manager",
        "entry_instruction": "calculate_kpi",
        "instructions": ["calculate_kpi", "aggregate_metrics"],
        "guides": ["sales_guide"],
        "tools": ["python_exec"]
    }


# ===========================================================
# Rule 1: skill_name must be unique
# ===========================================================

def test_blueprint_valid(valid_blueprint):
    """성공 케이스: 새로운 skill_name"""
    is_valid, msg = validate_blueprint(valid_blueprint, ["old_skill"])
    assert is_valid is True
    assert msg == "Valid"


def test_duplicate_skill_name_fails(valid_blueprint):
    """실패 케이스: 중복된 skill_name"""
    is_valid, msg = validate_blueprint(valid_blueprint, ["kpi_manager"])
    assert is_valid is False
    assert msg == "Skill name must be unique"


# ===========================================================
# Rule 2: entry_instruction must exist
# ===========================================================

def test_missing_entry_instruction_fails():
    """실패 케이스: entry_instruction 없음"""
    blueprint = {
        "skill_name": "new_skill",
        "guides": ["some_guide"]
    }
    is_valid, msg = validate_blueprint(blueprint, [])
    assert is_valid is False
    assert msg == "Entry instruction must exist"


def test_empty_entry_instruction_fails():
    """실패 케이스: entry_instruction 빈 문자열"""
    blueprint = {
        "skill_name": "new_skill",
        "entry_instruction": "",
        "guides": ["some_guide"]
    }
    is_valid, msg = validate_blueprint(blueprint, [])
    assert is_valid is False
    assert msg == "Entry instruction must exist"


# ===========================================================
# Rule 3: guides must exist
# ===========================================================

def test_missing_guides_fails():
    """실패 케이스: guides 없음"""
    blueprint = {
        "skill_name": "new_skill",
        "entry_instruction": "do_something"
    }
    is_valid, msg = validate_blueprint(blueprint, [])
    assert is_valid is False
    assert msg == "Guides must exist"


def test_empty_guides_fails():
    """실패 케이스: guides 빈 배열"""
    blueprint = {
        "skill_name": "new_skill",
        "entry_instruction": "do_something",
        "guides": []
    }
    is_valid, msg = validate_blueprint(blueprint, [])
    assert is_valid is False
    assert msg == "Guides must exist"


# ===========================================================
# Rule 4: instructions in instruction_graph
# ===========================================================

def test_invalid_instruction_fails(valid_blueprint):
    """실패 케이스: instruction_graph에 없는 instruction"""
    instruction_graph = ["calculate_kpi"]  # aggregate_metrics 없음
    is_valid, msg = validate_instructions(valid_blueprint, instruction_graph)
    assert is_valid is False
    assert "aggregate_metrics" in msg


def test_valid_instructions_pass(valid_blueprint):
    """성공 케이스: 모든 instruction이 graph에 존재"""
    instruction_graph = ["calculate_kpi", "aggregate_metrics"]
    is_valid, msg = validate_instructions(valid_blueprint, instruction_graph)
    assert is_valid is True


# ===========================================================
# Rule 5: tools in tool_registry
# ===========================================================

def test_invalid_tool_fails(valid_blueprint):
    """실패 케이스: tool_registry에 없는 tool"""
    tool_registry = []
    is_valid, msg = validate_tools(valid_blueprint, tool_registry)
    assert is_valid is False
    assert "python_exec" in msg


def test_valid_tools_pass(valid_blueprint):
    """성공 케이스: 모든 tool이 registry에 존재"""
    tool_registry = ["python_exec", "file_read", "file_write"]
    is_valid, msg = validate_tools(valid_blueprint, tool_registry)
    assert is_valid is True
