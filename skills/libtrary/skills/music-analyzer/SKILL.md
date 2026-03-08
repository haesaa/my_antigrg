---
name: music-analyzer
description: >
  독립형 프론트엔드 유틸리티 스킬. 브라우저 기반 HTML을 통해 오디오 파일을 분석하고 BPM, Key, Section 등의 정보를 추출하여 `music-meta.json` 형태로 변환합니다.
---

# 🎵 Music Analyzer Skill

> **실행자**: User (브라우저를 통한 수동 실행) 혹은 Agent (Puppeteer 등 브라우저 제어시)
> **환경**: 로컬 브라우저 (Chrome/Edge 등)
> **저장소 경로**: `c:\hehe\skills-main\outomidea\music-analyzer\`

## 목적

Audio 파일을 브라우저 상의 Web API (AudioContext) 및 분석 로직을 통해 분석하여, 후속 영상 생성 파이프라인(`1.music_video` 스킬 등)에서 요구하는 `music-meta.json` 혹은 `music-meta.md` 형태의 규격화된 데이터를 산출하는 프론트엔드 도구 모음입니다.

본 스킬은 다른 백엔드/CLI 스킬들과 달리 브라우저 위에서 실행되므로, 에이전트는 직접 코드를 실행하기보다는 가이드나 구조를 파악하고 사용자에게 사용 안내를 하는 목적으로 참조합니다.

## 구성 요소

| 파일명 | 용도 | 설명 |
|---|---|---|
| `음원분석.html` | 메인 분석기 UI | 사용자가 mp3/wav 파일을 드래그앤드롭하여 분석. BPM, Key, Section 등위 정보를 시각화하고 JSON이나 클립보드로 내보냄. |
| `원본음원분석.html` | 레거시 분석기 | 구버전 분석기로, 크로마그램 및 에너지 기반 스펙트럼 분석을 집중적으로 수행하던 기존 로직. 백업 및 참조용. |
| `music-meta.md` | 예시 출력 포맷 | 분석된 결과가 마크다운으로 어떻게 출력되는지에 대한 예시 샘플. |

## 사용 파이프라인 흐름 (Agent 가이드용)

1. **사용자 요청 시**: 유저가 "음원을 넣을 테니 뮤직비디오를 만들어줘" 라고 하나, 음원에 대한 메타데이터가 없다면?
2. **도구 안내**: 에이전트는 유저에게 `c:\hehe\skills-main\outomidea\music-analyzer\음원분석.html` 파일을 브라우저로 열어 음원을 분석하라고 안내합니다.
3. **결과물 확보**: 유저가 도구에서 파싱해낸 `music-meta.json` 텍스트를 복사-붙여넣기 하거나 파일로 첨부하도록 유도합니다.
4. **후속 스킬 연계**: 확보된 `music-meta.json`을 `1.music_video` 파이프라인의 `01-input-gate`에 전달합니다.

## 내부 로직 구조 참조

에이전트가 코드를 유지보수할 일이 생기면 다음 기술 스택을 참고하세요:

- **진입점**: HTML5, Vanilla JavaScript.
- **오디오 처리**: Web Audio API (`AudioContext`, `OfflineAudioContext`).
- **피쳐 추출 분석**: 에너지(RMS) 연산, onset detection, 로컬 미니마/맥시마 알고리즘.
- **외부 파일 의존성 없음**: 단일 HTML 파일 내부에 JS/CSS가 내장된 형태 (오프라인 구동 가능).
