"""model 模块单元测试。"""

from __future__ import annotations

import unittest

from answersheet.model import (
    MAX_COLUMNS,
    MAX_OPTIONS,
    MAX_QUESTIONS,
    ROWS_PER_COLUMN,
    AnswersheetError,
    SheetConfig,
    option_labels,
    page_numbers,
    paginate,
)


class ConfigTest(unittest.TestCase):
    def test_defaults(self) -> None:
        config = SheetConfig()
        self.assertEqual(config.questions, 50)
        self.assertEqual(config.options, 4)
        self.assertEqual(config.columns, 2)
        self.assertEqual(config.per_page, 60)
        self.assertEqual(config.pages, 1)

    def test_custom(self) -> None:
        config = SheetConfig(questions=200, options=6, columns=4)
        self.assertEqual(config.pages, 2)
        self.assertEqual(config.labels, ("A", "B", "C", "D", "E", "F"))

    def test_questions_range(self) -> None:
        with self.assertRaises(AnswersheetError):
            SheetConfig(questions=0)
        with self.assertRaises(AnswersheetError):
            SheetConfig(questions=MAX_QUESTIONS + 1)

    def test_options_range(self) -> None:
        with self.assertRaises(AnswersheetError):
            SheetConfig(options=1)
        with self.assertRaises(AnswersheetError):
            SheetConfig(options=MAX_OPTIONS + 1)

    def test_columns_range(self) -> None:
        with self.assertRaises(AnswersheetError):
            SheetConfig(columns=0)
        with self.assertRaises(AnswersheetError):
            SheetConfig(columns=MAX_COLUMNS + 1)

    def test_bool_rejected(self) -> None:
        with self.assertRaises(AnswersheetError):
            SheetConfig(questions=True)  # type: ignore[arg-type]
        with self.assertRaises(AnswersheetError):
            SheetConfig(options=True)  # type: ignore[arg-type]
        with self.assertRaises(AnswersheetError):
            SheetConfig(columns=True)  # type: ignore[arg-type]

    def test_non_int_rejected(self) -> None:
        with self.assertRaises(AnswersheetError):
            SheetConfig(questions="50")  # type: ignore[arg-type]

    def test_pagination_pages(self) -> None:
        self.assertEqual(SheetConfig(questions=50).pages, 1)
        self.assertEqual(SheetConfig(questions=60).pages, 1)
        self.assertEqual(SheetConfig(questions=61).pages, 2)
        self.assertEqual(SheetConfig(questions=200, columns=1).pages, 7)


class OptionLabelTest(unittest.TestCase):
    def test_labels(self) -> None:
        self.assertEqual(option_labels(2), ("A", "B"))
        self.assertEqual(option_labels(4), ("A", "B", "C", "D"))
        self.assertEqual(option_labels(6), ("A", "B", "C", "D", "E", "F"))

    def test_invalid(self) -> None:
        with self.assertRaises(AnswersheetError):
            option_labels(1)
        with self.assertRaises(AnswersheetError):
            option_labels(7)
        with self.assertRaises(AnswersheetError):
            option_labels(True)  # type: ignore[arg-type]


class PaginateTest(unittest.TestCase):
    def test_two_columns(self) -> None:
        pages = paginate(SheetConfig(questions=50))
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0][0], list(range(1, 31)))
        self.assertEqual(pages[0][1], list(range(31, 51)))

    def test_partial_column(self) -> None:
        pages = paginate(SheetConfig(questions=35))
        self.assertEqual(pages[0][1], list(range(31, 36)))

    def test_empty_columns_filled(self) -> None:
        pages = paginate(SheetConfig(questions=10, columns=4))
        self.assertEqual(len(pages[0]), 4)
        self.assertEqual(pages[0][0], list(range(1, 11)))
        self.assertEqual(pages[0][1:], [[], [], []])

    def test_multi_page(self) -> None:
        pages = paginate(SheetConfig(questions=70))
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[1][0], list(range(61, 71)))
        self.assertEqual(pages[1][1], [])

    def test_custom_rows(self) -> None:
        pages = paginate(SheetConfig(questions=10), rows=4)
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[0][0], [1, 2, 3, 4])

    def test_bad_rows(self) -> None:
        with self.assertRaises(AnswersheetError):
            paginate(SheetConfig(), rows=0)
        with self.assertRaises(AnswersheetError):
            paginate(SheetConfig(), rows=True)  # type: ignore[arg-type]

    def test_non_config(self) -> None:
        with self.assertRaises(AnswersheetError):
            paginate("config")  # type: ignore[arg-type]

    def test_rows_constant(self) -> None:
        self.assertEqual(ROWS_PER_COLUMN, 30)


class PageNumbersTest(unittest.TestCase):
    def test_first_page(self) -> None:
        columns = page_numbers(SheetConfig(questions=70), 1)
        self.assertEqual(columns[0][0], 1)

    def test_second_page(self) -> None:
        columns = page_numbers(SheetConfig(questions=70), 2)
        self.assertEqual(columns[0][0], 61)

    def test_out_of_range(self) -> None:
        for value in (0, 3):
            with self.assertRaises(AnswersheetError):
                page_numbers(SheetConfig(questions=70), value)

    def test_non_int(self) -> None:
        with self.assertRaises(AnswersheetError):
            page_numbers(SheetConfig(), "1")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
