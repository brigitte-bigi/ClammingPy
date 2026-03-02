# sample.py
#
# This file is part of ClammingPy tool.
# (C) 2023-2025 Brigitte Bigi, CNRS,
# Laboratoire Parole et Langage, Aix-en-Provence, France.
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
# along with ClammingPy. If not, see <http://www.gnu.org/licenses/>.
#
# This banner notice must not be removed.
#
# See Also:
#     - DocFormat: PEP 287 – reStructuredText Docstring Format
#     - https://docutils.sourceforge.io/rst.html
#     - https://docutils.sourceforge.io/docs/user/rst/quickref.html
# ---------------------------------------------------------------------------

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "clamming"))
from argparse import ArgumentParser

# The local version of clamming library.
from clamming import ClammingClassParser
from clamming import ClamsClass

# The class to be documented. Source code must be available.
from vehicle import Vehicle

# ----------------------------------------------------------------------------
# Verify and extract args:
# ----------------------------------------------------------------------------

parser = ArgumentParser(usage="%s --md" % os.path.basename(os.path.abspath(__file__)),
                        description="... a script to create documentation of a python class.")

parser.add_argument("--md",
                    action='store_true',
                    help="Enable markdown output instead of html")

args = parser.parse_args()

# ----------------------------------------------------------------------------
# Clamming:
# ----------------------------------------------------------------------------

# Parse the object and store collected information = clamming:
clamming_vehicle = ClammingClassParser(Vehicle)
# Get access to the members (public) and browse the data with:
# clamming.obj_clams, clamming.init_clams and clamming.fct_clams

# Retrieve the clams you collected when clamming the object:
clams = ClamsClass(clamming_vehicle)
if args.md:
    doc = clams.markdown()
else:
    doc = clams.html()

# Do whatever you want with the documentation string result:
print(doc)
