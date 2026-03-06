# CLAUDE.md — Harness Skills 가이드 v3

## 프로젝트 개요

**Harness Skills v3** — `harness-orchestrator`(Agent Teams 구조)가 Leader/Analyst/Builder/Reviewer 팀으로 자동 파이프라인 실행.

- **외부 API**: 사용하지 않음. Antigravity + 로컬 도구만 사용
- **로컬 도구**: 필요 시 링크+추천 → 사용자 승인 후에만 설치
- **MAX_TOKENS**: 10,000 (80%에서 checkpoint.json 자동 저장)

## 팀 구성

| 역할 | 담당 | 실행 스킬 |
|------|------|---------|
| **Leader** | 파이프라인 제어, 종료 처리 | 00-preflight, 01-complexity, 05-exit |
| **Analyst** | MCP Router + Instruction Generator | 02-analyze |
| **Builder** | Skill Forge (스킬 생성) | 03-forge |
| **Reviewer** | Verification 3단계 + Reflection | 04-verify |

## 실행 순서 (파이프라인)

```
유저 요청 → harness-orchestrator/SKILL.md (Leader 진입)
  → 00-preflight: 환경 초기화 + Resume 판정 + 보안 스캔
  → 01-complexity: 복잡도 판정 + ToT 3분기 + ToC 채점
  → 02-analyze: Analyst — MCP Router + Instruction Generator
  → 03-forge: Builder — simple|composite 스킬 생성
  → 04-verify: Reviewer — Schema/Functional/Quality 검증
  → 05-exit: 최종 보고 + Graceful Degradation
```

## Skills

| 스킬 | 역할 | 호출 방식 |
|------|------|---------|
| `harness-orchestrator` | 파이프라인 런너 (진입점) | Leader가 skills/ 동적 로딩 |
| `mcp-router` | MCP 서버 추천 | 02-analyze에서 view_file 로딩 |
| `instruction-gen` | system prompt 조합 | 02-analyze에서 view_file 로딩 |
| `skill-forge` | 스킬 자동 생성 | 03-forge에서 view_file 로딩 |
| `token-guard` | 토큰 추적 + 체크포인트 | 01-complexity / 05-exit에서 참조 |
| `verification-layer` | 3단계 품질 검증 | 04-verify에서 view_file 로딩 |
| `verify-outomidea-pipeline` | Outomidea V4 파이프라인 무결성 검증 | manage-skills을 통해 등록됨 |
| `word-counter` | 텍스트 통계 (독립 유틸) | standalone |
| `streamlit-tetris` | Streamlit 게임 생성 (예시) | standalone |

## 참조 파일

| 파일 | 용도 |
|------|------|
| `harness-orchestrator/references/tot-guide.md` | ToT/ToC/Reflection 가이드 |
| `references/interface-spec.md` | 모듈 간 인터페이스 스키마 |
| `Awesome-MCP-Servers-한국어-가이드.md` | MCP 서버 카탈로그 (2596개) |
| `harness-orchestrator/templates/checkpoint.template.jsonc` | 체크포인트 포맷 |
| `tests/e2e-dryrun.md` | E2E 테스트 시나리오 |
