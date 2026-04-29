# test_clamutils.py
#
# This file is part of ClammingPy tool.
# (C) 2023-2025 Brigitte Bigi, CNRS, Laboratoire Parole et Langage,
# Aix-en-Provence, France.
#
# Use of this software is governed by the GNU Public License, version 3.
#
# ClammingPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ClammingPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ClammingPy.
# If not, see <https://www.gnu.org/licenses/licenses.en.html>.
#
# This banner notice must not be removed.
# ---------------------------------------------------------------------------

import unittest
from dataclasses import dataclass

from clamming.clamutils import ClamUtils
from clamming.clamspack import ClamsPack
from clamming.clamsclass import ClamsClass
from clamming.claminfo import ClamInfo
from clamming.classparser import ClammingClassParser

# ---------------------------------------------------------------------------


class SomeClass:
    def __init__(self, name):
        self.name = name


@dataclass
class SomeDataClass:
    name: str

# ---------------------------------------------------------------------------


class TestClamUtils(unittest.TestCase):

    def test_get_class(self):
        # With a user-defined library
        self.assertEqual(ClamsPack, ClamUtils.get_class("ClamsPack", "clamming"))
        self.assertEqual(ClamsClass, ClamUtils.get_class("ClamsClass", "clamming"))
        self.assertEqual(ClamInfo, ClamUtils.get_class("ClamInfo", "clamming"))

        # ...with a wrong class name
        self.assertIsNone(ClamUtils.get_class("something", "clamming"))  # wrong name
        self.assertIsNone(ClamUtils.get_class("clamming", "clamming"))   # wrong type

        # With a standard Python library
        self.assertIsNotNone(ClamUtils.get_class("TestCase", "unittest"))

        # ... with invalid class
        self.assertIsNone(ClamUtils.get_class("something", "sys"))

        # With invalid module
        self.assertIsNone(ClamUtils.get_class("something", "somewhere"))

        # With locally defined classes
        self.assertIsNotNone(ClamUtils.get_class("SomeClass", __name__))
        self.assertIsNotNone(ClamUtils.get_class("SomeDataClass", __name__))

    def test_get_class_no_module(self):
        result = ClamUtils.get_class("NonExistentClass123")
        self.assertIsNone(result)

    def test_markdown_convert(self):
        u = ClamUtils()
        html = u.markdown_convert("**bold** text")
        self.assertIn("bold", html)
        self.assertIn("<strong>", html)

    def test_markdown_convert_empty(self):
        u = ClamUtils()
        html = u.markdown_convert("")
        self.assertIn("<p>", html)

    def test_source_to_html(self):
        u = ClamUtils()
        html = u.source_to_html("def hello(): pass")
        self.assertIn("hello", html)
        self.assertGreater(len(html), 0)

    def test_markdown_to_html_plain(self):
        u = ClamUtils()
        html = u.markdown_to_html("# Title\n\nSome text.")
        self.assertIn("Title", html)
        self.assertIn("Some text", html)

    def test_markdown_to_html_fenced_code(self):
        u = ClamUtils()
        md = "Some text.\n\n```python\ndef foo(): pass\n```\n\nMore text."
        html = u.markdown_to_html(md)
        self.assertIn("foo", html)
        self.assertIn("More text", html)

    def test_markdown_to_html_example_lines(self):
        u = ClamUtils()
        md = "Description.\n\n    >>> x = 1\n    > result = x + 1\n"
        html = u.markdown_to_html(md)
        self.assertIn("highlight", html)

    def test_markdown_to_html_table(self):
        u = ClamUtils()
        md = "| Col1 | Col2 |\n|------|------|\n| A    | B    |\n"
        html = u.markdown_to_html(md)
        self.assertIn("<table", html)

    def test_clamsclass_name_and_description(self):
        parser = ClammingClassParser(SomeClass)
        clams = ClamsClass(parser)
        self.assertEqual(clams.name, "SomeClass")
        self.assertIn("SomeClass", clams.short_description)

    def test_clamsclass_markdown(self):
        parser = ClammingClassParser(SomeClass)
        clams = ClamsClass(parser)
        md = clams.markdown()
        self.assertIn("## Class `SomeClass`", md)
        self.assertIn("### Constructor", md)

    def test_clamsclass_html(self):
        parser = ClammingClassParser(SomeClass)
        clams = ClamsClass(parser)
        html = clams.html()
        self.assertIn("<h2>Class SomeClass</h2>", html)


