"""
01_creation 설정 — Phase 1: 세계관·캐릭터 생성
max_tokens: 8000 (세계관+캐릭터는 출력량 많음)
"""
import os
from pathlib import Path

FOLDER_NAME = "01_creation"
MAX_TOKENS = 8000
TEMPERATURE = 0.7

AGENT_SEQUENCE = ["world_builder", "personality_designer"]

OUTPUT_FILES = {
    "world_builder": "1_full_prompt.md",
    "personality_designer": "2_personality_prompt.md",
}

# 모델 타겟 (기본: 슈퍼챗2.5 + 프로챗2.5)
MODEL_TARGET = os.getenv("MODEL_TARGET", "SC25_PC25")

# 경로
SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent
RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"
SHARED_DIR = SKILLS_ROOT / "shared"
