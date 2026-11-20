"""答题卡数据模型：题量、选项数与分栏分页。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

MIN_QUESTIONS = 1
MAX_QUESTIONS = 200
MIN_OPTIONS = 2
MAX_OPTIONS = 6
MIN_COLUMNS = 1
MAX_COLUMNS = 4
ROWS_PER_COLUMN = 30
OPTION_LABELS = "ABCDEF"


class AnswersheetError(ValueError):
    """题量、选项数或版式参数不合法。"""


def _check_int(value: int, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise AnswersheetError("%s必须是整数" % label)
    return value


@dataclass(frozen=True)
class SheetConfig:
    """一张答题卡的版式：题量、每题选项数与分栏数。"""

    questions: int = 50
    options: int = 4
    columns: int = 2

    def __post_init__(self) -> None:
        questions = _check_int(self.questions, "题目数量")
        options = _check_int(self.options, "选项数量")
        columns = _check_int(self.columns, "分栏数")
        if not MIN_QUESTIONS <= questions <= MAX_QUESTIONS:
            raise AnswersheetError(
                "题目数量必须在 %d~%d 之间，当前是 %d"
                % (MIN_QUESTIONS, MAX_QUESTIONS, questions)
            )
        if not MIN_OPTIONS <= options <= MAX_OPTIONS:
            raise AnswersheetError(
                "每题选项数必须在 %d~%d 之间，当前是 %d"
                % (MIN_OPTIONS, MAX_OPTIONS, options)
            )
        if not MIN_COLUMNS <= columns <= MAX_COLUMNS:
            raise AnswersheetError(
                "分栏数必须在 %d~%d 之间，当前是 %d"
                % (MIN_COLUMNS, MAX_COLUMNS, columns)
            )
        object.__setattr__(self, "questions", questions)
        object.__setattr__(self, "options", options)
        object.__setattr__(self, "columns", columns)

    @property
    def per_page(self) -> int:
        """每页可容纳的题目数。"""
        return self.columns * ROWS_PER_COLUMN

    @property
    def pages(self) -> int:
        """需要的页数。"""
        return (self.questions + self.per_page - 1) // self.per_page

    @property
    def labels(self) -> Tuple[str, ...]:
        """选项字母，例如 A/B/C/D。"""
        return option_labels(self.options)


def option_labels(count: int) -> Tuple[str, ...]:
    """返回指定数量的选项字母。"""
    value = _check_int(count, "选项数量")
    if not MIN_OPTIONS <= value <= MAX_OPTIONS:
        raise AnswersheetError(
            "选项数量必须在 %d~%d 之间，当前是 %d"
            % (MIN_OPTIONS, MAX_OPTIONS, value)
        )
    return tuple(OPTION_LABELS[:value])


def paginate(config: SheetConfig, rows: int = ROWS_PER_COLUMN) -> List[List[List[int]]]:
    """按页、按栏切分题号，返回「页 -> 栏 -> 题号」三层结构。"""
    if not isinstance(config, SheetConfig):
        raise AnswersheetError("config 必须是 SheetConfig 对象")
    size = _check_int(rows, "每栏行数")
    if size < 1:
        raise AnswersheetError("每栏行数必须大于 0")

    numbers = list(range(1, config.questions + 1))
    pages: List[List[List[int]]] = []
    index = 0
    while index < len(numbers):
        page: List[List[int]] = []
        for _ in range(config.columns):
            column = numbers[index : index + size]
            page.append(column)
            index += size
            if index >= len(numbers):
                while len(page) < config.columns:
                    page.append([])
                break
        pages.append(page)
    return pages


def page_numbers(config: SheetConfig, page: int) -> List[List[int]]:
    """取指定页码（从 1 开始）的栏目题号。"""
    if not isinstance(config, SheetConfig):
        raise AnswersheetError("config 必须是 SheetConfig 对象")
    page_index = _check_int(page, "页码")
    pages = paginate(config)
    if not 1 <= page_index <= len(pages):
        raise AnswersheetError(
            "页码超出范围：%d（共 %d 页）" % (page_index, len(pages))
        )
    return pages[page_index - 1]
