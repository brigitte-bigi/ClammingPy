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

    def _private_method(self):
        pass

    def __overload_method(self):
        pass

    def __str__(self):
        return self.name


class ClassWithoutDocstring:
    def __init__(self):
        self.value = 0

    def get_value(self):
        return self.value


class ClassWithoutConstructor:
    """A class with no __init__."""

    def compute(self) -> int:
        return 42


class ClassWithAsync:
    """A class with an async method."""

    async def fetch(self):
        """Fetch something asynchronously."""
        return None

# ---------------------------------------------------------------------------


class TestClassParser(unittest.TestCase):

    def test_class_parser_creation(self):
        parser = ClammingClassParser(SomeClass)
        self.assertEqual(parser.init_clams.name, "__init__")

        parser = ClammingClassParser(SomeOtherClass)
        self.assertEqual(parser.init_clams.name, "__init__")

    def test_class_parser_invalid(self):
        with self.assertRaises(TypeError):
            ClammingClassParser("not a class")
        with self.assertRaises(TypeError):
            ClammingClassParser(int)

    def test_properties(self):
        parser = ClammingClassParser(SomeClass)
        self.assertEqual(parser.obj_clams.name, "SomeClass")
        self.assertIsNotNone(parser.obj_clams.docstring)
        self.assertEqual(parser.init_clams.name, "__init__")
        self.assertIn("name", parser.init_clams.args)
        self.assertIsInstance(parser.fct_clams, dict)
        self.assertIn("lowerise", parser.fct_clams)

    def test_class_docstring_parsed(self):
        parser = ClammingClassParser(SomeClass)
        self.assertIn("short description", parser.obj_clams.docstring)

    def test_class_without_docstring(self):
        parser = ClammingClassParser(ClassWithoutDocstring)
        self.assertIsNone(parser.obj_clams.docstring)

    def test_class_without_constructor(self):
        parser = ClammingClassParser(ClassWithoutConstructor)
        self.assertEqual(parser.init_clams.name, "")

    def test_fct_clams_excludes_init(self):
        parser = ClammingClassParser(SomeClass)
        self.assertNotIn("__init__", parser.fct_clams)

    def test_fct_clams_includes_all_methods(self):
        parser = ClammingClassParser(SomeClass)
        self.assertIn("lowerise", parser.fct_clams)
        self.assertIn("_private_method", parser.fct_clams)
        self.assertIn("__str__", parser.fct_clams)

    def test_fct_clams_claminfo_fields(self):
        parser = ClammingClassParser(SomeClass)
        lowerise = parser.fct_clams["lowerise"]
        self.assertEqual(lowerise.name, "lowerise")
        self.assertIn("self", lowerise.args)
        self.assertIsInstance(lowerise.source, str)
        self.assertTrue(len(lowerise.source) > 0)

    def test_async_function_detected(self):
        parser = ClammingClassParser(ClassWithAsync)
        self.assertIn("fetch", parser.fct_clams)
        self.assertEqual(parser.fct_clams["fetch"].docstring, "Fetch something asynchronously.")
