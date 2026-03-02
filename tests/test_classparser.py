# test_classparser.py
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
from clamming.classparser import ClammingClassParser

try:
    from somewhere import SomeOtherClass
except ImportError:
    class SomeOtherClass:
        def __init__(self, *args, **kwargs):
            raise ImportError("SomeOtherClass was invalidated.")


class SomeClass:
    """Some class short description.

    :example:
    >>> c = SomeClass("toto")

    """
    def __init__(self, name: str):
        """Instantiate some class.

        :param name: (str) Some string

        """
        self.name = name

    def lowerise(self) -> str:
        return self.name.lower()

# ---------------------------------------------------------------------------


class TestClassParser(unittest.TestCase):

    def test_class_parser_creation(self):
        parser = ClammingClassParser(SomeClass)
        self.assertEqual(parser.init_clams.name, "__init__")

        parser = ClammingClassParser(SomeOtherClass)
        self.assertEqual(parser.init_clams.name, "__init__")
