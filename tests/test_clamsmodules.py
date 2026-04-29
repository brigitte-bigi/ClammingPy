# test_clamsmodules.py
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
import tempfile

import clamming
from clamming.clamsmodules import ClamsModules
from clamming.exportoptions import ExportOptions

# ---------------------------------------------------------------------------


class TestClamsModules(unittest.TestCase):

    def test_invalid_argument(self):
        with self.assertRaises(TypeError):
            ClamsModules(clamming)

    def test_creation_empty(self):
        clams = ClamsModules([])
        self.assertIsInstance(clams, ClamsModules)

    def test_creation_with_module(self):
        clams = ClamsModules([clamming])
        self.assertIsInstance(clams, ClamsModules)

    def test_markdown_export_packages(self):
        clams = ClamsModules([clamming])
        exporter = ExportOptions()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = clams.markdown_export_packages(tmpdir, exporter)
            self.assertEqual(len(out), 1)
            self.assertTrue(os.path.exists(out[0]))
            with open(out[0], "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("clamming", content)

    def test_markdown_export_creates_directory(self):
        clams = ClamsModules([clamming])
        exporter = ExportOptions()
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "newsubdir")
            out = clams.markdown_export_packages(new_dir, exporter)
            self.assertTrue(os.path.isdir(new_dir))
            self.assertEqual(len(out), 1)

    def test_html_export_index(self):
        clams = ClamsModules([clamming])
        exporter = ExportOptions()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = clams.html_export_index(tmpdir, exporter)
            self.assertTrue(os.path.exists(out))
            with open(out, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("<!DOCTYPE html>", content)
            self.assertIn("clamming", content)

    def test_html_export_index_with_readme(self):
        clams = ClamsModules([clamming])
        exporter = ExportOptions()
        with tempfile.TemporaryDirectory() as tmpdir:
            readme_path = os.path.join(tmpdir, "README.md")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write("# Test README\n\nSome content.")
            out = clams.html_export_index(tmpdir, exporter, readme=readme_path)
            with open(out, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Test README", content)

    def test_html_export_index_with_missing_readme(self):
        clams = ClamsModules([clamming])
        exporter = ExportOptions()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = clams.html_export_index(tmpdir, exporter, readme="/nonexistent/path.md")
            self.assertTrue(os.path.exists(out))

    def test_html_export_packages(self):
        clams = ClamsModules([clamming])
        exporter = ExportOptions()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = clams.html_export_packages(tmpdir, exporter)
            self.assertTrue(len(out) > 0)
            for f in out:
                self.assertTrue(os.path.exists(f))
            index = os.path.join(tmpdir, "index.html")
            self.assertIn(index, out)

    def test_html_export_packages_multiple_modules(self):
        import unittest as ut
        clams = ClamsModules([clamming, ut])
        exporter = ExportOptions()
        with tempfile.TemporaryDirectory() as tmpdir:
            out = clams.html_export_packages(tmpdir, exporter)
            self.assertTrue(len(out) > 1)
