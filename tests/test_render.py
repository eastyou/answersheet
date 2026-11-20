"""render 模块单元测试。"""

from __future__ import annotations

import unittest

from answersheet.model import AnswersheetError, SheetConfig
from answersheet.render import render_html


class RenderHtmlTest(unittest.TestCase):
    def test_basic_document(self) -> None:
        page = render_html(SheetConfig(questions=50))
        self.assertTrue(page.startswith("<!doctype html>"))
        self.assertIn("A4 portrait", page)
        self.assertIn("答题卡", page)

    def test_question_count(self) -> None:
        page = render_html(SheetConfig(questions=50))
        self.assertEqual(page.count('class="q"'), 50)
        self.assertEqual(page.count('class="bubble"'), 200)

    def test_option_labels(self) -> None:
        page = render_html(SheetConfig(questions=5, options=2))
        self.assertEqual(page.count('class="bubble"'), 10)
        self.assertIn('class="bubble">A<', page)
        self.assertIn('class="bubble">B<', page)
        self.assertNotIn('class="bubble">C<', page)

    def test_columns(self) -> None:
        page = render_html(SheetConfig(questions=10, columns=3))
        self.assertIn("repeat(3,1fr)", page)
        self.assertEqual(page.count('class="col"'), 3)

    def test_two_pages(self) -> None:
        page = render_html(SheetConfig(questions=70))
        self.assertEqual(page.count('<section class="sheet">'), 2)
        self.assertIn("第 1 / 2 页", page)
        self.assertIn("第 2 / 2 页", page)
        self.assertIn('<span class="no">61</span>', page)

    def test_subject(self) -> None:
        page = render_html(SheetConfig(), subject="语文")
        self.assertIn('class="subject">语文<', page)

    def test_empty_subject_omitted(self) -> None:
        page = render_html(SheetConfig(), subject="  ")
        self.assertNotIn('class="subject"', page)

    def test_title_escaped(self) -> None:
        page = render_html(SheetConfig(), title="<答题卡>")
        self.assertIn("&lt;答题卡&gt;", page)

    def test_info_fields(self) -> None:
        page = render_html(SheetConfig())
        for label in ("姓名", "班级", "学号", "日期"):
            self.assertIn("<b>%s</b>" % label, page)

    def test_instruction(self) -> None:
        page = render_html(SheetConfig())
        self.assertIn("2B 铅笔", page)

    def test_footer(self) -> None:
        page = render_html(SheetConfig(questions=30, options=5))
        self.assertIn("共 30 题", page)
        self.assertIn("每题 5 个选项", page)

    def test_bad_config(self) -> None:
        with self.assertRaises(AnswersheetError):
            render_html("config")  # type: ignore[arg-type]

    def test_empty_title(self) -> None:
        with self.assertRaises(AnswersheetError):
            render_html(SheetConfig(), title=" ")

    def test_non_text_subject(self) -> None:
        with self.assertRaises(AnswersheetError):
            render_html(SheetConfig(), subject=1)  # type: ignore[arg-type]

    def test_bad_rows(self) -> None:
        with self.assertRaises(AnswersheetError):
            render_html(SheetConfig(), rows=0)


if __name__ == "__main__":
    unittest.main()
