"""命令行入口：生成可打印的选择题答题卡。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .model import (
    MAX_COLUMNS,
    MAX_OPTIONS,
    MAX_QUESTIONS,
    MIN_COLUMNS,
    MIN_OPTIONS,
    MIN_QUESTIONS,
    AnswersheetError,
    SheetConfig,
)
from .render import render_html


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="answersheet",
        description="选择题答题卡：按题量与选项数生成 A4 可打印答题卡",
    )
    parser.add_argument("--version", action="version", version="answersheet 0.1.0")
    parser.add_argument(
        "-o", "--output", default="答题卡.html", help="输出 HTML 路径"
    )
    parser.add_argument(
        "-q",
        "--questions",
        type=int,
        default=50,
        help="题目数量 %d~%d，默认 50" % (MIN_QUESTIONS, MAX_QUESTIONS),
    )
    parser.add_argument(
        "--options",
        type=int,
        default=4,
        help="每题选项数 %d~%d，默认 4" % (MIN_OPTIONS, MAX_OPTIONS),
    )
    parser.add_argument(
        "--columns",
        type=int,
        default=2,
        help="分栏数 %d~%d，默认 2" % (MIN_COLUMNS, MAX_COLUMNS),
    )
    parser.add_argument("--subject", default="", help="科目名称，例如语文")
    parser.add_argument("--title", default="答题卡", help="页面标题")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        config = SheetConfig(
            questions=args.questions,
            options=args.options,
            columns=args.columns,
        )
        page = render_html(config, title=args.title, subject=args.subject)
    except AnswersheetError as exc:
        print("错误: %s" % exc, file=sys.stderr)
        return 2

    try:
        Path(args.output).write_text(page, encoding="utf-8")
    except OSError as exc:
        print("错误: 写入文件失败: %s" % exc, file=sys.stderr)
        return 1

    print(
        "已生成 %s：共 %d 题，每题 %d 个选项，%d 栏，共 %d 页"
        % (
            args.output,
            config.questions,
            config.options,
            config.columns,
            config.pages,
        )
    )
    print("用浏览器打开后按 Ctrl/Cmd + P，纸张选 A4 纵向即可打印")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
