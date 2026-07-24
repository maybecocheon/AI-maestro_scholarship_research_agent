# -*- coding: utf-8 -*-
"""Dummy content that exercises every formatting element, for a format check."""

def demo():
    return {
        "title_top": "2026년 제1회",
        "title_main": "샘플 업무 추진계획 보고서",
        "date": "2026.  7. ",
        "dept": ["○○혁신본부", "○○기획과"],
        "sections": [
            {
                "number": 1, "title": "추진 개요",
                "items": [
                    {"type": "bullet", "label": "추진목적", "text": "샘플 서식이 실제 문서와 동일하게 렌더링되는지 확인하기 위한 더미 보고서"},
                    {"type": "bullet", "label": "추진근거", "text": "○○ 기본계획 및 관련 지침에 따름"},
                    {"type": "bullet", "text": "라벨이 없는 일반 글머리 항목도 정상 표시되는지 확인"},
                    {"type": "table_boxed", "header": ["구분", "설명"], "pairs": [
                        ["가형", ["첫 번째 줄 예시 내용입니다.", "두 번째 줄 예시 내용입니다.", "·세부 항목 1", "·세부 항목 2"]],
                        ["나형", "한 줄짜리 설명 예시"],
                        ["다형", ["여러 줄로 구성된", "설명 예시입니다."]],
                    ]},
                ],
            },
            {
                "number": 2, "title": "추진 일정 및 방법",
                "items": [
                    {"type": "bullet", "label": "추진일정", "text": "아래 표와 같음"},
                    {"type": "table", "headers": ["구분", "기간"], "rows": [
                        ["준비", "2026. 7. 1.(수) ~ 7. 10.(금)"],
                        ["실행", "2026. 7. 13.(월) ~ 7. 24.(금)"],
                        ["정리", "2026. 7. 27.(월)"],
                    ]},
                    {"type": "note", "text": "세부일정은 조정될 수 있음"},
                    {"type": "bullet", "label": "추진방법", "text": "단계별 세부 실행"},
                    {"type": "subbullet", "text": "1단계: 자료 조사 및 분석"},
                    {"type": "subbullet", "text": "2단계: 초안 작성 및 검토"},
                ],
            },
            {
                "number": 3, "title": "평가 및 시상",
                "items": [
                    {"type": "bullet", "label": "배점기준", "text": "항목별 합산"},
                    {"type": "table",
                     "headers": ["기준", "내용", "배점"],
                     "widths": [2, 6, 2],
                     "rows": [
                        ["실용성", "실제 업무에 활용 가능한 정도", "40점"],
                        ["창의성", "차별화되는 아이디어 여부", "30점"],
                        ["명확성", "목적과 내용의 명확성", "30점"],
                     ],
                     "total": ["계", "", "100점"]},
                    {"type": "note", "text": "수상 내역은 심사 결과에 따라 조정될 수 있음"},
                ],
            },
            {
                "number": 4, "title": "행정사항",
                "items": [
                    {"type": "bullet", "text": "제출된 서류는 반환하지 않으며 관련 규정에 따라 처리함"},
                    {"type": "bullet", "text": "문의: ○○기획과 (051-000-0000)"},
                ],
            },
        ],
        "annexes": [
            {"type": "annex", "label": "붙임 1", "title": "참가신청서"},
            {"type": "bullet", "text": "붙임 페이지의 본문 예시입니다."},
        ],
    }
