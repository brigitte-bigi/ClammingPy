# ClammingPy Description

## Overview

> ClammingPy is a Light Python-API Documentation in Markdown and HTML

### Typical use

You have a Python API you documented with docstrings, and you want to share documentation in either Markdown or HTML.
ClammingPy is the documentation generator you may need: it is generating Markdown or HTML from the docstrings within the source code of any Python library.

> ClammingPy generates HTML-5 with a high level of WCAG 2.1 conformity.

### Features

Python modules are usually documented using docstrings. They typically use plain text markup formats such as reStructuredText (reST, the markup used for writing the official Python documentation) and/or Markdown.
`ClammingPy` is a Python, free, open-source, self-hosted library to export a Python class or module into a Markdown and/or HTML files, for documentation purpose. Contrariwise to other documentation tools, docstrings are analyzed with **flexibility rather than completeness...**

> Both ReST and Epydoc field styles are supported. It means that either ':field:' or '@field:' can be used indifferently, with upper- or lower- cases.

Two very useful reST non-standard field items can also be used in the docstrings: `:example:` and `:code:`. 
Finally, some variants in field names are supported:

- `:return:` or `:returns:` are both interpreted the same way;
- `:raise:` or `:raises:` or `:catch:` or `:except:` are all interpreted the same way.


### Main advantages

- easily customizable: it's a pure python library in Object-Oriented Programming
- open-source: easily add new features and functionalities 
- scalable: no limit to support numerous modules
- inclusive: the documentation is highly WCAG 2.1 compliant


## Install ClammingPy

Get it here: <https://sourceforge.net/projects/clamming/>.

ClammingPy requires Whakerexa to be installed; it can be downloaded from: <https://whakerexa.sf.net>. Get its documentation here: <https://whakerexa.sourceforge.io>.
Unpack it into the `ClammingPy/docs` folder.

### From the repo:

Download the repository and unpack it. ClammingPy tool includes the following folders and files:

1. `clamming`: the source code of `ClammingPy` library
2. `docs`: the documentation of clamming library in HTML, already including "wexa_statics".
3. `tests`: unittest of `Clamming` library
4. `sample`: a sample class `Vehicle` to illustrate `clamming` use
5. `makedoc.py`: create the ClammingPy documentation, using `clamming` library
6. `etc`: etcetera!

### From the package:

Install it in your python environment from the local wheel with:

```bash
> python -m pip install dist/<clamming.whl>
```


## Quick start

### Documenting a single class

The `sample` folder contains a Python class example and the simplest solution to get access to the documentation either in Markdown or HTML. The `Vehicle` class is illustrating the supported format and its flexibility. Try it with:

```bash
> cd sample
> python makedoc_vehicle.py > vehicle.html
> python makedoc_vehicle.py --md > vehicle.md
```

or with the main program:
```bash
> python main.py -c Vehicle -m sample.vehicle
> python main.py -c Vehicle -m sample.vehicle --md
```

In the same way, the documentation of any Python class can be extracted with, for example:

```bash
> python main.py -c TestCase -m unittest --md
> python main.py -c BaseHTTPRequestHandler -m http.server --md
```

When using the `ClammingPy` library directly, the documented files can be obtained with the following Python code:

```python
>>> import clamming
>>> import Vehicle  # Or any other Python class to be documented
>>> parser = clamming.ClammingClassParser(Vehicle)
>>> clams = clamming.ClamsClass(parser)
>>> print(clams.html())
>>> print(clams.markdown())
```

### Documenting all classes of a module

Below are two examples with the main program:
```bash
> python main.py -m clamming > clamming.html
> python main.py -m http.server --md | grep "### Class "
### Class `HTTPServer`
### Class `ThreadingHTTPServer`
### Class `BaseHTTPRequestHandler`
### Class `SimpleHTTPRequestHandler`
### Class `CGIHTTPRequestHandler`
```

The following Python code allows to generate the documentation of `clamming`
module in Mardown format or in HTML format as a standalone content:

```python
>>> import clamming
>>> clams_pack = clamming.ClamsPack(clamming)
>>> print(clams_pack.markdown())
>>> print(clams_pack.html())
```

Here is a summary of the main steps to generate an HTML documentation, in a bunch of HTML files:

```python
>> > import clamming
>> >  # Options for HTML exportation
>> > html_export = clamming.ExportOptions()
>> > html_export.software = 'ClammingPy ' + clamming.__version__
>> >  # Create an HTML page for each class of the module
>> > clams_pack = clamming.ClamsPack(clamming)
>> > clams_pack.html_export_clams("docs", html_export)
```

### Documenting all classes of a list of modules

There is an all-in-one function to generate the HTML documentation of a list of packages. It requires to define the followings:

1. The list of ClamsPack instances of the modules to be documented;
2. The HTMLDocExport allowing to fix the HTML options for files exportation.

```python
>> > import clamming
>> >  # List of modules to be documented.
>> > packages = list()
>> > packages.append(clamming)
>> >  # Options for HTML exportation
>> > html_export = clamming.ExportOptions()
>> > html_export.wexa_statics = '../Whakerexa-0.4/wexa_statics'
>> > html_export.software = 'ClammingPy ' + clamming.__version__
>> >  # Export documentation to HTML files into the "docs" folder.
>> > m = clamming.ClamsModules(packages)
>> > m.html_export_packages("docs", html_export)
>> >  # Export documentation to Markdown files into the "docs" folder.
>> > m.markdown_export_packages("docs")
```

See `makedoc.py` Python script for details.

> See the ClammingPy documentation in `docs` folder for extended usages.



## How to cite ClamminPy

By using ClammingPy, you are encouraged to mention it in your publications 
or products, in accordance with the best practices of the AGPL license.

Use one of the following reference to cite ClammingPy:

> Brigitte Bigi. ClammingPy - Light Python-API Documentation in Markdown and HTML,
> Version 1.9. 2024. <https://hal.science/hal-04392103>


## Projects using ClammingPy

- WhakerPy: <https://whakerpy.sf.net>
- WhintPy: <https://whintpy.sourceforge.io>
- AudiooPy: <https://audioopy.sf.net>
- PyMancala: <https://pymancala.sf.net>
- SPPAS: <https://sppas.org/api/index.html>
- *contact the author if you want to add a project here*


## Help / How to contribute

If you plan to contribute to the code or to report a bug, please send an e-mail to the author.
Any and all constructive comments are welcome.


## License/Copyright

See the accompanying LICENSE and AUTHORS files for the full list of contributors.

Copyright (C) 2023-2024  - [Brigitte Bigi](https://sppas.org/bigi/) - <contact@sppas.org>
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
along with this program. If not, see <https://www.gnu.org/licenses/>.

