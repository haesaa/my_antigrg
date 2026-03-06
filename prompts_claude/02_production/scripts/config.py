"""
02_production 설정 — Phase 2: 부속품 생성
max_tokens: 6000
"""
import os
from pathlib import Path

FOLDER_NAME = "02_production"
MAX_TOKENS = 6000
TEMPERATURE = 0.7

AGENT_SEQUENCE = [
    "visual_designer",    # 3단계: 외형·이미지 프롬프트
    "keyword_creator",    # 5단계: 키워드북 생성기
    "scenario_writer",    # 6단계: 시작 시나리오 작가
    "example_dialogue",   # 7단계: 예시대화 생성기
    "play_guide",         # 8단계: 추천답변·플레이가이드
    "quality_reviewer",   # 9단계: 품질 심사관
]

OUTPUT_FILES = {
    "visual_designer": "3_visual_prompts.md",
    "keyword_creator": "5_keyword_books.md",
    "scenario_writer": "6_opening_scenario.md",
    "example_dialogue": "7_example_dialogue.md",
    "play_guide": "8_play_guide.md",
    "quality_reviewer": "9_review.md",
}

CHAR_LIMITS = {
    "keyword_creator": 400,
    "scenario_writer": 900,
    "example_dialogue": 500,   # 각 칸당
    "play_guide": 400,
}

MODEL_TARGET = os.getenv("MODEL_TARGET", "SC25_PC25")
QUALITY_THRESHOLD = 80
MAX_RETRIES = 3

# 경로
SKILLS_ROOT = Path(__file__).resolve().parent.parent.parent
RESOURCES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "RAG"
SHARED_DIR = SKILLS_ROOT / "shared"
