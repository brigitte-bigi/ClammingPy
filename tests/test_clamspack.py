# test_clamspack.py
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

import os
import unittest

import clamming
from clamming.clamspack import ClamsPack
from clamming.exportoptions import ExportOptions

# ---------------------------------------------------------------------------


class TestClamsPack(unittest.TestCase):

    def test_clams_pack_creation(self):

        p = ClamsPack(clamming)
        self.assertEqual(p.name, "clamming")
        self.assertEqual(len(p), 8)

        p = ClamsPack(unittest)
        self.assertEqual(p.name, "unittest")
        with self.assertRaises(TypeError):
            ClamsPack(ClamsPack)

    # -----------------------------------------------------------------------

    def test_markdown(self):
        p = ClamsPack(clamming)
        md = p.markdown()
        self.assertTrue(md.startswith("# clamming module"))
        self.assertTrue(md.endswith(" ~\n"))
        self.assertIn("## Class `ClammingClassParser`", md)
        self.assertIn("## Class `ClamsClass`", md)
        self.assertIn("## Class `ClamsPack`", md)
        self.assertIn("## Class `ClamInfo`", md)
        self.assertIn("## Class `ClamInfoMarkdown`", md)

    # -----------------------------------------------------------------------

    def test_html(self):
        p = ClamsPack(clamming)
        html = p.html()
        self.assertTrue(html.startswith("<h1>clamming module</h1>"))
        self.assertTrue(html.endswith(" ~</p>\n"))
        self.assertIn("<h2>Class ClammingClassParser</h2>", html)
        self.assertIn("<h2>Class ClamsClass</h2>", html)
        self.assertIn("<h2>Class ClamsPack</h2>", html)
        self.assertIn("<h2>Class ClamInfo</h2>", html)
        self.assertIn("<h2>Class ClamInfoMarkdown</h2>", html)

    # -----------------------------------------------------------------------

    def test_html_index(self):
        p = ClamsPack(clamming)
        html_index = p.html_index()
        self.assertIn("#ClamInfo", html_index)
        self.assertIn("#ClamInfoMarkdown", html_index)
        self.assertIn("#ClamsPack", html_index)
        html_index = p.html_index(path_name="")
        self.assertIn('href="ClamInfo.html"', html_index)

    # -----------------------------------------------------------------------

    def test_readme_property(self):
        p = ClamsPack(clamming)
        readme = p.readme
        self.assertIsInstance(readme, str)

    def test_markdown_with_exporter_readme_false(self):
        p = ClamsPack(clamming)
        exporter = ExportOptions()
        exporter.readme = False
        md = p.markdown(exporter=exporter)
        self.assertTrue(md.startswith("# clamming module"))

    def test_markdown_with_exporter_readme_true(self):
        p = ClamsPack(clamming)
        exporter = ExportOptions()
        exporter.readme = True
        md = p.markdown(exporter=exporter)
        self.assertTrue(md.startswith("# clamming module"))

    def test_html_with_exporter_readme_false(self):
        p = ClamsPack(clamming)
        exporter = ExportOptions()
        exporter.readme = False
        html = p.html(exporter=exporter)
        self.assertTrue(html.startswith("<h1>clamming module</h1>"))

    def test_html_with_exporter_readme_true(self):
        p = ClamsPack(clamming)
        exporter = ExportOptions()
        exporter.readme = True
        html = p.html(exporter=exporter)
        self.assertTrue(html.startswith("<h1>clamming module</h1>"))

    def test_html_index_with_exporter(self):
        p = ClamsPack(clamming)
        exporter = ExportOptions()
        html_index = p.html_index(exporter=exporter)
        self.assertIn("clamming", html_index)

    def test_html_export_clams(self):
        import tempfile
        p = ClamsPack(clamming)
        h = ExportOptions()
        h.software = "Clamming"
        h.title = "ClammingPy tool"
        h.theme = "light"
        h.favicon = "clamming32x32.ico"
        h.copyright = clamming.__copyright__
        with tempfile.TemporaryDirectory() as tmpdir:
            out = p.html_export_clams(tmpdir, h)
            self.assertGreater(len(out), 0)
            for f in out:
                self.assertTrue(os.path.exists(f))

