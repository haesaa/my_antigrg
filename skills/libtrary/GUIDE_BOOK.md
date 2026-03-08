# 📖 Skill Factory Library — 쉬운 가이드북

> **대상**: 처음 보는 사람도 이해할 수 있게 쓴 안내서  
> **작성일**: 2026-03-06  
> **경로**: `c:\hehe\skills-copy\library\`

---

## 🔑 한 줄 요약

> **"AI에게 새로운 기능(Skill)을 안전하게 추가하는 공장(Factory)"**

---

## 🗺️ 전체 그림 — 레고에 비유하면

이 시스템은 레고 공장과 똑같이 생겼어요.

```
📋 설계도 (Blueprint)
  → 🔍 검사 (Validator)
    → 🏗️ 조립 (Builder)
      → 📦 등록 (Registry)
```

**핵심 규칙 딱 하나:**  
> AI(에이전트)는 절대 혼자서 기능 파일을 만들면 안 돼요.  
> 반드시 이 공장 파이프라인을 통해야만 만들 수 있어요.

왜냐고요? AI가 혼자 만들면 **엉뚱한 걸 만들거나 중복이 생길 수 있거든요.**

---

## 🏠 폴더 구조 — 방 배치도

```
library/                        ← 🏠 집 전체
│
├── 📘 GUIDE_BOOK.md            ← 지금 이 파일!
├── 📋 README.md                ← 개발자용 요약
├── 📓 _WORK_LOG.md             ← 작업 일지 (무엇을 했는지)
├── 📇 skill_registry.json      ← 만들어진 Skill 명단
├── 🗂️ catalog.json             ← 시스템 지도
│
├── 🏭 FACTORY/                 ← 공장 구역
│   ├── 🔧 pipeline_runner.py   ← 공장 자동 실행기 (메인!)
│   ├── 🛠️ skill_manager.py     ← 기능 추가/삭제/수정 도구
│   ├── 📁 blueprints/          ← 설계도 보관함
│   │   ├── skill_blueprint_schema.json   ← 설계도 양식
│   │   ├── example_blueprint.json        ← 예시 (kpi_manager)
│   │   └── data_cleaner_blueprint.json   ← 예시 (data_cleaner)
│   ├── 🔍 validators/          ← 검사실
│   │   ├── validate_blueprint.py         ← 검사 함수
│   │   └── test_blueprint_validation.py  ← 자동 테스트
│   └── 🔨 builders/            ← 조립실
│       ├── skill_builder.py              ← 조립 함수
│       └── test_skill_builder.py         ← 자동 테스트
│
├── 📚 LIBRARY/                 ← 도서관 구역
│   ├── 📖 guides/              ← 참고서 모음
│   ├── 📝 instructions/        ← 작업 설명서 모음
│   ├── 🔗 graph/               ← 목록 관리 (무엇이 있는지)
│   ├── 🔧 tools/               ← 도구 명단
│   └── 💾 memory/              ← 실행 기록
│
├── 🤖 skill_writer/SKILL.md    ← "설계도 쓰는" Skill
├── 🤖 skill_agent/SKILL.md     ← "어떤 Skill 쓸지 골라주는" Skill
└── 🤖 skills/                  ← 완성된 Skill들
    ├── kpi_manager/SKILL.md
    └── data_cleaner/SKILL.md
