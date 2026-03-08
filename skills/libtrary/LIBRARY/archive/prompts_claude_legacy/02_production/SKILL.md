---
name: 02_production
description: "크랙 프롬프트 파이프라인 Phase 2 — 부속품 생성. 3(외형)→5(키워드)→6(시나리오)→7(예시대화)→8(플레이가이드)→9(품질심사) 순차 실행."
version: 5.0.0
author: Antigravity
tags: [crack, phase3, phase5, phase6, phase7, phase8, phase9, production]
---

# Phase 2: Production (부속품 생성)

## 포함 에이전트

| 단계 | 에이전트 | 산출물 | 글자제한 |
|------|---------|--------|---------|
| 3 | visual_designer | outputs/3_visual_prompts.md | — |
| 5 | keyword_creator | outputs/5_keyword_books.md | 각 400자 |
| 6 | scenario_writer | outputs/6_opening_scenario.md | 각 900자 |
| 7 | example_dialogue | outputs/7_example_dialogue.md | 각칸 ~500자 |
| 8 | play_guide | outputs/8_play_guide.md | 400자 |
| 9 | quality_reviewer | outputs/9_review.md | — |

## 의존성

Phase 1 산출물(`outputs/1_full_prompt.md`, `outputs/2_personality_prompt.md`)을 inputs로 사용.

## 모델 타겟

기본: `MODEL_TARGET: SC25_PC25`
변경: `shared/model_profiles.md` 참조.

## 실행

```bash
python scripts/config.py --phases 3,5,6,7,8,9

# 개별 실행
python scripts/config.py --phases 3
python scripts/config.py --phases 5
python scripts/config.py --phases 6
python scripts/config.py --phases 7
python scripts/config.py --phases 8
python scripts/config.py --phases 9
```

## 제약

- max_tokens: 6000
- 01_creation 산출물 완료 후 실행
- 9단계 품질 점수 80점 미만 시 자동 재시도 (최대 3회)
