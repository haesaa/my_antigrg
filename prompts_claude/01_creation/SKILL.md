---
name: 01_creation
description: "크랙 프롬프트 파이프라인 Phase 1 — 세계관·캐릭터 생성. 1단계(세계관빌더)+2단계(성격유형)를 순차 실행. romance_guide.md를 기법 사전으로 상속."
version: 5.0.0
author: Antigravity
tags: [crack, phase1, phase2, worldbuilding, personality, creation]
---

# Phase 1: Creation (세계관 + 캐릭터 생성)

## 포함 에이전트

| 단계 | 에이전트 | 산출물 |
|------|---------|--------|
| 1 | world_builder | outputs/1_full_prompt.md |
| 2 | personality_designer | outputs/2_personality_prompt.md |

## 지식 로드 파이프라인 (GoT 적응적 탐색)

- **상시 로드 (0-hop)**: `c:\hehe\skills\RAG\A` 섹션의 필수 보안/제약 규칙 (`A1_security.md`, `A2_token_guard.md` 등)
- **1-hop 탐색**: `c:\hehe\skills\RAG\catalog.json` 쿼리 -> `worldbuilding`, `character`, `psychology` 태그 스캔 후 필요한 RAG 섹션(`B3`, `B2`, `E1` 등) 맵핑 동적 로드
- **2-hop 탐색**: 토큰 여유 수치(90% 미만) 확인 후, 심화 속성 식별 시 `sexology`(E2) 등 종속 개념 추가 병합
- **정적 참조 폐기**: 기존 하드코딩된 단일 파일 로드(`romance_guide.md` 등)를 완전히 폐기하고 자동 RAG 태깅 파이프라인 구조를 따름.

## 모델 타겟

기본: `MODEL_TARGET: SC25_PC25`
변경: `shared/model_profiles.md` 참조.

## 실행

```bash
python scripts/config.py --phases 1,2
```

## 결과물

- `outputs/1_full_prompt.md`: 세계관 + 캐릭터 전체 프롬프트
- `outputs/2_personality_prompt.md`: 성격유형 통합 프롬프트

## 제약

- max_tokens: 8000
- 캐릭터 수 하드코딩 금지
- {user} 성별/신분 하드코딩 금지
- romance_guide.md 기법 재정의 금지
