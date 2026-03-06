# Task Report: {{TASK_NAME}}

- 담당: {{ASSIGNEE}} ({{ROLE}})
- 시작: {{START_TIME}}
- 종료: {{END_TIME}}
- 상태: {{STATUS}}

---

## 사용 MCP

- Primary: {{PRIMARY_MCP}}
- 호출 횟수: {{CALL_COUNT}}
- 폴백 발생: {{FALLBACK_EVENTS}}

---

## Plan Approval (T2 전용)

- 테스트 이미지: {{TEST_IMAGE_PATH}}
- 검증 결과: 해상도 {{RESOLUTION}} {{RES_STATUS}}, 캐릭터 유사도 {{SIMILARITY}} {{SIM_STATUS}}
- 승인 시각: {{APPROVAL_TIME}}

---

## 산출물 목록

| 파일 | 크기 | 해상도/길이 | 검증 |
|------|------|-----------|------|
| {{FILE_1}} | {{SIZE_1}} | {{SPEC_1}} | {{CHECK_1}} |
| {{FILE_2}} | {{SIZE_2}} | {{SPEC_2}} | {{CHECK_2}} |

---

## 사용 프롬프트 (재현용)

- {{SCENE_ID}}: "{{PROMPT_TEXT}}"

---

## 에러/재시도 기록

| 시각 | 이벤트 | MCP | 결과 |
|------|--------|-----|------|
| {{TIME}} | {{EVENT}} | {{MCP}} | {{RESULT}} |

---

## 비용

- 토큰: {{TOKEN_COUNT}}
- API 호출 비용: ${{API_COST}}
- 누적 파이프라인 비용: ${{CUMULATIVE_COST}}
