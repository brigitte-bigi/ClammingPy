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
        self.assertTrue("## Class `ClammingClassParser`" in md)
        self.assertTrue("## Class `ClamsClass`" in md)
        self.assertTrue("## Class `ClamsPack`" in md)
        self.assertTrue("## Class `ClamInfo`" in md)
        self.assertTrue("## Class `ClamInfoMarkdown`" in md)

    # -----------------------------------------------------------------------

    def test_html(self):
        p = ClamsPack(clamming)
        html = p.html()
        self.assertTrue(html.startswith("<h1>clamming module</h1>"))
        self.assertTrue(html.endswith(" ~</p>\n"))
        self.assertTrue("<h2>Class ClammingClassParser</h2>" in html)
        self.assertTrue("<h2>Class ClamsClass</h2>" in html)
        self.assertTrue("<h2>Class ClamsPack</h2>" in html)
        self.assertTrue("<h2>Class ClamInfo</h2>" in html)
        self.assertTrue("<h2>Class ClamInfoMarkdown</h2>" in html)

    # -----------------------------------------------------------------------

    def test_html_index(self):
        p = ClamsPack(clamming)
        html_index = p.html_index()
        self.assertTrue("#ClamInfo" in html_index)
        self.assertTrue("#ClamInfoMarkdown" in html_index)
        self.assertTrue("#ClamsPack" in html_index)
        html_index = p.html_index(path_name="")
        self.assertTrue('href="ClamInfo.html"' in html_index)

    # -----------------------------------------------------------------------

    def test_html_export(self):
        p = ClamsPack(clamming)
        h = ExportOptions()
        h.software = "Clamming"
        h.title = "ClammingPy tool"
        h.theme = "light"
        h.favicon = "clamming32x32.ico"
        h.copyright = clamming.__copyright__

        # p.html_export_clams("", h)

