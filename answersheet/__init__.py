"""answersheet：A4 可打印选择题答题卡。"""

from __future__ import annotations

from .model import (
    MAX_COLUMNS,
    MAX_OPTIONS,
    MAX_QUESTIONS,
    MIN_COLUMNS,
    MIN_OPTIONS,
    MIN_QUESTIONS,
    OPTION_LABELS,
    ROWS_PER_COLUMN,
    AnswersheetError,
    SheetConfig,
    option_labels,
    page_numbers,
    paginate,
)
from .render import render_html

__version__ = "0.1.0"

__all__ = [
    "MAX_COLUMNS",
    "MAX_OPTIONS",
    "MAX_QUESTIONS",
    "MIN_COLUMNS",
    "MIN_OPTIONS",
    "MIN_QUESTIONS",
    "OPTION_LABELS",
    "ROWS_PER_COLUMN",
    "AnswersheetError",
    "SheetConfig",
    "option_labels",
    "page_numbers",
    "paginate",
    "render_html",
    "__version__",
]
