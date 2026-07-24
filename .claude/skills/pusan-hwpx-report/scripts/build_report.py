#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a HWPX report in the "부산대 추진계획" house style.

Design principle — FORMAT FIDELITY BY PRESERVATION
--------------------------------------------------
The visual identity of this document (fonts, page margins, the blue-gradient
title table, the navy numbered-section boxes, the light-blue table header rows,
the embedded university signature logo) lives entirely in resources that are
tedious and error-prone to regenerate from scratch: header.xml defines 8 fonts,
59 border/fill styles, 86 character styles and 71 paragraph styles, and
BinData/image1.jpg holds the logo.

So we DO NOT rebuild those. We keep the whole template package byte-for-byte
(assets/template/) and only rewrite Contents/section0.xml — the body — reusing
the exact style IDs the original author chose. Every element below emits XML
that references those preserved IDs, which is why swapping in different text
leaves the formatting untouched.

Content is supplied as a plain Python dict (see report_spec() / demo at bottom,
or pass a JSON file). Layout numbers (line heights etc.) are only first-open
hints — Hangul recomputes them on load, so they never need to be exact.
"""
import os, re, sys, json, shutil, zipfile, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TEMPLATE = os.path.join(SKILL, "assets", "template")
COVER_FRAG = os.path.join(SKILL, "assets", "frag_cover.xml")

# ---------------------------------------------------------------- helpers
def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def lineseg(vs=1200, horz=45352):
    """A single cached line segment. Values are first-open hints; Hangul reflows."""
    return (f'<hp:linesegarray><hp:lineseg textpos="0" vertpos="0" vertsize="{vs}" '
            f'textheight="{vs}" baseline="{int(vs*0.85)}" spacing="600" horzpos="0" '
            f'horzsize="{horz}" flags="393216"/></hp:linesegarray>')

def para(pp, runs, vs=1200, page_break=0, horz=45352):
    """A top-level body paragraph."""
    return (f'<hp:p id="0" paraPrIDRef="{pp}" styleIDRef="0" pageBreak="{page_break}" '
            f'columnBreak="0" merged="0">{runs}{lineseg(vs, horz)}</hp:p>')

def run(cp, text=None):
    if text is None:
        return f'<hp:run charPrIDRef="{cp}"/>'
    return f'<hp:run charPrIDRef="{cp}"><hp:t>{esc(text)}</hp:t></hp:run>'

# ---------------------------------------------------------------- cover
def cover_block(spec):
    """Title table + date + department signature. Verbatim template, text swapped."""
    frag = open(COVER_FRAG, encoding="utf-8").read()
    dept_lines = spec.get("dept", ["AX·정보화혁신본부", "AX혁신과"])
    dept_paras = "".join(
        f'<hp:p id="2147483648" paraPrIDRef="20" styleIDRef="0" pageBreak="0" '
        f'columnBreak="0" merged="0">{run(14, ln)}{lineseg(1800, 17988)}</hp:p>'
        for ln in dept_lines
    )
    frag = frag.replace("{{TITLE1}}", esc(spec.get("title_top", "")))
    frag = frag.replace("{{TITLE2}}", esc(spec.get("title_main", "")))
    frag = frag.replace("{{DATE}}", esc(spec.get("date", "")))
    frag = frag.replace("{{DEPT_PARAS}}", dept_paras)
    return frag

# ---------------------------------------------------------------- section header (네모 숫자 절)
def section_header(num, title, page_break=0):
    """Navy number box + underlined title, as a 1x2 borderless-outer table."""
    tbl = (
        '<hp:tbl id="0" zOrder="5" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" '
        'textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" '
        'repeatHeader="1" rowCnt="1" colCnt="2" cellSpacing="0" borderFillIDRef="4" noAdjust="0">'
        '<hp:sz width="21890" widthRelTo="ABSOLUTE" height="2731" heightRelTo="ABSOLUTE" protect="0"/>'
        '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" '
        'holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="COLUMN" vertAlign="TOP" horzAlign="LEFT" '
        'vertOffset="0" horzOffset="0"/>'
        '<hp:outMargin left="140" right="140" top="140" bottom="140"/>'
        '<hp:inMargin left="141" right="141" top="141" bottom="141"/>'
        '<hp:tr>'
        + _tc(13, para_in_cell(21, run(16, str(num)), 1600), 0, 0, 3267, 2731, cs=1)
        + _tc(14, para_in_cell(22, run(17, " " + title), 1700), 1, 0, 18623, 2731, cs=1)
        + '</hp:tr></hp:tbl>'
    )
    runs = f'<hp:run charPrIDRef="15">{tbl}<hp:t/></hp:run>'
    return para(23, runs, vs=3011, page_break=page_break)

# ---------------------------------------------------------------- bullets / notes
def bullet(text, label=None):
    """◦ primary bullet.  label -> renders '(label)' in the bold style before text."""
    if label:
        runs = run(18, " ◦ ") + run(19, f"({label}) ") + run(20, text)
    else:
        runs = run(18, " ◦ ") + run(20, text)
    return para(24, runs, vs=1500)

def subbullet(text):
    """- secondary bullet, indented under a ◦."""
    return para(24, run(20, "   - " + text), vs=1400)

def note(text):
    """※ footnote-style remark."""
    return para(13, run(27, "   ※ " + text), vs=1200)

def plain(text):
    """A plain body paragraph (no marker)."""
    return para(13, run(20, text), vs=1400)

# ---------------------------------------------------------------- table cells
def para_in_cell(pp, runs, vs, horz=5000):
    return (f'<hp:p id="2147483648" paraPrIDRef="{pp}" styleIDRef="0" pageBreak="0" '
            f'columnBreak="0" merged="0">{runs}{lineseg(vs, horz)}</hp:p>')

def _tc(bf, inner_paras, col, row, width, height, cs=1, hdr=0):
    return (
        f'<hp:tc name="" header="{hdr}" hasMargin="0" protect="0" editable="0" dirty="0" '
        f'borderFillIDRef="{bf}">'
        f'<hp:subList id="" textDirection="HORIZONTAL" lineWrap="BREAK" vertAlign="CENTER" '
        f'linkListIDRef="0" linkListNextIDRef="0" textWidth="0" textHeight="0" hasTextRef="0" '
        f'hasNumRef="0">{inner_paras}</hp:subList>'
        f'<hp:cellAddr colAddr="{col}" rowAddr="{row}"/>'
        f'<hp:cellSpan colSpan="{cs}" rowSpan="1"/>'
        f'<hp:cellSz width="{width}" height="{height}"/>'
        f'<hp:cellMargin left="510" right="510" top="141" bottom="141"/></hp:tc>'
    )

def _cell_paras(lines, pp, cp, vs, horz):
    """One line -> one <hp:p>. lines may be str or list[str]."""
    if isinstance(lines, str):
        lines = [lines]
    if not lines:
        lines = [""]
    return "".join(
        para_in_cell(pp, (run(cp, ln) if ln != "" else run(cp)), vs, horz) for ln in lines
    )

# ---------------------------------------------------------------- grid table (청회색 머리행 표)
# Border-fill scheme copied from the original scoring/award tables.
GRID = {
    "header": (23, 24, 25),      # first / middle / last column
    "first":  (26, 27, 28),
    "middle": (29, 30, 31),
    "last":   (32, 33, 34),
    "total":  (35, 36, 37),      # 계 row, pale-yellow fill
}

def _colpos(c, ncols):
    if c == 0:
        return 0
    if c == ncols - 1:
        return 2
    return 1

def table(headers, rows, total=None, widths=None, total_width=45000):
    """Centered grid table with a light-blue header row (and optional pale 계 row).

    headers : list[str]                 - header cells (defines column count)
    rows    : list[list[str|list[str]]] - body rows; a cell may be a list for multi-line
    total   : list[str] | None          - a summary '계' row rendered in the pale style
    widths  : list[int] | None          - relative column weights (defaults to equal)
    """
    ncols = len(headers)
    if widths is None:
        widths = [1] * ncols
    tot_w = sum(widths)
    colw = [max(1200, int(total_width * w / tot_w)) for w in widths]

    body_count = len(rows)
    trs = []

    # header row
    cells = "".join(
        _tc(GRID["header"][_colpos(c, ncols)],
            _cell_paras(headers[c], 33, 29, 1200, colw[c] - 1020),
            c, 0, colw[c], 2614, hdr=1)
        for c in range(ncols)
    )
    trs.append(f"<hp:tr>{cells}</hp:tr>")

    # body rows
    for i, rowvals in enumerate(rows):
        if i == 0 and body_count > 1:
            band = "first"
        elif i == body_count - 1 and total is None:
            band = "last"
        elif i == 0 and body_count == 1 and total is None:
            band = "last"
        else:
            band = "middle"
        cells = "".join(
            _tc(GRID[band][_colpos(c, ncols)],
                _cell_paras(rowvals[c] if c < len(rowvals) else "", 34, 23, 1200, colw[c] - 1020),
                c, i + 1, colw[c], 2614)
            for c in range(ncols)
        )
        trs.append(f"<hp:tr>{cells}</hp:tr>")

    # total row
    if total is not None:
        r = body_count + 1
        cells = "".join(
            _tc(GRID["total"][_colpos(c, ncols)],
                _cell_paras(total[c] if c < len(total) else "", 34, 29, 1200, colw[c] - 1020),
                c, r, colw[c], 2614)
            for c in range(ncols)
        )
        trs.append(f"<hp:tr>{cells}</hp:tr>")

    nrows = len(trs)
    tbl = (
        f'<hp:tbl id="0" zOrder="2" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" '
        f'textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" '
        f'rowCnt="{nrows}" colCnt="{ncols}" cellSpacing="0" borderFillIDRef="3" noAdjust="0">'
        f'<hp:sz width="{sum(colw)}" widthRelTo="ABSOLUTE" height="{nrows*2614}" '
        f'heightRelTo="ABSOLUTE" protect="0"/>'
        f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" '
        f'holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" '
        f'vertOffset="0" horzOffset="0"/>'
        f'<hp:outMargin left="0" right="0" top="0" bottom="0"/>'
        f'<hp:inMargin left="510" right="510" top="141" bottom="141"/>'
        + "".join(trs) + "</hp:tbl>"
    )
    runs = f'<hp:run charPrIDRef="20"><hp:t>    </hp:t>{tbl}<hp:t/></hp:run>'
    return para(27, runs, vs=2614)

# ---------------------------------------------------------------- boxed 2-col table (구분/내용)
BOX = {"header": (15, 16), "first": (17, 18), "middle": (19, 20), "last": (21, 22)}

def table_boxed(pairs, header=("구분", "내용"), label_width=6376, content_width=38638):
    """Boxed 2-column table: bold label cell + left-justified (multi-line) content cell.

    pairs : list[(label, content)] where content is str or list[str]
    header: (left_title, right_title)
    """
    n = len(pairs)
    trs = []
    # header
    cells = (_tc(BOX["header"][0], para_in_cell(25, run(22, header[0]), 1200, label_width - 1020),
                 0, 0, label_width, 2614, hdr=1)
             + _tc(BOX["header"][1], para_in_cell(25, run(22, header[1]), 1200, content_width - 1020),
                   1, 0, content_width, 2614, hdr=1))
    trs.append(f"<hp:tr>{cells}</hp:tr>")
    for i, (label, content) in enumerate(pairs):
        band = "first" if i == 0 else ("last" if i == n - 1 else "middle")
        lines = content if isinstance(content, list) else [content]
        height = max(2614, 1920 * len(lines))
        left = _tc(BOX[band][0], para_in_cell(26, run(23, label), 1200, label_width - 1020),
                   0, i + 1, label_width, height)
        right_paras = "".join(
            para_in_cell(28, run(24, ln) if ln else run(24), 1200, content_width - 1020) for ln in lines
        )
        right = _tc(BOX[band][1], right_paras, 1, i + 1, content_width, height)
        trs.append(f"<hp:tr>{left}{right}</hp:tr>")
    nrows = len(trs)
    total_w = label_width + content_width
    tbl = (
        f'<hp:tbl id="0" zOrder="2" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" '
        f'textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" '
        f'rowCnt="{nrows}" colCnt="2" cellSpacing="0" borderFillIDRef="4" noAdjust="1">'
        f'<hp:sz width="{total_w}" widthRelTo="ABSOLUTE" height="{nrows*2614}" '
        f'heightRelTo="ABSOLUTE" protect="0"/>'
        f'<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" '
        f'holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" '
        f'vertOffset="0" horzOffset="0"/>'
        f'<hp:outMargin left="141" right="141" top="141" bottom="0"/>'
        f'<hp:inMargin left="510" right="510" top="141" bottom="141"/>'
        + "".join(trs) + "</hp:tbl>"
    )
    runs = f'<hp:run charPrIDRef="20"><hp:t>    </hp:t>{tbl}<hp:t/></hp:run>'
    return para(27, runs, vs=2614)

# ---------------------------------------------------------------- annex header (붙임)
def annex_header(label, title, page_break=1):
    """붙임 N  |  title  — cyan number box + title, starts a new page by default."""
    tbl = (
        '<hp:tbl id="0" zOrder="13" numberingType="TABLE" textWrap="TOP_AND_BOTTOM" '
        'textFlow="BOTH_SIDES" lock="0" dropcapstyle="None" pageBreak="CELL" repeatHeader="1" '
        'rowCnt="1" colCnt="3" cellSpacing="0" borderFillIDRef="4" noAdjust="0">'
        '<hp:sz width="47916" widthRelTo="ABSOLUTE" height="2980" heightRelTo="ABSOLUTE" protect="0"/>'
        '<hp:pos treatAsChar="1" affectLSpacing="0" flowWithText="1" allowOverlap="0" '
        'holdAnchorAndSO="0" vertRelTo="PARA" horzRelTo="PARA" vertAlign="TOP" horzAlign="LEFT" '
        'vertOffset="0" horzOffset="0"/>'
        '<hp:outMargin left="0" right="0" top="0" bottom="0"/>'
        '<hp:inMargin left="510" right="510" top="141" bottom="141"/>'
        '<hp:tr>'
        + _tc(38, para_in_cell(51, run(49, label), 1700, 5648), 0, 0, 6670, 2980, cs=1, hdr=1)
        + _tc(39, para_in_cell(50, run(50), 1700, 1440), 1, 0, 1303, 2980, cs=1)
        + _tc(40, para_in_cell(13, run(51, title), 1600, 38920), 2, 0, 39943, 2980, cs=1)
        + '</hp:tr></hp:tbl>'
    )
    runs = f'<hp:run charPrIDRef="27">{tbl}<hp:t/></hp:run>'
    return para(61, runs, vs=2980, page_break=page_break)

# ---------------------------------------------------------------- assembly
def render_item(it):
    t = it["type"]
    if t == "bullet":
        return bullet(it["text"], it.get("label"))
    if t == "subbullet":
        return subbullet(it["text"])
    if t == "note":
        return note(it["text"])
    if t == "plain":
        return plain(it["text"])
    if t == "table":
        return table(it["headers"], it["rows"], it.get("total"), it.get("widths"))
    if t == "table_boxed":
        return table_boxed(it["pairs"], tuple(it.get("header", ("구분", "내용"))))
    if t == "annex":
        return annex_header(it["label"], it["title"], it.get("page_break", 1))
    raise ValueError(f"unknown item type: {t}")

def build_section_xml(spec):
    parts = [cover_block(spec)]
    seen_header = False
    for si, sec in enumerate(spec.get("sections", [])):
        if "number" in sec:  # a numbered section header
            # The cover occupies page 1 on its own, so the first numbered
            # section starts on a fresh page (matching the source document).
            default_pb = 0 if seen_header else 1
            parts.append(section_header(sec["number"], sec["title"],
                                        page_break=sec.get("page_break", default_pb)))
            seen_header = True
        for it in sec.get("items", []):
            parts.append(render_item(it))
    for it in spec.get("annexes", []):
        parts.append(render_item(it))
    return "".join(parts)

def build(spec, out_path):
    # exact section root prefix (namespaces) + secPr live in the template's section0.xml
    orig = open(os.path.join(TEMPLATE, "Contents", "section0.xml"), encoding="utf-8").read()
    sec_open = orig[:orig.index("<hp:p")]
    body = build_section_xml(spec)
    new_section = sec_open + body + "</hs:sec>"

    tmp = tempfile.mkdtemp()
    try:
        stage = os.path.join(tmp, "pkg")
        shutil.copytree(TEMPLATE, stage)
        with open(os.path.join(stage, "Contents", "section0.xml"), "w", encoding="utf-8") as f:
            f.write(new_section)
        # repackage: mimetype first & stored, rest deflated
        if os.path.exists(out_path):
            os.remove(out_path)
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
            mt = os.path.join(stage, "mimetype")
            z.write(mt, "mimetype", compress_type=zipfile.ZIP_STORED)
            for root, _, files in os.walk(stage):
                for name in files:
                    full = os.path.join(root, name)
                    rel = os.path.relpath(full, stage).replace("\\", "/")
                    if rel == "mimetype":
                        continue
                    z.write(full, rel)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out_path

# ---------------------------------------------------------------- CLI
if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--spec":
        spec = json.load(open(sys.argv[2], encoding="utf-8"))
        out = sys.argv[3] if len(sys.argv) > 3 else "report.hwpx"
    else:
        sys.path.insert(0, HERE)
        from demo_spec import demo
        spec = demo()
        out = sys.argv[1] if len(sys.argv) > 1 else "report.hwpx"
    path = build(spec, out)
    print("wrote", path)
