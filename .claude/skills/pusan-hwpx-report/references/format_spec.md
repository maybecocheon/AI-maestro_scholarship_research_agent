# 서식 내부 규칙 (유지보수용)

이 문서는 `build_report.py`가 참조하는 원본 스타일 ID 매핑과, 한글에서 렌더링을 검증하는 방법을 정리한다.
원본 예시 파일: `2026년 제2회 산지니 AI 활용 사례 공모전 추진계획.hwpx`.

## 패키지 구성

```
assets/template/            # 원본 HWPX를 통째로 보존 (이 자원들이 서식의 전부)
├── Contents/header.xml     # 폰트/글자/문단/테두리 스타일 정의 — 절대 수정 금지
├── Contents/section0.xml   # 원본 본문. 빌더는 이 파일의 <hp:p> 앞부분(secPr 포함 sec 열기 태그)만 재사용
├── BinData/image1.jpg      # 대학 로고(부산대 서명)
├── settings.xml, version.xml, META-INF/, Scripts/, Preview/, mimetype
assets/frag_cover.xml       # 표지 블록(PARA 0~6) 원본 그대로 + placeholder 4개
scripts/build_report.py     # 본문 조립기
scripts/demo_spec.py        # 모든 요소를 쓰는 더미 스펙
```

빌드 절차: 템플릿을 임시 폴더로 복사 → `Contents/section0.xml`을 새로 씀(sec 열기 태그는 원본에서 그대로
따오고 그 뒤 본문을 조립) → mimetype을 STORED로 먼저 넣어 다시 zip.

## 표지 placeholder

`frag_cover.xml` 안의 치환 지점: `{{TITLE1}}`, `{{TITLE2}}`, `{{DATE}}`, `{{DEPT_PARAS}}`.
부서 줄은 `paraPrIDRef=20 / charPrIDRef=14` 문단을 줄 수만큼 생성해 `{{DEPT_PARAS}}`에 넣는다.

## 스타일 ID 매핑 (원본에서 채취)

### 문단(paraPrIDRef)
| ID | 용도 |
|----|------|
| 0  | 첫 문단(secPr 보유, 표지 표) |
| 13 | 기본(justify) — ※ 각주, 표 셀 |
| 16/17/18 | 표지 여백/날짜 문단(prev 6000·6000·4000) |
| 20 | 표지 부서명(center) |
| 23 | 절 표제 감싸는 문단 |
| 21/22 | 절 번호칸 / 제목칸 |
| 24 | ◦ 글머리, - 하위 글머리(내어쓰기 -3014) |
| 25/26/27/28 | 표 셀(머리행/라벨/내용/다단내용) |
| 33/34 | 그리드 표 머리행/본문 셀 |
| 50/51/61 | 붙임 표 셀/감싸는 문단 |

### 글자(charPrIDRef)
| ID | 용도 |
|----|------|
| 10 | 표지 큰 제목(HY헤드라인M) · 11 표지 윗줄 · 12 날짜 · 14 부서명 |
| 16/17 | 절 번호(흰색) / 절 제목 |
| 18 | ◦ 마크 · 19 (라벨) 굵게 · 20 본문 |
| 22 | 표 머리행(굵게) · 23 표 본문 · 24 표 다단 내용 |
| 27 | ※ 각주 · 29 그리드 표 머리행 |
| 49/50/51 | 붙임 번호/여백/제목 |

### 테두리·채움(borderFillIDRef)
| ID | 용도 |
|----|------|
| 4  | 표 외곽 테두리(SOLID 박스) · 3 외곽 없음(그리드용) |
| 6/7/9/10 | 표지 상·하단 블루 그라데이션 막대 |
| 8  | 표지 제목 셀(#F1F1F1) |
| 11/12 | 부서 표 로고칸/텍스트칸 |
| 13 | 절 번호 박스(navy #3E57A5) · 14 절 제목칸(아래 밑줄) |
| 15/16 | 박스표 머리행(#DFE6F7) L/R |
| 17·19·21 / 18·20·22 | 박스표 본문 L열(첫/중간/끝) / R열(첫/중간/끝) |
| 23/24/25 | 그리드표 머리행 첫/중간/끝 열(#DFE6F7) |
| 26·29·32 등 | 그리드표 본문 첫/중간/끝 행 (열 위치별 3종) |
| 35/36/37 | 그리드표 **계** 행(#FFF7CC 옅은 노랑) |
| 38/39/40 | 붙임 표제 cyan 번호칸(#079FCE)/여백/제목칸 |

그리드 표 본문 borderFill 규칙(`build_report.GRID`):
- 머리행: 23/24/25
- 본문 첫 행: 26/27/28, 중간 행: 29/30/31, 끝 행(계 없을 때): 32/33/34
- 계 행: 35/36/37
- 열 위치: 0열=first, 마지막열=last, 그 외=middle

## 한글로 열어 확인 (PowerShell + COM)

한컴오피스가 설치돼 있으면(`...\HOffice110\Bin\Hwp.exe`) 아래로 실제 렌더링/페이지 수를 확인하고
PDF로 내보낼 수 있다. 보안 대화상자가 뜨면 멈출 수 있으니 타임아웃과 함께 백그라운드로 돌린다.

```powershell
param($src,$pdf)
$hwp = New-Object -ComObject 'HWPFrame.HwpObject'
try { $hwp.RegisterModule('FilePathCheckDLL','FilePathCheckerModule') } catch {}
try { $hwp.SetMessageBoxMode(0x20) } catch {}   # 대화상자 억제
$null = $hwp.Open($src, '', '')
Write-Output ("PageCount: " + $hwp.PageCount)
$null = $hwp.SaveAs($pdf, 'PDF', '')            # 전체 페이지 PDF 내보내기
$hwp.Quit()
```

PDF를 이미지로 볼 때는 `pymupdf`(`pip install pymupdf`)로:
`fitz.open(pdf)[i].get_pixmap(dpi=96).tobytes('png')`.

> 주의: MuPDF의 JPEG 디코더가 로고 이미지를 못 읽는 경우가 있는데(첫 렌더 시 경고), 서식과는 무관하다.
> `FileSaveAsPdf` 액션은 현재 페이지만 내보낼 때가 있으니 위처럼 `SaveAs(...,'PDF',...)`를 쓴다.

## 확장 여지

- 원본에는 참가신청서·개인정보 동의서 같은 전용 서식(입력칸 표, 체크박스 □)이 붙임에 더 있다.
  이 스킬은 보고서 본문 골조(표지·절·글머리·표·붙임 표제)에 집중한다. 그런 정형 폼이 필요하면
  원본 `section0.xml`의 해당 PARA(붙임 1/2/3 표)를 조각으로 떠서 `table_boxed`처럼 함수화하면 된다.
