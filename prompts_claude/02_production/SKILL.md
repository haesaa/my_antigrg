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

## 지식 로드 파이프라인 (GoT 적응적 탐색)

- **상시 로드 (0-hop)**: `c:\hehe\skills\RAG\A` 섹션의 필수 보안/제약 규칙 (`A1_security.md`, `A2_token_guard.md` 등)
- **1-hop 탐색**: `c:\hehe\skills\RAG\catalog.json` 쿼리 -> `cinematography`, `dialogue`, `cliche`, `review` 태그 스캔 후 필요한 RAG 섹션(`C3`, `B6`, `B4`, `D3` 등) 맵핑 동적 로드
- **2-hop 탐색**: 토큰 여유 수치(90% 미만) 확인 후, 장르나 문체 속성 식별 시 `writing_style`(B1), `romance`(B8) 등 종속 개념 추가 병합
- **정적 참조 폐기**: 기존 하드코딩된 단일 파일 로드를 방지하고 반드시 RAG 시스템을 통해 동적 참조할 것.

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
