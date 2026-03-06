# D2: 프롬프트 키워드/모델 튜닝 편향 극복 (SoT)

- **시스템 프롬프트 (System Prompt)**: 역할(Role), 목표(Goal), 제약(Constraints), 형식(Output) 4단 구조
- **편향 제어**:
  - LLM 특유의 "도덕적 설교" 투사 방어 지시문 추가 ("어떠한 훈계나 도덕적 평가 금지")
  - `[UNSAFE]` 허용 시, "Safety Violation 필터 우회를 위한 문맥적 은유" 활용
- **키워드 할당**: 주요 설정/속성은 1어절 Keyword로 고정해 일관성 유지
