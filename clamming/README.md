```
-----------------------------------------------------------------------------

  ██████╗ ██╗       █████╗  ███╗   ███╗ ███╗   ███╗ ██╗ ███╗   ██╗  ██████╗
 ██╔════╝ ██║      ██╔══██╗ ████╗ ████║ ████╗ ████║ ██║ ████╗  ██║ ██╔════╝ 
 ██║      ██║      ███████║ ██╔████╔██║ ██╔████╔██║ ██║ ██╔██╗ ██║ ██║  ███╗
 ██║      ██║      ██╔══██║ ██║╚██╔╝██║ ██║╚██╔╝██║ ██║ ██║╚██╗██║ ██║   ██║  
 ╚██████╗ ███████╗ ██║  ██║ ██║ ╚═╝ ██║ ██║ ╚═╝ ██║ ██║ ██║ ╚████║ ╚██████╔╝
  ╚═════╝ ╚══════╝ ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚═╝     ╚═╝ ╚═╝ ╚═╝  ╚═══╝  ╚═════╝                                                                              

            a Python library to generate accessible documentation

            Copyright (C) 2023-2026, Brigitte Bigi, CNRS
            Laboratoire Parole et Langage, Aix-en-Provence, France
-----------------------------------------------------------------------------
```

## Usage

### Documenting a single class

The documented files can be obtained with the following Python code:

```python
>>> import clamming
>>> import Vehicle  # Or any other Python class to be documented
>>> parser = clamming.ClammingClassParser(Vehicle)
>>> clams = clamming.ClamsClass(parser)
>>> print(clams.html())
>>> print(clams.markdown())
```

### Documenting all classes of a module

The following Python code allows to generate the documentation of `clamming`
module in Mardown format or in HTML format as a standalone content:

```python
>>> import clamming
>>> clams_pack = clamming.ClamsPack(clamming)
>>> print(clams_pack.markdown())
>>> print(clams_pack.html())
```

The exportation can be customized:

```python
>>> import clamming
>>> # Options for exportation
>>> html_export = clamming.ExportOptions()
>>> html_export.software = 'ClammingPy ' + clamming.__version__
```

### Documenting all classes of a list of modules

There is an all-in-one class allowing to generate the documentation of a list of packages. 

```python
>>> import clamming
>>> import tests
>>> # List of modules to be documented.
>>> packages = list()
>>> packages.append(clamming)
>>> packages.append(tests)
>>> # Options for exportation
>>> export = clamming.ExportOptions()
>>> export.wexa_statics = '../Whakerexa-2.0/wexa_statics'
>>> export.software = 'ClammingPy ' + clamming.__version__
>>> # Export documentation to HTML files into the "docs" folder.
>>> m = clamming.ClamsModules(packages)
>>> m.html_export_packages("docs", export)
>>> # Export documentation to Markdown files into the "docs" folder.
>>> m.markdown_export_packages("docs", export)
```


## License/Copyright

Copyright (C) 2023-2026 - [Brigitte Bigi](https://sppas.org/bigi/) - <contact@sppas.org>, CNRS,
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

