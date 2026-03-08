# MCP 서버 레지스트리

> Music Video Generation Skill에서 사용하는 MCP 서버 전체 목록

---

## A. 영상 생성 (img2vid / txt2vid)

| MCP | 용도 | 비고 |
|-----|------|------|
| **agent-media** (yuvalsuede) | Kling, Veo, Sora, Seedance 등 7개 모델 통합 | 핵심 — 멀티모델 영상 생성 허브 |
| **WaveSpeed** | 이미지 및 비디오 생성 | 빠른 생성 |
| **JSON2Video** | JSON 기반 프로그래밍 방식 비디오 생성 | 콘티→영상 자동화 |
| **PiAPI** | Midjourney/Flux/Kling/Hunyuan/Udio/Trellis 통합 | 멀티모달 미디어 허브 |

---

## B. 이미지 생성 (txt2img / img2img)

| MCP | 용도 |
|-----|------|
| **Pixelle** | ComfyUI 워크플로우를 MCP 도구화 — txt/img/sound/video |
| **comfy-pilot** | ComfyUI 워크플로우 직접 제어 |
| **Fal MCP Server** | FLUX, Stable Diffusion, MusicGen |
| **Replicate** | 범용 ML 모델 허브, Flux 등 |

---

## C. 영상 편집/합성

| MCP | 용도 |
|-----|------|
| **atsurae** (1000ri-jp) | AI 영상 편집, 5레이어 합성, FFmpeg 렌더링 |
| **ffmpeg-mcp** (video-creator) | FFmpeg 기반 로컬 비디오 편집/이어붙이기 |
| **video-edit-mcp** | 트리밍, 병합, 이펙트, 오버레이, 포맷 변환, 오디오 처리 |
| DaVinci Resolve MCP | 전문 영상 편집, 색보정 (선택) |

---

## D. 음악/오디오

| MCP | 용도 |
|-----|------|
| **Mureka** | 가사/노래/배경음악 생성 |
| **Fal MCP (MusicGen)** | AI 음악 생성 |
| **ElevenLabs** | TTS, 음성 복제 |
| **Fish Audio** | 다중 음성 TTS + 스트리밍 |
| **AllVoiceLab** | TTS, 음성 복제, 비디오 번역 |
| Suno (vap-showcase) | Flux+Veo+Suno 통합, 비용 제어 |

---

## E. 분석/유틸리티

| MCP | 용도 |
|-----|------|
| **Probe.dev** | FFprobe/MediaInfo 미디어 분석 검증 |
| **VisionAgent** | 이미지/비디오 추론 분석 |
| Cloudinary | 미디어 업로드/변환/AI 분석 |
| Transcribe | 오디오/비디오 전사 |

---

## F. 애니메이션 특화 (P3 전용)

| MCP | 용도 |
|-----|------|
| Allyson | 정적 파일→애니메이션 SVG 변환 |
| TouchDesigner MCP | 인터랙티브 미디어/비주얼 제어 |

---

## 폴백 체인 요약

| 기능 | 1순위 | 2순위 | 폴백 |
|------|-------|-------|------|
| 이미지 생성 | Pixelle (ComfyUI) | comfy-pilot | Fal / Replicate |
| 영상 생성 | agent-media (Kling+) | PiAPI | Fal |
| BGM 생성 | Mureka | Fal (MusicGen) | Suno |
| TTS/내레이션 | ElevenLabs | Fish Audio | AllVoiceLab |
| 편집/합성 | atsurae | ffmpeg-mcp | video-edit-mcp |
| 미디어 분석 | Probe.dev | ffprobe (로컬) | VisionAgent |

---

## 주의사항

- **프로덕션급 안정성**: agent-media, Fal, ElevenLabs, ffmpeg-mcp 정도만 프로덕션급
- **API 키 관리**: 환경변수/시크릿 매니저에서만 관리, 에이전트 컨텍스트 진입 차단
- **Rate Limit**: MCP별 분당 호출 상한 존재, `config/mcp-fallback.json` 참조