```

---

## ⚙️ 공장 파이프라인 — 기능 하나 만드는 5단계

### 예시: "CSV 파일을 깨끗하게 정리하는 기능" 만들기

---

### 1단계 🖊️ — 설계도(Blueprint) 작성

`FACTORY/blueprints/` 안에 JSON 파일로 설계도를 써요.

```json
{
  "skill_name": "data_cleaner",
  "entry_instruction": "clean_csv",
  "instructions": ["clean_csv", "remove_duplicates"],
  "guides": ["blueprint_writing_guide"],
  "tools": ["python_exec", "file_write"]
}
```

**쉽게 풀면:**

- `skill_name` → 기능 이름 (영어 소문자, 언더스코어만)
- `entry_instruction` → 처음에 실행하는 동작
- `guides` → 참고할 참고서 목록
- `tools` → 사용하는 도구 목록

---

### 2단계 🔍 — 검사(Validator) 통과

5가지 규칙을 자동으로 검사해요.

| 규칙 | 검사 내용 | 실패하면? |
|------|----------|----------|
| 규칙 1 | 이름이 이미 있는 건 아닌가? | "이름 중복!" |
| 규칙 2 | entry_instruction이 비어있지 않은가? | "실행 동작 없음!" |
| 규칙 3 | guides가 있는가? | "참고서 없음!" |
| 규칙 4 | instructions이 목록에 있는 것인가? | "없는 동작!" |
| 규칙 5 | tools가 목록에 있는 것인가? | "없는 도구!" |

---

### 3단계 🔨 — 조립(Builder) 실행

검사를 통과하면 자동으로 파일이 만들어져요.

```
skills/
└── data_cleaner/
    └── SKILL.md   ← 이게 자동으로 생겨요!
```

---

### 4단계 📇 — 명단(Registry) 등록

`skill_registry.json`에 자동으로 추가돼요.

```json
{
  "skills": [
    { "name": "kpi_manager", "entry_instruction": "calculate_kpi" },
    { "name": "data_cleaner", "entry_instruction": "clean_csv" }
  ]
}
```

---

### 5단계 💾 — 기록(Memory) 저장

언제 어떤 기능을 만들었는지 `LIBRARY/memory/session_memory.json`에 저장돼요.

---

## 🚀 실제로 실행하는 방법

### 새 Skill 한 번에 만들기

```powershell
cd c:\hehe\skills-copy\library\FACTORY

# kpi_manager Skill 만들기
python pipeline_runner.py blueprints\example_blueprint.json

# data_cleaner Skill 만들기
python pipeline_runner.py blueprints\data_cleaner_blueprint.json
```

**화면에 이렇게 나오면 성공! ✅**

```
[FACTORY] Skill Factory Pipeline Starting...

[1] Blueprint loaded: data_cleaner
[2] OK Validation PASSED
[3] OK Skill built: ...\skills\data_cleaner\SKILL.md
[4] OK Skill registered in skill_registry.json
[5] OK Session memory updated

