"""
03_condenser 설정 — Phase 3: 축약 + 축약 품질심사
max_tokens: 6000
"""
import os
from pathlib import Path

FOLDER_NAME = "03_condenser"
MAX_TOKENS = 6000
TEMPERATURE = 0.7

AGENT_SEQUENCE = ["prompt_condenser", "condenser_reviewer"]

OUTPUT_FILES = {
    "prompt_condenser": "4_condensed_prompt.md",
    "condenser_reviewer": "10_condenser_review.md",
}

CHAR_LIMITS = {
    "prompt_condenser": 4800,
}

MODEL_TARGET = os.getenv("MODEL_TARGET", "SC25_PC25")
QUALITY_THRESHOLD = 80
MAX_RETRIES = 3

# 경로
SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent
RESOURCES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "RAG"
SHARED_DIR = SKILLS_ROOT / "shared"
