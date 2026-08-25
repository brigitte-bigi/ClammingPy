# test_exportoptions.py
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

from clamming.exportoptions import ExportOptions

# ---------------------------------------------------------------------------


class TestHTMLDocExport(unittest.TestCase):

    def test_instantiate(self):
        opts_export = ExportOptions()
        self.assertTrue(opts_export._ExportOptions__readme)
        self.assertEqual(opts_export._ExportOptions__software, ExportOptions.DEFAULT_SOFTWARE)
        self.assertEqual(opts_export._ExportOptions__url, ExportOptions.DEFAULT_URL)
        self.assertEqual(opts_export._ExportOptions__title, ExportOptions.DEFAULT_TITLE)
        self.assertEqual(opts_export._ExportOptions__favicon, 'clamming32x32.ico')
        # self.assertEqual(opts_export.theme, 'light')
        self.assertIsNone(opts_export._ExportOptions__next_class)
        self.assertIsNone(opts_export._ExportOptions__prev_class)
        self.assertIsNone(opts_export._ExportOptions__next_pack)
        self.assertIsNone(opts_export._ExportOptions__prev_pack)

    # ----------------------------------------------------------------------------

    def test_getters_setters_properties(self):
        opts_export = ExportOptions()
        opts_export.readme = False
        opts_export.software = 'Clamming'
        opts_export.url = 'https://clamming.sf.net'
        opts_export.title = 'HTML Export'
        opts_export.favicon = 'favicon.ico'
        opts_export.theme = 'dark'
        opts_export.next_class = 'NextClass'
        opts_export.prev_class = 'PrevClass'
        opts_export.next_module = 'NextModule'
        opts_export.prev_module = 'PrevModule'

        self.assertFalse(opts_export.readme)
        self.assertEqual(opts_export.software, 'Clamming')
        self.assertEqual(opts_export.url, 'https://clamming.sf.net')
        self.assertEqual(opts_export.title, 'HTML Export')
        self.assertEqual(opts_export.favicon, 'favicon.ico')
        self.assertEqual(opts_export.theme, 'dark')
        self.assertEqual(opts_export.next_class, 'NextClass')
        self.assertEqual(opts_export.prev_class, 'PrevClass')
        self.assertEqual(opts_export.next_module, 'NextModule')
        self.assertEqual(opts_export.prev_module, 'PrevModule')

        opts_export.next_class = None
        opts_export.prev_class = None
        opts_export.next_module = None
        opts_export.prev_module = None

        self.assertIsNone(opts_export.next_class)
        self.assertIsNone(opts_export.prev_class)
        self.assertIsNone(opts_export.next_module)
        self.assertIsNone(opts_export.prev_module)

        with self.assertRaises(TypeError):
            opts_export.software = None
        with self.assertRaises(TypeError):
            opts_export.title = None
        with self.assertRaises(TypeError):
            opts_export.favicon = None
        with self.assertRaises(TypeError):
            opts_export.theme = None

        with self.assertRaises(TypeError):
            opts_export.next_class = 123
        with self.assertRaises(TypeError):
            opts_export.prev_class = 123
        with self.assertRaises(TypeError):
            opts_export.next_module = 123
        with self.assertRaises(TypeError):
            opts_export.prev_module = 123

        opts_export.readme = 1
        self.assertTrue(opts_export.readme)
        opts_export.readme = 0
        self.assertFalse(opts_export.readme)

    # ----------------------------------------------------------------------------

    def test_lang_setter(self):
        opts_export = ExportOptions()
        self.assertEqual(opts_export.lang, "en")
        opts_export.lang = "fr"
        self.assertEqual(opts_export.lang, "fr")
        with self.assertRaises(TypeError):
            opts_export.lang = 42

    def test_get_head(self):
        opts_export = ExportOptions()
        opts_export.title = 'HTML Export'
        opts_export.favicon = 'favicon.ico'
        opts_export.theme = 'dark'
        actual_head = opts_export.get_head().strip()

        self.assertTrue(actual_head.startswith("<head>"))
        self.assertTrue(actual_head.endswith("</head>"))
        self.assertIn("<title>HTML Export</title>", actual_head)
        self.assertIn('<link rel="logo icon" href="./statics/favicon.ico" />', actual_head)
        self.assertIn('href="./wexa_statics/css/wexa.css"', actual_head)
        self.assertIn('href="./wexa_statics/css/print.css"', actual_head)
        self.assertIn('href="./wexa_statics/css/layout.css"', actual_head)
        self.assertIn('href="./wexa_statics/css/menu.css"', actual_head)
        self.assertIn('href="./wexa_statics/css/code.css"', actual_head)
        self.assertIn('href="./wexa_statics/css/extras/book.css"', actual_head)
        self.assertIn('href="./statics/clamming.css"', actual_head)

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    def test_get_header(self):
        opts_export = ExportOptions()
        header = opts_export.get_header()
        self.assertIn("<header>", header)
        self.assertIn("</header>", header)
        self.assertIn("main-content", header)

    def test_get_header_with_software_icon_url(self):
        opts_export = ExportOptions()
        opts_export.software = "MySoftware"
        opts_export.icon = "logo.png"
        opts_export.url = "https://example.com"
        header = opts_export.get_header()
        self.assertIn("MySoftware", header)
        self.assertIn("logo.png", header)
        self.assertIn("https://example.com", header)

    def test_get_nav(self):
        opts_export = ExportOptions()
        nav = opts_export.get_nav()
        self.assertIn("<nav", nav)
        self.assertIn("</nav>", nav)
        self.assertIn("index.html", nav)

    def test_get_nav_with_prev_next(self):
        opts_export = ExportOptions()
        opts_export.next_class = "NextClass.html"
        opts_export.prev_class = "PrevClass.html"
        opts_export.next_module = "NextModule.html"
        opts_export.prev_module = "PrevModule.html"
        nav = opts_export.get_nav()
        self.assertIn("NextClass.html", nav)
        self.assertIn("PrevClass.html", nav)
        self.assertIn("NextModule.html", nav)
        self.assertIn("PrevModule.html", nav)

    def test_get_nav_disabled_links(self):
        opts_export = ExportOptions()
        nav = opts_export.get_nav()
        self.assertIn('aria-disabled="true"', nav)

    def test_css_theme_setter(self):
        opts_export = ExportOptions()
        self.assertEqual(opts_export.css_theme, "")
        opts_export.css_theme = "clamming_theme.css"
        self.assertEqual(opts_export.css_theme, "clamming_theme.css")
        with self.assertRaises(TypeError):
            opts_export.css_theme = 42

    def test_get_head_without_css_theme(self):
        """No theme is named, so the head is the one of the pages made before themes."""
        opts_export = ExportOptions()
        actual_head = opts_export.get_head()

        self.assertNotIn("wexa-theme", actual_head)
        self.assertNotIn("ThemeManager", actual_head)
        self.assertNotIn("theme_manager.js", actual_head)
        self.assertNotIn("highcontrast", actual_head)

    def test_get_head_with_css_theme(self):
        """The theme is linked once, and registered in both loading paths."""
        opts_export = ExportOptions()
        opts_export.css_theme = "clamming_theme.css"
        actual_head = opts_export.get_head()

        self.assertEqual(1, actual_head.count('id="wexa-theme"'))
        self.assertIn('href="./statics/clamming_theme.css"', actual_head)
        self.assertEqual(2, actual_head.count("themes.setDefault('clamming_theme')"))
        self.assertEqual(2, actual_head.count("wexa_theme_highcontrast.css"))
        self.assertEqual(1, actual_head.count("theme_manager.js"))
        self.assertEqual(1, actual_head.count("new window.Wexa.ThemeManager()"))

    def test_get_head_css_theme_registered_name(self):
        """A theme is registered with the name of its file, extension excluded."""
        opts_export = ExportOptions()
        opts_export.statics = "./css"
        opts_export.css_theme = "my.theme.css"
        actual_head = opts_export.get_head()

        self.assertIn('href="./css/my.theme.css"', actual_head)
        self.assertEqual(2, actual_head.count("themes.setDefault('my.theme')"))

    def test_get_nav_links_are_handled(self):
        """A link of the navigation is identified, so 'LinkController' can carry the parameters."""
        opts_export = ExportOptions()
        opts_export.next_class = "NextClass.html"
        nav = opts_export.get_nav()

        self.assertIn('id="nav-index"', nav)
        self.assertIn('id="nav-next-class"', nav)
        self.assertEqual(2, nav.count('class="wexa-link"'))
        self.assertEqual(2, nav.count('data-target="_self"'))
        self.assertIn('aria-disabled="true"', nav)

    def test_get_head_links_with_parameters(self):
        """The links are handed to 'LinkController' in both loading paths, and only with a theme."""
        opts_export = ExportOptions()
        self.assertNotIn("handleLinksWithParameters", opts_export.get_head())

        opts_export.css_theme = "clamming_theme.css"
        actual_head = opts_export.get_head()
        self.assertEqual(2, actual_head.count("handleLinksWithParameters(wexaLinks)"))
        self.assertEqual(2, actual_head.count("a.wexa-link[id]"))

    def test_get_header_theme_button(self):
        """The switch is offered only when there is a theme to switch."""
        opts_export = ExportOptions()
        self.assertNotIn("btn-css-theme", opts_export.get_header())

        opts_export.css_theme = "clamming_theme.css"
        header = opts_export.get_header()
        self.assertIn('id="btn-css-theme"', header)
        self.assertIn("window.themes.next()", header)
        self.assertIn('id="btn-contrast"', header)
        self.assertIn('id="btn-color"', header)

    def test_aside_toc_setter(self):
        opts_export = ExportOptions()
        self.assertFalse(opts_export.aside_toc)
        opts_export.aside_toc = True
        self.assertTrue(opts_export.aside_toc)
        opts_export.aside_toc = 0
        self.assertFalse(opts_export.aside_toc)

    def test_get_nav_aside_toc(self):
        """The table of contents is an aside, so 'book.js' makes it collapsible."""
        opts_export = ExportOptions()
        opts_export.aside_toc = True
        nav = opts_export.get_nav()
        self.assertIn('<aside id="nav-book" class="book-toc-aside"', nav)
        self.assertIn("</aside>", nav)
        self.assertNotIn("<nav", nav)
        self.assertNotIn("</nav>", nav)
        self.assertIn('<ul id="toc">', nav)

    def test_get_nav_aside_toc_first_title(self):
        """The first title of the panel is the label 'book.js' gives to its button."""
        opts_export = ExportOptions()
        opts_export.software = "ClammingPy 3.0"
        opts_export.icon = "clamming.png"
        opts_export.url = "https://clamming.sf.net"
        opts_export.aside_toc = True
        nav = opts_export.get_nav()

        first_title = nav[nav.index("<h1>"):nav.index("</h1>") + 5]
        self.assertEqual("<h1>Table of Contents</h1>", first_title)
        self.assertEqual(1, nav.count("Table of Contents"))
        self.assertNotIn("ClammingPy 3.0", nav)
        self.assertNotIn("clamming.png", nav)

    def test_get_nav_fixed_toc(self):
        """The table of contents is a nav, so it is always shown."""
        opts_export = ExportOptions()
        nav = opts_export.get_nav()
        self.assertIn('<nav id="nav-book" class="book-toc"', nav)
        self.assertIn("</nav>", nav)
        self.assertNotIn("<aside", nav)
        self.assertIn('<ul id="toc">', nav)

    def test_get_footer(self):
        opts_export = ExportOptions()
        opts_export.copyright = "© 2025 Me"
        footer = opts_export.get_footer()
        self.assertIn("<footer>", footer)
        self.assertIn("© 2025 Me", footer)

    def test_get_statics_setters(self):
        opts_export = ExportOptions()
        opts_export.statics = "./my_statics"
        self.assertEqual(opts_export.statics, "./my_statics")
        opts_export.wexa_statics = "./my_wexa"
        self.assertEqual(opts_export.wexa_statics, "./my_wexa")
        with self.assertRaises(TypeError):
            opts_export.statics = 123
        with self.assertRaises(TypeError):
            opts_export.wexa_statics = 123

    def test_copyright_setter(self):
        opts_export = ExportOptions()
        opts_export.copyright = "© 2025"
        self.assertEqual(opts_export.copyright, "© 2025")
        with self.assertRaises(TypeError):
            opts_export.copyright = 42

    def test_icon_setter(self):
        opts_export = ExportOptions()
        opts_export.icon = "icon.png"
        self.assertEqual(opts_export.icon, "icon.png")
        with self.assertRaises(TypeError):
            opts_export.icon = 42

    def test_description_setter(self):
        opts_export = ExportOptions()
        long_descr = "A" * 100
        opts_export.description = long_descr
        self.assertLessEqual(len(opts_export.description), 160)
        with self.assertRaises(TypeError):
            opts_export.description = 123

    def test_description_too_long_truncated(self):
        opts_export = ExportOptions()
        opts_export.description = "A" * 200
        self.assertEqual(len(opts_export.description), 160)

