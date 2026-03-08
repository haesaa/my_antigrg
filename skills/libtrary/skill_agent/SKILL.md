---
name: skill_agent
description: skill_registry.json을 기반으로 적합한 Skill을 선택하고 실행하는 Routing Agent Skill
---

# Skill Skill Agent

entry_instruction

route_skill

---

## Guides

- skill_routing_guide
- registry_lookup_guide

---

## Tools

- file_read
- python_exec

---

## Instructions

### route_skill

1. `skill_registry.json`을 읽어 등록된 Skill 목록을 불러온다
2. 사용자 요청을 분석하여 적합한 Skill을 선택한다
3. 선택된 Skill의 `entry_instruction`을 실행한다
4. 실행 결과를 반환한다

**Rule**: registry에 없는 Skill은 실행하지 않는다.  
**Rule**: 새 Skill이 필요하면 `skill_writer`로 라우팅한다.
