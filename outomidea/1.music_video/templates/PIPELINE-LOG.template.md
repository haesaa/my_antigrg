# Pipeline Log: {{PROJECT_NAME}}

- 생성일: {{CREATED_DATE}}
- 모드: {{PIPELINE_MODE}} ({{MODE_DESC}})
- 입력: {{INPUT_FILES}}
- 상태: 🟡 진행중

---

## Preflight

- [ ] 프로젝트 디렉토리 생성 ({{TIMESTAMP}})
- [ ] 입력 파일 복사: {{FILE_COUNT}}개
- [ ] MCP 연결 확인: {{MCP_STATUS}}
- [ ] 예산 설정: 상한 ${{BUDGET_LIMIT}}

---

## Input Gate

- [ ] 파일 검증: {{PASS_COUNT}}/{{TOTAL_COUNT}} 통과
- [ ] 인젝션 스캔: {{INJECTION_COUNT}}건 탐지
- [ ] 모드 결정: {{PIPELINE_MODE}}
- 상태: {{GATE_STATUS}}

---

## T1: 분석 (Analyzer)

- 시작: {{T1_START}}
- 완료: {{T1_END}}
- 상태: {{T1_STATUS}}
- 산출물: work/T1-analysis/analysis.json
- 요약: {{T1_SUMMARY}}
- 누적비용: ${{CUMULATIVE_COST}}

---

## T2: 이미지 생성 (Creator)

- 시작: {{T2_START}}
- 테스트 이미지: work/T2-images/test-image.png
- Plan Approval: {{PLAN_APPROVAL_STATUS}}
- 장면 생성: {{SCENE_PROGRESS}}
- 완료: {{T2_END}}
- 산출물: work/T2-images/scene-01.png ~ scene-{{SCENE_COUNT}}.png
- 누적비용: ${{CUMULATIVE_COST}}

---

## T3: 모션 생성 (Creator)

- 시작: {{T3_START}}
- {{SCENE_DETAIL}}
- 완료: {{T3_END}}
- 누적비용: ${{CUMULATIVE_COST}}

---

## T4: 오디오 (Editor) — T2와 병렬 실행

- 시작: {{T4_START}}
- {{AUDIO_DETAIL}}
- 완료: {{T4_END}}
- 누적비용: ${{CUMULATIVE_COST}}

---

## T5: 편집/합성 (Editor)

- 시작: {{T5_START}}
- 트랜지션 적용: {{TRANSITION_TYPE}}
- 렌더링: 1920x1080 H.264 AAC
- 완료: {{T5_END}}
- 산출물: output/final.mp4
- 누적비용: ${{CUMULATIVE_COST}}

---

## 최종

- 상태: {{FINAL_STATUS}}
- 총 소요시간: {{TOTAL_DURATION}}
- 총 비용: ${{TOTAL_COST}} / ${{BUDGET_LIMIT}}
- 최종 파일: output/final.mp4
- 해시: sha256:{{FILE_HASH}}
