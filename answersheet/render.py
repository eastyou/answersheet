"""把答题卡渲染成可打印的 A4 页面。"""

from __future__ import annotations

import html
from typing import List, Sequence

from .model import (
    ROWS_PER_COLUMN,
    AnswersheetError,
    SheetConfig,
    paginate,
)

PAGE_WIDTH_MM = 210.0
PAGE_HEIGHT_MM = 297.0


def _num(value: float) -> str:
    text = "%.1f" % value
    return text.rstrip("0").rstrip(".") if "." in text else text


def _info_markup() -> str:
    return (
        '<div class="info">'
        "<span><b>姓名</b><i></i></span>"
        "<span><b>班级</b><i></i></span>"
        "<span><b>学号</b><i></i></span>"
        "<span><b>日期</b><i></i></span>"
        "</div>"
    )


def _column_markup(numbers: Sequence[int], labels: Sequence[str]) -> str:
    rows: List[str] = []
    for number in numbers:
        bubbles = "".join(
            '<span class="bubble">%s</span>' % label for label in labels
        )
        rows.append(
            '<div class="q"><span class="no">%d</span>'
            '<span class="bubbles">%s</span></div>' % (number, bubbles)
        )
    return '<div class="col">%s</div>' % "".join(rows)


def render_html(
    config: SheetConfig,
    title: str = "答题卡",
    subject: str = "",
    rows: int = ROWS_PER_COLUMN,
) -> str:
    """生成完整 HTML：按分栏与分页排布题号与选项圆圈。"""
    if not isinstance(config, SheetConfig):
        raise AnswersheetError("config 必须是 SheetConfig 对象")
    if not isinstance(title, str) or not title.strip():
        raise AnswersheetError("标题不能为空")
    if not isinstance(subject, str):
        raise AnswersheetError("科目名称必须是文本")

    pages = paginate(config, rows)
    total = len(pages)
    sheets: List[str] = []
    for page_index, columns in enumerate(pages):
        head = (
            '<header class="head"><h1>%s</h1>' % html.escape(title.strip())
        )
        if subject.strip():
            head += '<p class="subject">%s</p>' % html.escape(subject.strip())
        head += _info_markup() + "</header>"

        note = (
            '<p class="note">请用 2B 铅笔把所选选项涂黑，'
            "修改时用橡皮擦干净；每题只能选一个答案。</p>"
        )
        grid = (
            '<div class="cols" style="grid-template-columns:repeat(%d,1fr)">%s</div>'
            % (
                config.columns,
                "".join(_column_markup(column, config.labels) for column in columns),
            )
        )
        foot = (
            '<footer class="foot"><span>第 %d / %d 页 · 共 %d 题 · 每题 %d 个选项</span>'
            "<span>answersheet · A4 纵向</span></footer>"
            % (page_index + 1, total, config.questions, config.options)
        )
        sheets.append(
            '<section class="sheet">%s%s%s%s</section>' % (head, note, grid, foot)
        )

    toolbar = (
        '<div class="toolbar"><strong>%s</strong>'
        "<span>共 %d 题 · %d 栏 · 每题 %d 个选项 · 共 %d 页</span></div>"
        % (
            html.escape(title.strip()),
            config.questions,
            config.columns,
            config.options,
            total,
        )
    )

    return (
        "<!doctype html>\n"
        '<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n%s\n%s\n</body>\n</html>\n"
        % (html.escape(title.strip()), STYLE, toolbar, "\n".join(sheets))
    )


STYLE = """
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: 8mm 0 12mm;
    background: #e2e8f0;
    color: #0f172a;
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  }
  .toolbar {
    width: 210mm;
    margin: 0 auto 6mm;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 12px;
    color: #334155;
    font-size: 13px;
  }
  .toolbar strong { font-size: 15px; letter-spacing: 1px; }
  .toolbar span { color: #64748b; font-size: 12px; }
  .sheet {
    width: 210mm;
    height: 297mm;
    margin: 0 auto 8mm;
    padding: 13mm 15mm 9mm;
    background: #fff;
    box-shadow: 0 6px 22px rgba(15, 23, 42, 0.14);
    display: flex;
    flex-direction: column;
    page-break-after: always;
    break-after: page;
    overflow: hidden;
  }
  .sheet:last-child { page-break-after: auto; break-after: auto; }
  .head { text-align: center; }
  .head h1 {
    margin: 0;
    font-size: 22pt;
    font-weight: 600;
    letter-spacing: 6pt;
  }
  .head .subject {
    margin: 1.5mm 0 0;
    font-size: 11pt;
    color: #475569;
    letter-spacing: 2pt;
  }
  .info {
    display: flex;
    justify-content: space-between;
    gap: 5mm;
    margin: 5mm 0 3mm;
    font-size: 10.5pt;
    color: #334155;
  }
  .info span { flex: 1; display: flex; align-items: flex-end; gap: 1.5mm; }
  .info b { font-weight: 400; white-space: nowrap; }
  .info i { flex: 1; height: 4.6mm; border-bottom: 0.3mm solid #94a3b8; }
  .note {
    margin: 0 0 4mm;
    padding: 2.2mm 3.5mm;
    background: #f1f5f9;
    border-left: 1.2mm solid #0f172a;
    font-size: 8.5pt;
    color: #475569;
  }
  .cols {
    display: grid;
    gap: 5mm 8mm;
  }
  .col { display: flex; flex-direction: column; }
  .q {
    display: flex;
    align-items: center;
    height: 6.8mm;
    border-bottom: 0.15mm solid #e2e8f0;
  }
  .q .no {
    width: 8mm;
    text-align: right;
    padding-right: 2mm;
    font-size: 8.5pt;
    color: #475569;
  }
  .q .bubbles { display: flex; gap: 1.6mm; margin-left: 2mm; }
  .bubble {
    width: 4.6mm;
    height: 4.6mm;
    border: 0.3mm solid #475569;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 6.5pt;
    color: #475569;
    line-height: 1;
  }
  .foot {
    margin-top: auto;
    padding-top: 2mm;
    display: flex;
    justify-content: space-between;
    font-size: 8pt;
    color: #64748b;
    border-top: 0.2mm solid #e2e8f0;
  }
  @page { size: A4 portrait; margin: 0; }
  @media print {
    body { background: #fff; padding: 0; }
    .toolbar { display: none; }
    .sheet { margin: 0; box-shadow: none; }
    * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
"""