[DONE] Pipeline Complete: data_cleaner
```

---

## ➕➖✏️ CRUD — 기능 추가 / 삭제 / 수정

### 추가 (CREATE)

1. `FACTORY/blueprints/` 안에 새 Blueprint JSON 파일 작성
2. `python pipeline_runner.py 파일이름.json` 실행

### 삭제 (DELETE)

```python
# skill_manager.py 사용
from skill_manager import delete_skill
delete_skill("data_cleaner")  # registry에서 제거 + 폴더 삭제
```

### 수정 (UPDATE)

```python
from skill_manager import update_skill
update_skill("data_cleaner", 새_blueprint_dict)
```

### 목록 보기 (READ)

```python
from skill_manager import list_skills
print(list_skills())  # ['kpi_manager', 'data_cleaner']
```

---

## 📚 도서관(LIBRARY) — 참고서 목록

`LIBRARY/guides/` 안에 있는 참고서들:

| 파일 | 설명 | 사용처 |
|------|------|--------|
| `blueprint_writing_guide.md` | 설계도 작성법 | Skill 만들 때 |
| `skill_naming_guide.md` | 이름 짓는 규칙 | Skill 이름 지을 때 |
| `validation_rules_guide.md` | 5개 검사 규칙 설명 | 검사 이해할 때 |
| `REFERENCE-prompt-and-frame-guide.md` | 영상/MV 프롬프트 키워드 | 영상 관련 Skill 만들 때 |
| `romance_guide.md` | 로맨스 문체·기법 가이드 | 글쓰기 Skill 만들 때 |
| `typology_reference.md` | 캐릭터 성격 유형 참고서 | 캐릭터 Skill 만들 때 |
| `psy_love_theories.md` | 사랑·관계 심리학 이론 통합 가이드 | 로맨스 및 인간관계 시나리오 작성 시 |
| `psy_motivation_theories.md` | 동기부여 및 심리 이론(자기결정성 등) 통합 가이드 | 행동 동기 및 성장 서사 작성 시 |
| `psy_trauma_defense.md` | 복합 외상(C-PTSD) 및 방어기제 가이드 | 트라우마 및 갈등 서사 작성 시 |
| `psy_limerence.md` | 리머런스(Limerence) 메커니즘 가이드 | 정서적 집착, 짝사랑 관련 서사 작성 시 |
| `psy_nonviolent_communication.md` | 비폭력대화(NVC) 실천 가이드 | 평화적 갈등 해결 대화 작성 시 |
| `psy_love_and_jealousy.md` | 사랑과 질투 심리학 서사 가이드 | 파괴석 감정 및 극복 서사 작성 시 |
| `psy_transactional_analysis.md` | 에릭 번의 교류분석(TA) 이론 가이드 | 대인관계 심리 게임 시나리오 작성 시 |
| `psy_bl_romance_guide.md` | BL 및 로맨스 장르 분석 대백과사전 | BL/로맨스 캐릭터 유형 및 키워드 설정 시 |
| `model_profiles.md` | 언어 모델별 프롬프트 최적화 규칙 레퍼런스 | 각 모델에 특화된 프롬프트 작성 시 |

---

## 📝 설명서(instructions) — 동작 상세 설명

`LIBRARY/instructions/` 안에 있어요:

| 파일 | 어떤 Skill의 동작? | 하는 일 |
|------|-----------------|---------|
| `calculate_kpi.md` | kpi_manager | KPI 숫자 계산 |
| `generate_character.md` | character_writer | 캐릭터 시트 생성 |
| `write_blueprint.md` | skill_writer | 새 설계도 작성 |
| `clean_csv.md` | data_cleaner | CSV 파일 정제 |

---

## 🔗 목록(Graph) — 뭐가 있는지 관리

`LIBRARY/graph/` 안에 있어요:

- **`guide_graph.json`** → 어떤 참고서가 있는지 목록 (Validator 규칙 3에서 사용)
- **`instruction_graph.json`** → 어떤 동작이 있는지 목록 (Validator 규칙 4에서 사용)

> 새 참고서나 동작을 추가하면 여기도 꼭 업데이트해야 해요!

---

## ✅ 테스트 — 잘 작동하는지 확인하기

```powershell
# 검사 기능 테스트 (10개 전부 통과해야 함)
cd FACTORY\validators
python -m pytest test_blueprint_validation.py -v

# 조립 기능 테스트 (5개 전부 통과해야 함)
cd FACTORY\builders
python -m pytest test_skill_builder.py -v

# CRUD 기능 테스트 (4개 전부 통과해야 함)
cd FACTORY
python -m pytest test_skill_manager.py -v
```

**총 19개 테스트, 전부 PASSED ✅**

---

## ⚠️ 이것만은 꼭 지켜요

> 1. **SKILL.md를 직접 만들지 말 것** → 반드시 pipeline_runner.py로만
> 2. **새 동작 추가 시** → `instruction_graph.json`에도 등록
> 3. **새 참고서 추가 시** → `guide_graph.json`에도 등록
> 4. **새 도구 추가 시** → `LIBRARY/tools/tool_registry.json`에도 등록
> 5. **가이드 파일 읽을 때** → `Do not open guide files directly.` / `Always read section index first.` / `guide <= 300 tokens`

---

## 🏷️ 예약된 파일 이름 (쓰면 안 됨)

library namespace 충돌을 막기 위해 아래 이름은 사용 금지:

- `writing_style.md`
- `rules_security.md`

---

## 📞 뭔가 막히면?

| 상황 | 확인할 파일 |
|------|------------|
| 전체 작업 흐름 궁금 | `_WORK_LOG.md` |
| 시스템 구조 보기 | `README.md` |
| Validator 오류 | `LIBRARY/guides/validation_rules_guide.md` |
| Skill 설계 방법 | `LIBRARY/guides/blueprint_writing_guide.md` |
| 이름 짓기 규칙 | `LIBRARY/guides/skill_naming_guide.md` |
