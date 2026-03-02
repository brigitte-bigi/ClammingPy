# main.py
# Summary: Create the documentation of a module, using ClammingPy library.
# Usage: python main.py --help
#
# This file is part of ClammingPy tool.
# Copyright (C) 2023-2025 Brigitte Bigi, CNRS,
# Laboratoire Parole et Langage, Aix-en-Provence, France.
#
# Use of this software is governed by the GNU Affero Public License, version 3.
#
# ClammingPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ClammingPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ClammingPy. If not, see <http://www.gnu.org/licenses/>.
#
# This banner notice must not be removed.
#
# ---------------------------------------------------------------------------

from __future__ import annotations
import os
import sys
import importlib
from argparse import ArgumentParser

import clamming

# ----------------------------------------------------------------------------
# Verify and extract args:
# ----------------------------------------------------------------------------


parser = ArgumentParser(usage="%s [options]" % os.path.basename(os.path.abspath(__file__)),
                        description="... create documentation of a python class or module.")

parser.add_argument("--md",
                    action='store_true',
                    help="Enable Markdown output instead of HTML")

parser.add_argument("-c",
                    metavar="str",
                    required=False,
                    help="Name of the class to be documented")

parser.add_argument("-m",
                    metavar="str",
                    required=True,
                    help="Name of the module")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# At least one argument is expected. If not, add help.
if len(sys.argv) <= 1:
    sys.argv.append('-h')

args = parser.parse_args()

# ---------------------------------------------------------------------------
# Import the given module

try:
    module = importlib.import_module(args.m)
except ModuleNotFoundError as e:
    print("Invalid module name: {:s}".format(str(e)))
    sys.exit(-1)

# ---------------------------------------------------------------------------
# Print the doc

if args.c:
    # Create the documentation of a single class of the Python module
    # ---------------------------------------------------------------
    # Turn the given string into a class
    c = clamming.ClamUtils().get_class(args.c, args.m)
    # Create the documentation of the class
    parser = clamming.ClammingClassParser(c)
    clams_class = clamming.ClamsClass(parser)
    # Print in the requested format
    if args.md:
        print(clams_class.markdown())
    else:
        print(clams_class.html())

else:
    # Create the documentation of all classes of the Python module
    # ------------------------------------------------------------
    # Exportation default options
    exporter = clamming.ExportOptions()
    # Package parser
    clams_pack = clamming.ClamsPack(module)
    # Print in the requested format
    if args.md:
        print(clams_pack.markdown(exporter))
    else:
        print(clams_pack.html(exporter))
