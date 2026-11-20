"""命令行入口单元测试。"""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from typing import List

from answersheet.cli import main


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.target = self.root / "sheet.html"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cli(self, argv: List[str]) -> int:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            return main(argv)

    def test_generate(self) -> None:
        code = self.run_cli(["-o", str(self.target)])
        self.assertEqual(code, 0)
        page = self.target.read_text(encoding="utf-8")
        self.assertIn("<!doctype html>", page)
        self.assertEqual(page.count('class="q"'), 50)

    def test_custom_generation(self) -> None:
        code = self.run_cli(
            [
                "-o", str(self.target),
                "-q", "70", "--options", "2", "--columns", "1",
            ]
        )
        self.assertEqual(code, 0)
        page = self.target.read_text(encoding="utf-8")
        self.assertEqual(page.count('<section class="sheet">'), 3)
        self.assertEqual(page.count('class="bubble"'), 140)

    def test_subject_and_title(self) -> None:
        code = self.run_cli(
            ["-o", str(self.target), "--subject", "数学", "--title", "期中答题卡"]
        )
        self.assertEqual(code, 0)
        page = self.target.read_text(encoding="utf-8")
        self.assertIn("数学", page)
        self.assertIn("期中答题卡", page)

    def test_invalid_questions(self) -> None:
        code = self.run_cli(["-o", str(self.target), "-q", "0"])
        self.assertEqual(code, 2)
        self.assertFalse(self.target.exists())

    def test_invalid_options(self) -> None:
        code = self.run_cli(["-o", str(self.target), "--options", "8"])
        self.assertEqual(code, 2)

    def test_invalid_columns(self) -> None:
        code = self.run_cli(["-o", str(self.target), "--columns", "5"])
        self.assertEqual(code, 2)

    def test_help(self) -> None:
        with self.assertRaises(SystemExit) as ctx:
            with contextlib.redirect_stdout(io.StringIO()):
                main(["--help"])
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
