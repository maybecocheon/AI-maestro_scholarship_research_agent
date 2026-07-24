---
description: 조사원 5명(정책·거점국립대·주요사립대·특수대학·공시)을 동시 실행해 주제를 리서치하고, 편집장이 사용자와 상의해 보고서 목차·스토리라인을 확정한다. 인자로 주제를 받으며 기본값은 "타대학 장학 제도".
argument-hint: "[리서치 주제] (생략 시 '타대학 장학 제도')"
---

# 장학 제도 리서치 → 목차·스토리라인 확정 파이프라인

리서치 주제: **$ARGUMENTS** (비어 있으면 "타대학 장학 제도"로 진행)

아래 절차를 **순서대로** 수행하세요. 조사 단계는 반드시 병렬입니다.

## 0. 사전 점검
- agent-browser 스킬 설치 확인: `~\.claude\skills\agent-browser\SKILL.md` 존재 여부. 없으면 사용자에게 알리고 설치(`npx skills add vercel-labs/agent-browser --global --yes --agent claude-code`, `npm i -g agent-browser`, `agent-browser install`) 후 진행. Chrome 실행은 `--args "--no-sandbox"` 필수.
- 출력 폴더 준비: `research\`, `report\` (없으면 생성). **한글 보고서(HWP/HWPX) 변환 작업 파일은 절대 건드리지 말 것.**

## 1. 조사원 5명 동시 실행 (병렬)
Agent 도구 호출 5개를 **한 메시지에 함께** 보내 동시에 실행합니다. 순차 금지.
각 조사원 리서치 시간은 약 15분(핵심 페이지 8~12개) 소프트 캡. 각자 결과를 지정 md에 저장.

- `researcher-policy` → `research\01_policy_정책조사원.md`
- `researcher-natl-univ` → `research\02_natl_거점국립대.md`
- `researcher-private-univ` → `research\03_private_주요사립대.md`
- `researcher-special-univ` → `research\04_special_특수대학.md`
- `researcher-disclosure` → `research\05_disclosure_공시조사원.md`

각 조사원 프롬프트에 리서치 주제("$ARGUMENTS")를 전달하세요. (해당 서브에이전트 타입이 없으면 general-purpose로 실행하되, 각 에이전트 정의 파일 `.claude\agents\researcher-*.md`의 지침을 프롬프트에 그대로 넣어 자기완결적으로 실행)

5개가 모두 끝나면 5개 md 파일이 생성됐는지 확인하고 사용자에게 간단히 보고.

## 2. 편집장 종합 → 제안서
`editor-in-chief` 서브에이전트를 실행해 5개 md를 읽고 **제안서**(종합 인사이트 / 목차안 / 언급할 점 / 언급하되 가릴 점 / 스토리라인 순서 후보 / 사용자 질문)를 텍스트로 받으세요.

## 3. 사용자와 상의해 확정 (필수, 혼자 정하지 말 것)
편집장 제안서를 바탕으로 **AskUserQuestion**으로 사용자와 확정합니다. 최소 다음 3개 축을 물으세요:
1. **언급할 점**(강조 포인트) — 무엇을 전면에 둘지
2. **언급하되 가릴 점** — 어떤 민감/불확실 항목의 톤을 낮출지
3. **이야기 순서(스토리라인)** — 후보안 중 택1 또는 수정
필요하면 추가 질문. 사용자가 수정 요청하면 반영해 재확인.

## 4. 최종 저장
확정된 내용을 `report\목차_스토리라인.md`에 저장(메인 에이전트가 저장; 편집장이 아님). 구성:
- 보고서 제목(안), 대상 독자, 핵심 메시지 한 문장
- 확정 목차(대·소제목 트리)
- 절별 스토리라인(무엇을·어떤 근거로·어떤 순서로)
- "강조할 점 / 톤 낮출 점" 명시
- 각 절의 근거 자료(어느 조사원 md·수치 인용)
- 다음 단계 메모: "한글(HWPX) 보고서 변환은 별도 세션/스킬에서 진행 — 본 파이프라인은 목차·스토리라인 확정까지"

## 산출물 요약
- `research\01~05_*.md` (조사원별 원자료)
- `report\목차_스토리라인.md` (사용자 확정 결과)
