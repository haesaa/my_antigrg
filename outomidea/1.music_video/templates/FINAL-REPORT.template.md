# Final Report

- 프로젝트: {{PROJECT_ID}}
- 모드: {{PIPELINE_MODE}} ({{MODE_DESC}})
- 결과: {{FINAL_STATUS}}

---

## 최종 산출물

- {{OUTPUT_FILE}} ({{FILE_SIZE}}, {{DURATION}}, {{RESOLUTION}})
- SHA-256: {{FILE_HASH}}

---

## 파이프라인 요약

| 단계 | 상태 | 소요시간 | MCP | 비용 |
|------|------|---------|-----|------|
| T1 분석 | {{T1_STATUS}} | {{T1_DURATION}} | {{T1_MCP}} | ${{T1_COST}} |
| T2 이미지 | {{T2_STATUS}} | {{T2_DURATION}} | {{T2_MCP}} | ${{T2_COST}} |
| T3 모션 | {{T3_STATUS}} | {{T3_DURATION}} | {{T3_MCP}} | ${{T3_COST}} |
| T4 오디오 | {{T4_STATUS}} | {{T4_DURATION}} | {{T4_MCP}} | ${{T4_COST}} |
| T5 편집 | {{T5_STATUS}} | {{T5_DURATION}} | {{T5_MCP}} | ${{T5_COST}} |
| **합계** | | **{{TOTAL_DURATION}}** | | **${{TOTAL_COST}}** |

---

## 보안 이벤트

- 입력 검증: {{INPUT_VALIDATION}}
- NSFW 스캔: {{NSFW_RESULT}} ({{FRAME_COUNT}}장면 검사)
- 메타데이터 스트립: {{METADATA_STRIP}}
- 인젝션 탐지: {{INJECTION_DETECTION}}

---

## 비용 상세

| 항목 | 비용 |
|------|------|
| MCP API 호출 | ${{MCP_COST}} |
| 에이전트 토큰 | ${{TOKEN_COST}} |
| 재시도/폴백 | ${{RETRY_COST}} |
| **합계** | **${{TOTAL_COST}}** |
| **예산 상한** | **${{BUDGET_LIMIT}}** |
| **잔여** | **${{REMAINING}}** |

---

## 재현 정보

- 모든 프롬프트: work/T1-analysis/prompts/
- 분석 결과: work/T1-analysis/analysis.json
- MCP 설정: config/mcp-fallback.json
- 이 프로젝트를 이어서 작업하려면:

  ```
  "{{PROJECT_ID}} T{N}부터 재실행" 으로 지시
  ```

---

## 산출물 전체 목록

### input/ (유저 원본 — READ-ONLY)

{{INPUT_FILE_LIST}}

### work/ (중간 산출물 — 보존)

{{WORK_FILE_LIST}}

### output/ (최종 산출물)

{{OUTPUT_FILE_LIST}}
