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


