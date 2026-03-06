---
name: harness-02-analyze
description: >
  유저 요청에서 필요한 외부 서비스를 식별하고(MCP Router), 작업에 맞는 시스템 프롬프트를 생성한다(Instruction Generator).
  "MCP 연동", "어떤 MCP 써야 해", "지침 만들어줘" 등의 요청에서 Analyst 팀원이 실행한다.
---

# 02-analyze: MCP Router + Instruction Generator

> **실행자**: Analyst (Teammate 1)
> **실행 시점**: 01-complexity 완료 후
> **쓰기 권한**: `work/analysis/` 만
> **특이사항**: simple 태스크에서 서비스 키워드 없으면 스킵 가능

## 목적

두 가지 분석 작업을 수행한다:

1. **MCP Router** — 태스크 수행에 필요한 외부 서비스를 식별하고 최적 MCP 서버를 추천
2. **Instruction Generator** — 도메인에 맞는 system prompt를 생성하여 03-forge(스킬 생성)의 품질을 높임

## 실행 시점

- 01-complexity 완료 후 Leader가 Analyst를 호출하면 실행.
- 복잡도 composite/research일 때 항상 실행; simple은 서비스 키워드 있을 때만 실행.

## 워크플로우

### Step 1: MCP Router 실행

1. 유저 요청에서 서비스 키워드 추출 (Slack, Gmail, GitHub, Notion 등)
2. `view_file("../../mcp-router/SKILL.md")` 동적 로딩 후 매핑 테이블 참조
3. 매칭 실패 시: `grep_search(키워드, "..'/Awesome-MCP-Servers-한국어-가이드.md'")`로 검색
4. 결과를 `work/analysis/mcp-result.json`에 저장:

   ```json
   {
     "matched_servers": [{ "name": "...", "status": "...", "install_guide": "..." }],
     "fallback": null
   }
   ```

5. 매칭된 MCP가 있으면 유저에게 설치 안내 메시지 표시

### Step 2: Instruction Generator 실행

1. `view_file("../../instruction-gen/SKILL.md")` 동적 로딩
2. 도메인 판정 후 Extension 조합:
   - **code** → 언어/프레임워크/린트 Extension
   - **analysis** → 데이터소스/분석프레임 Extension
   - **writing** → 톤/독자/구조 Extension
   - **integration** → MCP 설정/인증/에러핸들링 Extension
   - **skill** → YAML frontmatter/섹션구조/품질기준 Extension
3. 토큰 잔여량에 따라 CoT Scaffold 조정:
   - 잔여 < 2,000: CoT 2단계 + 예시 제거
   - 잔여 ≥ 5,000: CoT 4단계 + Do/Don't 예시 포함
4. 생성된 지침을 `work/analysis/system-prompt.md`에 저장

### Step 3: PIPELINE-LOG 기록

```
## T1: 분석 (Analyst)
- MCP 매칭: {서버명 또는 "없음"}
- 지침 생성: {도메인} ({CoT 단계}단계)
- 완료: {시각}
```

## 관련 파일

| File | Purpose |
|------|---------|
| `../../mcp-router/SKILL.md` | MCP 서버 매핑 테이블 |
| `../../instruction-gen/SKILL.md` | 지침 생성 템플릿 |
| `../../Awesome-MCP-Servers-한국어-가이드.md` | MCP 카탈로그 (폴백 검색) |
| `03-forge.md` | 다음 단계 (Builder) |

## 예외사항

1. **MCP 매칭 실패**: `fallback="no_mcp"` 기록 후 계속 진행 (MCP 없이 스킬 생성 가능)
2. **단순 지침 생성 작업**: Instruction Gen만 실행하고 MCP Router는 스킵
