# 타대학 장학 제도 리서치 에이전트

조사원·편집장 서브에이전트로 주제를 병렬 리서치하고, 편집장이 사용자와 상의해 보고서 목차·스토리라인을 확정하는 멀티에이전트 파이프라인입니다. 세팅 주제는 **"타대학 장학 제도"**(부산대학교 벤치마킹 관점).

## 구성

### 서브에이전트 (`.claude/agents/`)
| 역할 | 파일 | 담당 |
|---|---|---|
| 정책 조사원 | `researcher-policy.md` | 교육부·한국장학재단 정책·공고 |
| 타대학(거점국립대) | `researcher-natl-univ.md` | 서울대·부산대·경북대·전남대·충남대 교내 장학 |
| 타대학(주요 사립대) | `researcher-private-univ.md` | 연세·고려·성균관·한양·이화·경희·중앙·서강 |
| 타대학(특수대학) | `researcher-special-univ.md` | 과기원·교대·사관/경찰대·폴리텍 |
| 공시 조사원 | `researcher-disclosure.md` | 대학알리미 장학금 지표 |
| 편집장 | `editor-in-chief.md` | 5개 결과 종합 → 목차·스토리라인 *제안*(단독 확정 금지) |

### 오케스트레이터 (`.claude/commands/`)
- `scholarship-research.md` → `/scholarship-research "[주제]"` (기본 "타대학 장학 제도")
  1. 조사원 5명 **동시 실행**(각 ~15분 상한), 결과를 `research/01~05_*.md`로 각각 저장
  2. 편집장 종합 → 제안서
  3. **사용자와 상의**해 언급할 점·가릴 점·이야기 순서 확정
  4. `report/목차_스토리라인.md` 저장

### 산출물
- `research/01~05_*.md` — 조사원별 원자료 (각 기관 사이트 직접 수집)
- `report/목차_스토리라인.md` — 사용자 확정 목차·스토리라인
- `report/타대학_장학제도_벤치마킹_보고서_초안.md` — 본문 초안

## 사전 요구
- [agent-browser](https://github.com/vercel-labs/agent-browser) 스킬(유저 스코프) + Node.js. 이 PC에서는 Chrome 실행 시 `--args "--no-sandbox"` 필요.

## 재실행
새 Claude Code 세션에서 `/scholarship-research "주제"` 한 번으로 조사→목차 확정까지 재현됩니다.

> 한글(HWPX) 보고서 변환은 별도 세션/스킬에서 진행합니다.
