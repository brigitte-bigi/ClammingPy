# makedoc.py
# Summary: Create the documentation of ClammingPy, using clamming library.
# Usage: python makedoc.py
#
# This file is part of ClammingPy tool.
# Copyright (C) 2023-2026 Brigitte Bigi, CNRS,
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

import os
from argparse import ArgumentParser

import clamming
import tests
from clamming import ClamsModules
from clamming import ExportOptions

# ###########################################################################
# Fix the default path to the "wexa_statics" folder of Whakerexa/
WEXA = './Whakerexa-2.1/wexa_statics'
# ###########################################################################


# -------------------------------------------------
# Extract args from command-line
# -------------------------------------------------

parser = ArgumentParser(usage="%s [options]" % os.path.basename(os.path.abspath(__file__)),
                        description="... a script to create ClammingPy documentation.")

parser.add_argument("-w",
                    metavar="file",
                    required=False,
                    default="",
                    help='Relative path to the "wexa_statics" folder of Whakerexa(default: {:s})'.format(WEXA))

parser.add_argument("--noreadme",
                    action='store_true',
                    help='Do not add the README file of the library')

args = parser.parse_args()


# -------------------------------------------------
# List of modules to be documented.
# --------------------------------
packages = list()
# Automatically create the documentation of all known classes of 'clamming'.
packages.append(clamming)
# The attribute __all__ is missing in 'tests' package, then no documentation
# is to be generated for it!
packages.append(tests)

# ----------------------------
# Options for exportation
# ----------------------------
opts_export = ExportOptions()
opts_export.software = 'ClammingPy ' + clamming.__version__
opts_export.url = 'https://github.com/brigitte-bigi/ClammingPy/'
opts_export.copyright = clamming.__copyright__
opts_export.title = 'ClammingPy doc'
# ... statics is the relative path to a folder with custom CSS, JS, etc.
opts_export.statics = './statics'
# ... the theme corresponds either to a statics/<theme>.css file, or "light" or "dark"
opts_export.theme = 'light'
# ... the favicon and icon are files in the statics folder
opts_export.favicon = 'clamming32x32.ico'
opts_export.icon = 'clamming.png'
# ... path to 'wexa_statics' folder, relatively to "docs"
opts_export.wexa_statics = WEXA
if args.w:
    opts_export.wexa_statics = args.w
# ... add README of each module - if exists
if args.noreadme:
    opts_export.readme = False

# -------------------------------------------------
# Generate documentation
# -------------------------------------------------
clams_modules = ClamsModules(packages)

# Export documentation into HTML files.
# One .html file = one documented class.
clams_modules.html_export_packages("docs", opts_export, "README.md")

# Export documentation into a Markdown file.
# One .md file = one documented module.
clams_modules.markdown_export_packages("docs", opts_export)
