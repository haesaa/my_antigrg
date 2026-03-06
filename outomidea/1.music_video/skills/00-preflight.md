---
name: 00-preflight
description: >
  파이프라인 실행 전 환경을 검증하고, 프로젝트 디렉토리를 초기화한다. 파이프라인 최초 진입 시 자동 활성화됩니다.
---

# 00-preflight: 사전 검증 스킬

> **실행자**: Leader (직접 실행, 팀 생성 전)
> **실행 시점**: 파이프라인 최초 진입 시
> **쓰기 권한**: 프로젝트 루트 전체 (디렉토리 생성)

## 목적

파이프라인 실행 전 환경을 검증하고, 프로젝트 디렉토리를 초기화합니다.
이 스킬이 실패하면 파이프라인에 진입하지 않으며, 작업의 기반을 마련하는 필수 관문입니다.

## 실행 시점

- 파이프라인 최초 진입 시 자동 활성화됩니다.
- 유저가 새로운 Music Video 프로젝트 시작을 요청할 때 사용해야 합니다.

## 워크플로우

### Step 1: 프로젝트 디렉토리 생성

- 타임스탬프 형식(`project-YYYYMMDD-HHMMSS`)으로 다음 구조를 생성합니다:

  ```
  project-{YYYYMMDD}-{HHMMSS}/
  ├── input/
  │   ├── clips/
  │   ├── skill1-output/
  │   └── music/
  ├── work/
  │   ├── S2-story/
  │   ├── S3-conti/
  │   ├── S4-prompts/
  │   ├── E1-clip-analysis/
  │   ├── E2-matching/
  │   ├── E3-timeline/
  │   └── E4-assembly/
  ├── output/
  ├── quarantine/
  └── logs/
  ```

### Step 2: PIPELINE-LOG.md 초기화

- `templates/PIPELINE-LOG.template.md`를 복사하여 루트에 `PIPELINE-LOG.md`를 생성합니다.
- 생성일, 시작 시간을 기록합니다.

### Step 3: 입력 파일 복사

- 유저가 제공한 모든 입력 파일을 `input/` 디렉토리에 복사합니다 (원본 보존).
- 파일 목록을 PIPELINE-LOG.md에 기록합니다.
- 운영 모드: MV-Story 모드 또는 Direct 모드 (01-input-gate에서 확정).

### Step 4: MCP 연결 테스트

- `config/mcp-fallback.json`을 읽어 필요한 MCP 서버 핑/헬스체크를 수행합니다.
- 결과를 기록합니다 (✅, ⚠️, ❌).

### Step 5: 예산 상한 확인

- `config/budget-limits.json`에서 파이프라인별 비용 상한을 확인합니다.
- `logs/cost.log`를 초기화합니다 (`총비용: $0.00 / 상한: $X.XX`).

### Step 6: 기존 프로젝트 재실행 감지

- 기존 프로젝트 경로인 경우, `PIPELINE-LOG.md`를 읽어 완료된 단계를 파악합니다.
- `"=== 재실행 ==="`을 기록하고 미완료 단계부터 재개합니다.

### Step 7: 결과 기록

- `PIPELINE-LOG.md`의 `## Preflight` 섹션에 통과 항목들을 기록합니다.

## 관련 파일

| File | Purpose |
|------|---------|
| `templates/PIPELINE-LOG.template.md` | 로그 템플릿 |
| `config/mcp-fallback.json` | MCP 계층 구조 설정 |
| `config/budget-limits.json` | 비용 상한 설정 |

## 예외사항

1. MCP 연결 일부 실패: 폴백 체인이 있으므로 1순위 실패만으로는 중단하지 않습니다.
2. 모든 폴백 실패: 해당 기능이 필수적일 때만 유저에게 알리고 중단 여부를 확인합니다.
