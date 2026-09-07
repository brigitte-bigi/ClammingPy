"""
:filename: clamming.exportoptions.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Store the options and content for an export.

.. _This file is part of ClammingPy: https://github.com/brigitte-bigi/ClammingPy
..
    -------------------------------------------------------------------------

    Copyright (C) 2023-2025 Brigitte Bigi, CNRS
    Laboratoire Parole et Langage, Aix-en-Provence, France

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    -------------------------------------------------------------------------

"""

from __future__ import annotations
from typing import NoReturn
import logging

# ---------------------------------------------------------------------------


class ExportOptions:
    """Store the options and content for an export to documented files.

    ExportOptions is a data class, used to store options and content for
    exporting a documented file. It provides methods to set and get various
    information such as software name, copyright, icon, title, favicon, and
    theme. It also allows setting the names of the next and previous classes
    or modules for generating a table of contents (HTML only).

    :example:
    >>> h = ExportOptions()
    >>> h.software = "Clamming"
    >>> h.theme = "light"
    >>> html_head = h.get_head()
    >>> html_nav = h.get_nav()
    >>> html_footer = h.get_footer()

    """

    # ----------------------------------------------------------------------------
    # Public Constants
    # ----------------------------------------------------------------------------

    HTML_HEAD = \
        """
        <head>
            
            <title>{TITLE}</title>

            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
            <meta name="description" content="{META_DESCRIPTION}" />

            <link rel="logo icon" href="{STATICS}/{FAVICON}" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css.min/wexa.css" type="text/css" media="screen" />{THEME_LINK}
            <link rel="stylesheet" href="{WEXA_STATICS}/css.min/print.css" type="text/css" media="print" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css.min/layout.css" type="text/css" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css.min/menu.css" type="text/css" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css.min/code.css" type="text/css" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css.min/extras/book.css" type="text/css" />
            <link rel="stylesheet" href="{STATICS}/clamming.css" type="text/css" />

       </head>
       
       """

    # The theme parts of the 'head'. They are empty when no CSS theme is given.
    # 'ThemeManager' only ever swaps the 'href' of the link whose id is
    # "wexa-theme", so this link is the only one a theme is ever loaded with.

    HTML_THEME_LINK = \
        """
            <link rel="stylesheet" id="wexa-theme" href="{STATICS}/{CSS_THEME}" type="text/css" />"""

    # The loader of Whakerexa. It decides by itself whether the browser can be
    # given the modules or the bundle, registers the themes the page brings and
    # then those of the framework, and hands the namespace to 'bootPage'. It
    # stands at the end of the body, and it is the only script of a page.

    HTML_SCRIPTS = \
        """
    <script>
        /**
         * Start what this page has of its own: its table of contents, and the
         * links that carry the theme and the accessibility choices to the page
         * they open.
         *
         * @param {{Object}} wexa - The framework and the extras the loader was asked for.
         * @returns {{void}}
         */
        function bootPage(wexa) {{
            const book = new wexa.Book("main-content");
            book.fillTable(false);

            const wexaLinks = [];
            document.querySelectorAll('a.wexa-link[id]').forEach(function (a) {{ wexaLinks.push(a.id); }});
            wexa.links.handleLinksWithParameters(wexaLinks);
        }}
    </script>

    <script src="{WEXA_STATICS}/js/wexa.loader.js"
            data-base="{WEXA_STATICS}/"
            data-extras="js/extras/book.js"{THEME_DATA}></script>
"""

    # The theme the page brings, given to the loader. The themes of the
    # framework are registered after it, so the button cycles through them.

    HTML_THEME_DATA = \
        """
            data-themes-base="{WEXA_STATICS}/css.min/themes/"
            data-themes="{THEME_NAME}:{STATICS}/{CSS_THEME}"
            data-default="{THEME_NAME}" """

    HTML_BUTTONS_ACCESSIBILITY = \
        """
            <a role="button" class="skip" href="#main-content" aria-label="Go to main content">
                Go to main content
            </a>
            <nav class="nav-wexa top" aria-label="Accessibility">
                <button id="btn-contrast" class="menuitem accessibility print-off" aria-label="Contrast" aria-pressed="false" onclick="window.Wexa.accessibility.switchContrastScheme()"></button>
                <button id="btn-color" class="menuitem accessibility print-off" aria-label="Color" aria-pressed="false" onclick="window.Wexa.accessibility.switchColorScheme()"></button>{THEME_BUTTON}
            </nav>
        """

    # The button switching the theme. It is added only when a theme is given.
    # Its identifier is the one 'ThemeManager' injects its icon into.

    HTML_THEME_BUTTON = \
        """
                <button id="btn-css-theme" class="menuitem print-off" type="button" aria-label="Switch CSS theme" title="Switch CSS theme" onclick="window.themes && window.themes.next()"></button>"""
    HTML_FOOTER = \
        """
            <footer>
                <p class="copyright">{COPYRIGHT}</p>
                <p class="copyright">Powered by <a href="https://brigitte-bigi.github.io/Whakerexa/">Whakerexa</a></p>
            </footer>
        """

    # ----------------------------------------------------------------------------
    # Customized HTML information
    # ----------------------------------------------------------------------------

    # About the documented software
    DEFAULT_SOFTWARE = ""
    DEFAULT_COPYRIGHT = ""
    DEFAULT_ICON = ""
    DEFAULT_URL = ""

    # Color modes of Whakerexa requiring a class on the HTML root element.
    # The light mode is the default one, so it does not require any class.
    ROOT_COLOR_MODES = ("dark", )

    # For creating HTML pages
    DEFAULT_WEXA_STATICS = "./wexa_statics"
    DEFAULT_STATICS = "./statics"
    DEFAULT_TITLE = ""
    DEFAULT_FAVICON = "clamming32x32.ico"
    DEFAULT_THEME = "light"
    DEFAULT_LANG = "en"
    DEFAULT_ASIDE_TOC = False
    DEFAULT_CSS_THEME = ""

    # ----------------------------------------------------------------------------

    def __init__(self):
        """Create a documentation export system for a ClamsPack.

        Main functionalities:

        - Store options and content for exporting a standalone file;
        - Set and get HTML information such as software name, copyright, icon, title, favicon, and theme;
        - Set the names of the next and previous classes or modules for generating a table of contents.

        """
        self.__readme = True

        # HTML information
        self.__software = ExportOptions.DEFAULT_SOFTWARE
        self.__copyright = ExportOptions.DEFAULT_COPYRIGHT
        self.__url = ExportOptions.DEFAULT_URL
        self.__icon = ExportOptions.DEFAULT_ICON
        self.__title = ExportOptions.DEFAULT_TITLE
        self.__favicon = ExportOptions.DEFAULT_FAVICON
        self.__theme = ExportOptions.DEFAULT_THEME
        self.__lang = ExportOptions.DEFAULT_LANG
        self.__statics = ExportOptions.DEFAULT_STATICS
        self.__wexa_statics = ExportOptions.DEFAULT_WEXA_STATICS
        self.__descr = "Python class documentation"
        self.__aside_toc = ExportOptions.DEFAULT_ASIDE_TOC
        self.__css_theme = ExportOptions.DEFAULT_CSS_THEME

        # Previous and next class and module names for the TOC
        self.__next_class = None
        self.__prev_class = None
        self.__next_pack = None
        self.__prev_pack = None

    # ----------------------------------------------------------------------------

    def get_add_readme(self) -> bool:
        """Return whether the README of library is added or not."""
        return self.__readme

    def set_add_readme(self, readme: bool) -> NoReturn:
        """Set whether the README of library is added or not.

        :param readme: (bool) whether the README is added or not.

        """
        self.__readme = bool(readme)

    readme = property(get_add_readme, set_add_readme)

    # ----------------------------------------------------------------------------

    def get_aside_toc(self) -> bool:
        """Return whether the table of contents is a collapsible aside or not."""
        return self.__aside_toc

    def set_aside_toc(self, aside_toc: bool) -> NoReturn:
        """Set whether the table of contents is a collapsible aside or not.

        The table of contents is a fixed 'nav' panel by default. When it is an
        aside instead, 'book.js' hides it and adds a button to open and close it.

        :param aside_toc: (bool) whether the table of contents is an aside or not.

        """
        self.__aside_toc = bool(aside_toc)

    aside_toc = property(get_aside_toc, set_aside_toc)

    # ----------------------------------------------------------------------------

    def get_css_theme(self) -> str:
        """Return the filename of the CSS theme of the documented software."""
        return self.__css_theme

    def set_css_theme(self, name: str = DEFAULT_CSS_THEME) -> NoReturn:
        """Set the filename of the CSS theme, in the statics folder.

        A theme is a stylesheet defining colors only. When a name is given, the
        pages are opening with it, and the high-contrast theme of Whakerexa can
        be activated instead. When the name is empty, no theme is declared at
        all: the pages are the ones ClammingPy created before themes existed.

        :example:
        >>> h = ExportOptions()
        >>> h.css_theme = "clamming_theme.css"

        :param name: (str) Name of the theme file, or an empty string
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the ExportOptions.css_theme. Got {} instead."
                            "".format(name))
        self.__css_theme = name

    css_theme = property(get_css_theme, set_css_theme)

    # ----------------------------------------------------------------------------

    def get_software(self) -> str:
        """Return the name of the software."""
        return self.__software

    def set_software(self, name: str = DEFAULT_SOFTWARE) -> NoReturn:
        """Set a software name.

        :param name: (str) Name of the documented software
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.software. Got {} instead."
                            "".format(name))
        self.__software = name

    software = property(get_software, set_software)

    # ----------------------------------------------------------------------------

    def get_url(self) -> str:
        """Return the url of the software."""
        return self.__url

    def set_url(self, name: str = "") -> NoReturn:
        """Set a software url.

        :param name: (str) URL of the documented software
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.url. Got {} instead."
                            "".format(name))
        self.__url = name

    url = property(get_url, set_url)

    # ----------------------------------------------------------------------------

    def get_copyright(self) -> str:
        """Return the copyright of the HTML page."""
        return self.__copyright

    def set_copyright(self, text: str = DEFAULT_COPYRIGHT) -> NoReturn:
        """Set a copyright text, added to the footer of the page.

        :param text: (str) Copyright of the documented software
        :raises: TypeError: Given text is not a string

        """
        if isinstance(text, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.copyright. Got {} instead."
                            "".format(text))
        self.__copyright = text

    copyright = property(get_copyright, set_copyright)

    # ----------------------------------------------------------------------------

    def get_icon(self) -> str:
        """Return the icon filename of the software."""
        return self.__icon

    def set_icon(self, name: str = DEFAULT_ICON) -> NoReturn:
        """Set an icon filename.

        :param name: (str) Filename of the icon of the documented software
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.icon. Got {} instead."
                            "".format(name))
        self.__icon = name

    icon = property(get_icon, set_icon)

    # ----------------------------------------------------------------------------

    def get_title(self) -> str:
        """Return the title of the HTML page."""
        return self.__title

    def set_title(self, text: str = DEFAULT_TITLE) -> NoReturn:
        """Set a title to the output HTML pages.

        :param text: (str) Title of the HTML pages
        :raises: TypeError: Given text is not a string

        """
        if isinstance(text, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.title. Got {} instead."
                            "".format(text))
        self.__title = text

    title = property(get_title, set_title)

    # ----------------------------------------------------------------------------

    def get_statics(self) -> str:
        """Return the static path of the CSS, JS, etc."""
        return self.__statics

    def set_statics(self, name: str = DEFAULT_STATICS) -> NoReturn:
        """Set the static path of the customs CSS, JS, etc.

        :param name: (str) Path of the static elements
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.statics. Got {} instead."
                            "".format(name))
        self.__statics = name

    statics = property(get_statics, set_statics)

    # ----------------------------------------------------------------------------

    def get_wexa_statics(self) -> str:
        """Return the static path of the CSS, JS, etc. of Whakerexa. """
        return self.__wexa_statics

    def set_wexa_statics(self, name: str = DEFAULT_WEXA_STATICS) -> NoReturn:
        """Set the static path of the customs CSS, JS, etc. of Whakerexa.

        :param name: (str) Path of the static elements
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.wexa_statics. Got {} instead."
                            "".format(name))
        self.__wexa_statics = name

    wexa_statics = property(get_wexa_statics, set_wexa_statics)

    # ----------------------------------------------------------------------------

    def get_favicon(self) -> str:
        """Return the favicon filename of the HTML pages."""
        return self.__favicon

    def set_favicon(self, name: str = DEFAULT_FAVICON) -> NoReturn:
        """Set a favicon to the output HTML pages.

        :param name: (str) Favicon of the HTML pages
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.favicon. Got {} instead."
                            "".format(name))
        self.__favicon = name

    favicon = property(get_favicon, set_favicon)

    # ----------------------------------------------------------------------------

    def get_theme(self) -> str:
        """Return the theme of the HTML page."""
        return self.__theme

    def set_theme(self, name: str = DEFAULT_THEME) -> NoReturn:
        """Set a theme name.

        :param name: (str) Name of the theme of the HTML pages
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.theme. Got {} instead."
                            "".format(name))
        self.__theme = name

    theme = property(get_theme, set_theme)

    # ----------------------------------------------------------------------------

    def get_root_class(self) -> str:
        """Return the 'class' attribute value of the HTML root element.

        Since Whakerexa 3.0, the color mode is a class of ':root' -- it was a
        class of 'body' before. The light mode being the default one, it is
        represented by an empty class.

        """
        if self.__theme in ExportOptions.ROOT_COLOR_MODES:
            return self.__theme
        return ""

    # ----------------------------------------------------------------------------

    def get_lang(self) -> str:
        """Return the language code of the HTML pages."""
        return self.__lang

    def set_lang(self, name: str = DEFAULT_LANG) -> NoReturn:
        """Set the language code of the HTML pages.

        :param name: (str) BCP 47 language tag, e.g. 'en', 'fr', 'es'
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the ExportOptions.lang. Got {} instead."
                            "".format(name))
        self.__lang = name

    lang = property(get_lang, set_lang)

    # ----------------------------------------------------------------------------

    def get_description(self) -> str:
        """Return the 160 chars description of the HTML page."""
        return self.__descr

    def set_description(self, descr: str = "") -> NoReturn:
        """Set a 160 chars max description text.

        :param descr: (str) Description of the documented document
        :raises: TypeError: Given descr is not a string

        """
        if isinstance(descr, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.descr. Got {} instead."
                            "".format(descr))
        descr = descr.replace("\n", " ")
        descr = descr.replace("'", " ")
        descr = descr.replace('"', " ")
        if len(descr) < 90:
            logging.warning(f"Given description is a little bit shorted than the 90 expected characters: {descr}")
            descr = "Python Class Documentation of " + descr
        if len(descr) > 160:
            logging.warning(f"Given description is longer than 160 characters: {descr}.")
        self.__descr = descr[:160]

    description = property(get_description, set_description)

    # ----------------------------------------------------------------------------

    def get_next_class(self) -> str:
        """Return the name of the next documented class."""
        return self.__next_class

    def set_next_class(self, name: str | None = None) -> NoReturn:
        """Set the name of the next documented class.

        :param name: (str|None) Name of the next documented class
        :raises: TypeError: Given name is not a string

        """
        if name is not None and isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' or None for the HTMLDocExport.next_class. Got {} instead."
                            "".format(name))
        self.__next_class = name

    next_class = property(get_next_class, set_next_class)

    # ----------------------------------------------------------------------------

    def get_prev_class(self) -> str:
        """Return the name of the previous documented class, for the ToC."""
        return self.__prev_class

    def set_prev_class(self, name: str | None = None) -> NoReturn:
        """Set the name of the previous documented class.

        :param name: (str|None) Name of the previous documented class
        :raises: TypeError: Given name is not a string

        """
        if name is not None and isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' or None for the HTMLDocExport.prev_class. "
                            "Got {} instead.".format(name))
        self.__prev_class = name

    prev_class = property(get_prev_class, set_prev_class)

    # ----------------------------------------------------------------------------

    def get_next_module(self) -> str:
        """Return the name of the next documented module."""
        return self.__next_pack

    def set_next_module(self, name: str | None = None) -> NoReturn:
        """Set the name of the next documented module.

        :param name: (str|None) Name of the next documented module
        :raises: TypeError: Given name is not a string

        """
        if name is not None and isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' or None for the HTMLDocExport.next_module. "
                            "Got {} instead.".format(name))
        self.__next_pack = name

    next_module = property(get_next_module, set_next_module)

    # ----------------------------------------------------------------------------

    def get_prev_module(self) -> str:
        """Return the name of the previous documented module, for the ToC."""
        return self.__prev_pack

    def set_prev_module(self, name: str | None = None) -> NoReturn:
        """Set the name of the previous documented module.

        :param name: (str|None) Name of the previous documented module
        :raises: TypeError: Given name is not a string

        """
        if name is not None and isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' or None for the HTMLDocExport.prev_module. "
                            "Got {} instead.".format(name))
        self.__prev_pack = name

    prev_module = property(get_prev_module, set_prev_module)

    # ----------------------------------------------------------------------------
    # Export of the HTML contents
    # ----------------------------------------------------------------------------

    def get_head(self) -> str:
        """Return the HTML 'head' of the page."""
        return ExportOptions.HTML_HEAD.format(
            TITLE=self.__title,
            FAVICON=self.__favicon,
            THEME=self.__theme,
            STATICS=self.__statics,
            WEXA_STATICS=self.__wexa_statics,
            META_DESCRIPTION=self.__descr,
            THEME_LINK=self.__theme_part(ExportOptions.HTML_THEME_LINK)
        )

    # ----------------------------------------------------------------------------

    def get_scripts(self) -> str:
        """Return the scripts of the page, to be added at the end of its body.

        The loader of Whakerexa is the only script a page carries: it decides
        whether the browser is given the modules or the bundle, registers the
        themes, and calls 'bootPage' with what it loaded.

        :return: (str) HTML code

        """
        return ExportOptions.HTML_SCRIPTS.format(
            WEXA_STATICS=self.__wexa_statics,
            THEME_DATA=self.__theme_part(ExportOptions.HTML_THEME_DATA)
        )

    # ----------------------------------------------------------------------------

    def __theme_part(self, template: str) -> str:
        """Return the given part of the page filled with the theme information.

        The name a theme is registered with is the name of its file, without the
        extension: it is what the browser address shows when the reader switched.

        :param template: (str) One of the HTML_THEME_* templates
        :return: (str) The filled template, or an empty string if no theme is set

        """
        if len(self.__css_theme) == 0:
            return ""
        theme_name = self.__css_theme
        if "." in theme_name:
            theme_name = theme_name[:theme_name.rindex(".")]
        return template.format(
            STATICS=self.__statics,
            WEXA_STATICS=self.__wexa_statics,
            CSS_THEME=self.__css_theme,
            THEME_NAME=theme_name
        )

    # ----------------------------------------------------------------------------

    def get_header(self) -> str:
        """Return the 'header' of the HTML->body of the page."""
        h = list()
        h.append("    <header>")
        theme_button = ""
        if len(self.__css_theme) > 0:
            theme_button = ExportOptions.HTML_THEME_BUTTON
        h.append(ExportOptions.HTML_BUTTONS_ACCESSIBILITY.format(THEME_BUTTON=theme_button))
        if len(self.__software) > 0:
            h.append("    <h1>{SOFTWARE}</h1>".format(SOFTWARE=self.__software))
        if len(self.__icon) > 0:
            h.append('        <p><img class="small-logo" src="{STATICS}/{ICON}" '
                     'alt="Software logo"/></p>'.format(STATICS=self.__statics, ICON=self.__icon))
        if len(self.__url) > 0:
            h.append('        <p><a class="external-link" href="{URL}">{URL}</a></p>'.format(URL=self.__url))
        h.append("    </header>")
        return "\n".join(h)

    # ----------------------------------------------------------------------------

    def get_nav(self) -> str:
        """Return the 'nav' of the HTML->body of the page."""
        nav = list()
        if self.__aside_toc is True:
            tag_name = "aside"
            class_name = "book-toc-aside"
        else:
            tag_name = "nav"
            class_name = "book-toc"
        nav.append("<{TAG} id=\"nav-book\" class=\"{CLASS}\" aria-label=\"Table of contents\">"
                   "".format(TAG=tag_name, CLASS=class_name))
        if self.__aside_toc is True:
            # 'book.js' labels the button it adds with the first title of the
            # panel, so this title says what the button opens. The name of the
            # software, its logo and its address are in the header of the page:
            # a panel that is hidden most of the time does not repeat them.
            nav.append("    <h1>Table of Contents</h1>")
        else:
            if self.__software == ExportOptions.DEFAULT_SOFTWARE:
                nav.append("    <h1>Documentation</h1>")
            else:
                nav.append("    <h1>{SOFTWARE}</h1>".format(SOFTWARE=self.__software))
            if len(self.__icon) > 0:
                nav.append("    <img class=\"small-logo center\" src=\"{STATICS}/{ICON}\" alt=\"\"/>"
                           "".format(STATICS=self.__statics, ICON=self.__icon))
            if len(self.__url) > 0:
                nav.append('        <p><a class="external-link" href="{URL}">{URL}</a></p>'.format(URL=self.__url))
        nav.append("    <ul>")
        nav.append(ExportOptions.__nav_link("&crarr; Prev. Module", self.__prev_pack, "nav-prev-module"))
        nav.append(ExportOptions.__nav_link("&uarr; Prev. Class", self.__prev_class, "nav-prev-class"))
        nav.append(ExportOptions.__nav_link("&#8962; Index", "index.html", "nav-index"))
        nav.append(ExportOptions.__nav_link("&darr; Next Class", self.__next_class, "nav-next-class"))
        nav.append(ExportOptions.__nav_link("&rdsh; Next Module", self.__next_pack, "nav-next-module"))
        nav.append("    </ul>")
        if self.__aside_toc is False:
            nav.append("    <h2>Table of Contents</h2>")
        nav.append("    <ul id=\"toc\"></ul>")
        nav.append("    <hr>")
        nav.append("    <p><small>Automatically created</small></p><p><small>by <a class=\"external-link\" href=\"https://github.com/brigitte-bigi/ClammingPy\">ClammingPy</a></small></p>")
        nav.append("</{TAG}>".format(TAG=tag_name))
        return "\n".join(nav)

    # -----------------------------------------------------------------------

    def get_footer(self) -> str:
        """Return the 'footer' of the HTML->body of the page."""
        return ExportOptions.HTML_FOOTER.format(COPYRIGHT=self.__copyright)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    @staticmethod
    def __nav_link(text: str, link: str | None, identifier: str) -> str:
        """Return a link of the navigation.

        The 'wexa-link' class is the one the page collects to hand its links to
        'LinkController': a link handled by it carries the framework parameters
        -- the theme, the contrast and the color -- to the page it opens.

        :param text: (str) Content of the link
        :param link: (str|None) Target of the link, or None for a disabled one
        :param identifier: (str) Identifier of the link, required by 'LinkController'
        :return: (str) HTML code

        """
        if link is None:
            a = 'aria-disabled="true"'
        else:
            a = 'href="{:s}" class="wexa-link" data-target="_self"'.format(link)
        return """<li><a role="button" tabindex="0" id="{ID}" {LINK}> {TEXT}</a></li>""".format(
            ID=identifier, LINK=a, TEXT=text)
