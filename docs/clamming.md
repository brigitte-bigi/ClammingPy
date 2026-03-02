# clamming module

## List of classes

## Class `ClamUtils`

### Description

*Some utilities for ClammingPy.*




### Constructor

#### __init__

```python
def __init__(self):
    """Create a ClamUtils instance."""
    self.markdowner = None
    self.lexer = None
    self.formatter = None
    if len(HTML) == 0:
        self.markdowner = markdown2.Markdown()
        self.formatter = pygments_formatter.HtmlFormatter(**ClamUtils.HTML_FORMATTER_ARGS)
        self.lexer = pygments_lexers.PythonLexer()
```

*Create a ClamUtils instance.*



### Public functions

#### get_class

```python
@staticmethod
def get_class(class_name: str, module_name: str | None=None) -> Any:
    """Return a class object by its name, regardless of import context.

        This method searches for a class within a module, whether the module
        has been imported from a package, from a local test, or executed as
        a script. It first checks already-loaded modules (``sys.modules``),
        then attempts a safe import using ``importlib``.

        This approach ensures stability both for installed packages
        (e.g., ``clamming``) and for local tests (e.g., ``tests.test_clamutils``).

        :param class_name: (str) Name of the class to retrieve.
        :param module_name: (str|None) Name of the module where to look for the class.
                            If None, defaults to the caller’s module.
        :return: (class|None) Class object if found, otherwise None.
        """
    if module_name is None:
        frame = inspect.currentframe()
        caller = frame.f_back if frame else None
        module_name = caller.f_globals.get('__name__', '__main__') if caller else '__main__'
    module = None
    if module_name in sys.modules:
        module = sys.modules[module_name]
    else:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            main_module = sys.modules.get('__main__')
            spec = getattr(main_module, '__spec__', None)
            if spec is not None and hasattr(spec, 'name'):
                alt_name = getattr(spec, 'name')
                module = sys.modules.get(alt_name, None)
            if module is None:
                logging.warning('get_class(): module not found: %s', module_name)
                return None
    class_inst = getattr(module, class_name, None)
    if class_inst is None:
        logging.debug('get_class(): class not found: %s in %s', class_name, module_name)
        return None
    if not inspect.isclass(class_inst):
        logging.debug('get_class(): "%s" found in %s but is not a class.', class_name, module_name)
        return None
    return class_inst
```

*Return a class object by its name, regardless of import context.*

This method searches for a class within a module, whether the module
has been imported from a package, from a local test, or executed as
a script. It first checks already-loaded modules (``sys.modules``),
then attempts a safe import using ``importlib``.

This approach ensures stability both for installed packages
(e.g., ``clamming``) and for local tests (e.g., ``tests.test_clamutils``).

##### Parameters

- **class_name**: (*str*) Name of the class to retrieve.
- **module_name**: (*str*|None) Name of the module where to look for the class. If None, defaults to the caller’s module.


##### Returns

- (class|None) Class object if found, otherwise None.

#### markdown_convert

```python
def markdown_convert(self, md):
    """Return HTML of the given markdown content.

        :param md: (str) A standard-limited markdown content
        :return: (str) The HTML content

        """
    if len(HTML) > 0:
        logging.warning(f'Markdown to HTML conversion is disabled: {HTML}')
        return ''
    return self.markdowner.convert(md)
```

*Return HTML of the given markdown content.*

##### Parameters

- **md**: (*str*) A standard-limited markdown content


##### Returns

- (*str*) The HTML content

#### markdown_to_html

```python
def markdown_to_html(self, content):
    """Turn a markdown content into HTML.

        :param content: (str) A complex markdown content
        :return: (str) The HTML content

        """
    if len(HTML) > 0:
        logging.warning(f'Markdown to HTML conversion is disabled: {HTML}')
        return ''
    h = list()
    code = list()
    md = list()
    i = 0
    all_lines = content.split('\n')
    while i < len(all_lines):
        line = all_lines[i]
        if line.strip().startswith('```') is True:
            has_language = len(line.strip()) == 3
            if len(md) > 0:
                h.append(self.markdowner.convert('\n'.join(md)))
                md = list()
            line = ''
            while line.strip().startswith('```') is False:
                code.append(line)
                i = i + 1
                if i >= len(all_lines):
                    break
                line = all_lines[i]
            if len(code) > 0:
                if has_language is True:
                    h.append('<pre>')
                    h.append('\n'.join(code))
                    h.append('</pre>')
                else:
                    h.append(pygments_highlight('\n'.join(code), self.lexer, self.formatter))
                code = list()
        else:
            idx = self.__is_code(line)
            if idx != -1:
                if len(md) > 0:
                    h.append(self.markdowner.convert('\n'.join(md)))
                    md = list()
                if idx > 0:
                    code.append(line[idx:])
                else:
                    code.append(line)
            else:
                if len(code) > 0:
                    h.append(pygments_highlight('\n'.join(code), self.lexer, self.formatter))
                    code = list()
                md.append(line)
        i = i + 1
    if len(code) > 0:
        h.append(pygments_highlight('\n'.join(code), self.lexer, self.formatter))
    if len(md) > 0:
        h.append(self.markdowner.convert('\n'.join(md)))
    html_result = '\n'.join(h)
    return html_result.replace('<p></p>', '')
```

*Turn a markdown content into HTML.*

##### Parameters

- **content**: (*str*) A complex markdown content


##### Returns

- (*str*) The HTML content

#### source_to_html

```python
def source_to_html(self, source):
    """Turn a source code content into HTML.

        :param source: (str) The source code content
        :return: (str) The HTML content

        """
    if len(HTML) > 0:
        logging.warning('Source code to HTML conversion is disabled: {:s}'.format(HTML))
        return ''
    return pygments_highlight(source, self.lexer, self.formatter)
```

*Turn a source code content into HTML.*

##### Parameters

- **source**: (*str*) The source code content


##### Returns

- (*str*) The HTML content



### Protected functions

#### __is_code

```python
@staticmethod
def __is_code(line):
    entry = line.strip()
    if entry.startswith('>>>') is True:
        return line.index('>') - 1
    if entry.startswith('> ') is True:
        return line.index('>') - 1
    return -1
```





## Class `ClamInfo`

### Description

*The information extracted for a function in the documented class.*

Public members are:

- name (str): required, the name of the function
- args (list of str): optional, the arguments of the function
- source (str): optional, the source code of the function, including its definition
- docstring (str or None): optional, the docstring of the function

##### Example

    >>> clam_info = ClamInfo("add", args=tuple("a", "b"), source="def add(a, b): return a+b", docstring="Add two args.")
    >>> clam_info.name
    > add
    >>> clam_info.args
    > ["a", "b"]
    >>> clam_info.source
    > "def add(a, b): return a+b"
    >>> clam_info.docstring
    > "Add two args."
    >>> clam_info = ClamInfo("add", args=tuple("a", "b"), source="def add(a, b): return a+b")
    >>> clam_info.docstring
    > None

##### Raises

- *TypeError*: if a given argument is not of the expected type.


### Constructor

#### __init__

```python
def __init__(self, name: str, args: list[str] | tuple[str]=(), source: str='', docstring: str | None=None):
    """Create a data class for a documented function.

    :param name: (str) Name of the documented function
    :param args: (list|tuple) List of its arguments
    :param source: (str) Source code of the function
    :param docstring: (str) Docstring of the function
    :raises: TypeError: Wrong type of one of the given parameters

    """
    self.__name = ''
    self.__args = list()
    self.__source = ''
    self.__docstring = None
    self.set_name(name)
    self.set_args(args)
    self.set_source(source)
    self.set_docstring(docstring)
```

*Create a data class for a documented function.*

##### Parameters

- **name**: (*str*) Name of the documented function
- **args**: (*list*|*tuple*) List of its arguments
- **source**: (*str*) Source code of the function
- **docstring**: (*str*) Docstring of the function


##### Raises

- *TypeError*: Wrong type of one of the given parameters



### Public functions

#### get_name

```python
def get_name(self) -> str:
    """Return the name of the stored class."""
    return self.__name
```

*Return the name of the stored class.*

#### set_name

```python
def set_name(self, name: str) -> NoReturn:
    """Set a new name.

        :param name: (str) New name of the documented function/class/...
        :raises: TypeError: given class_name is not a string

        """
    if isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the ClamInfo.name, got {:s} instead.".format(str(type(name))))
    self.__name = name
```

*Set a new name.*

##### Parameters

- **name**: (*str*) New name of the documented function/class/...


##### Raises

- *TypeError*: given class_name is not a string

#### get_args

```python
def get_args(self) -> list:
    """Return a copy of the list of arguments."""
    return [i for i in self.__args]
```

*Return a copy of the list of arguments.*

#### set_args

```python
def set_args(self, args: list[str] | tuple[str]) -> NoReturn:
    """Set the list of args.

        :param args: (list|tuple) Source code
        :raises: TypeError: The given args is not a list or tuple

        """
    if isinstance(args, (list, tuple)) is False:
        raise TypeError("Expected a 'list' or 'tuple' for the ClamInfo.args. Got {:s} instead.".format(str(type(args))))
    self.__args = args
```

*Set the list of args.*

##### Parameters

- **args**: (*list*|*tuple*) Source code


##### Raises

- *TypeError*: The given args is not a list or tuple

#### get_source

```python
def get_source(self) -> str:
    """Return the source code."""
    return self.__source
```

*Return the source code.*

#### set_source

```python
def set_source(self, source: str) -> NoReturn:
    """Set a new source code.

        :param source: (str) Source code
        :raises: TypeError: The given source code is not a string

        """
    if isinstance(source, str) is False:
        raise TypeError("Expected a 'str' for the ClamInfo.source, got {:s} instead.".format(str(type(source))))
    self.__source = source
```

*Set a new source code.*

##### Parameters

- **source**: (*str*) Source code


##### Raises

- *TypeError*: The given source code is not a string

#### get_docstring

```python
def get_docstring(self) -> str:
    """Return the docstring of the class."""
    return self.__docstring
```

*Return the docstring of the class.*

#### set_docstring

```python
def set_docstring(self, docstring: str) -> NoReturn:
    """Set a new docstring to the class."""
    if docstring is not None:
        if isinstance(docstring, str) is False:
            raise TypeError("Expected a 'str' for the ClamInfo.docstring. Got {:s} instead.".format(str(type(docstring))))
    self.__docstring = docstring
```

*Set a new docstring to the class.*



## Class `ClamInfoMarkdown`

### Description

*Convert and store ClamInfo data into Markdown format.*

Docstrings are analyzed with **flexibility rather than completeness...
it's the choice here.**

> Both ReST and Epydoc field styles are supported. :field: or @field: can be used indifferently, with upper- or lower- cases.

Two very useful non-standard field list are added:
`:example:` and `:code:`

Finally, some variants in field names are supported:

- :return: or :returns: are both interpreted the same way;
- :raise: or :raises: or :catch: or :except: are all interpreted the same way.


### Constructor

#### __init__

```python
def __init__(self, clam: ClamInfo):
    """Create a ClamInfoMarkdown converter.

    :param clam: (ClamInfo)
    :raises: TypeError: The given argument is not a ClamInfo.

    """
    if isinstance(clam, ClamInfo) is False:
        raise TypeError("Expected a 'ClamInfo' for the ClamInfoMarkdown.clam, got {:s} instead.".format(str(type(clam))))
    self.__clam = clam
```

*Create a ClamInfoMarkdown converter.*

##### Parameters

- **clam**: (ClamInfo)


##### Raises

- *TypeError*: The given argument is not a ClamInfo.



### Public functions

#### name

```python
@property
def name(self) -> str:
    """Return the name into Markdown format."""
    return self.convert_name(self.__clam.name)
```

*Return the name into Markdown format.*

#### args

```python
@property
def args(self) -> list:
    """Return the list of arguments."""
    return self.__clam.args
```

*Return the list of arguments.*

#### source

```python
@property
def source(self) -> str:
    """Return the source code in Markdown format."""
    return self.convert_source(self.__clam.source)
```

*Return the source code in Markdown format.*

#### docstring

```python
@property
def docstring(self) -> str:
    """Return the docstring in Markdown format."""
    return self.convert_docstring(self.__clam.docstring)
```

*Return the docstring in Markdown format.*

#### convert_name

```python
@staticmethod
def convert_name(name: str) -> str:
    """Convert the given name into markdown.

        :param name: (str) Name of a function or class
        :return: (str) The name in Markdown

        """
    return '#### {:s}'.format(str(name))
```

*Convert the given name into markdown.*

##### Parameters

- **name**: (*str*) Name of a function or class


##### Returns

- (*str*) The name in Markdown

#### convert_source

```python
@staticmethod
def convert_source(source: str) -> str:
    """Convert source code into markdown.

        :param source: (str) Source code of a function or class or anything
        :return: (str) The source in Markdown

        """
    source = str(source)
    if len(source) == 0:
        return ''
    code = list()
    code.append('\n```python')
    code.append(source)
    code.append('```\n')
    return '\n'.join(code)
```

*Convert source code into markdown.*

##### Parameters

- **source**: (*str*) Source code of a function or class or anything


##### Returns

- (*str*) The source in Markdown

#### convert_docstring

```python
@staticmethod
def convert_docstring(docstring: str) -> str:
    """Convert reStructuredText of a docstring to Markdown.

        :param docstring: (str) The docstring of any source code.
        :return: (str) Docstring in Markdown.

        """
    if docstring is None:
        return ''
    md = list()
    is_field_section = ''
    for i, line in enumerate(docstring.split('\n')):
        text = line.strip()
        if len(text) == 0:
            is_field_section = ''
        if i == 0 and text.endswith('.'):
            md.append('*{:s}*'.format(text))
        elif text.startswith(':') or text.startswith('@'):
            fieldname, text = ClamInfoMarkdown._extract_fieldname(text)
            if fieldname is not None:
                if is_field_section != fieldname:
                    if len(is_field_section) > 0:
                        md.append('\n')
                    md.append(ClamInfoMarkdown.MARKDOWN_SECTION[fieldname])
                is_field_section = fieldname
                if len(text) > 0:
                    if fieldname == 'param':
                        md.append(ClamInfoMarkdown._param(text))
                    elif fieldname in ('raise', 'raises'):
                        md.append(ClamInfoMarkdown._raise(text))
                    elif fieldname in ('return', 'returns'):
                        md.append(ClamInfoMarkdown._return(text))
                    elif fieldname == 'example':
                        md.append(ClamInfoMarkdown._example(text))
                    elif fieldname is not None and len(text) > 0:
                        md.append(text)
            elif len(text) > 0:
                md.append(ClamInfoMarkdown._plist(text))
                is_field_section = ''
        elif text.startswith('>>>'):
            if is_field_section != 'example':
                md.append('\n')
                md.append(ClamInfoMarkdown.MARKDOWN_SECTION['example'])
            is_field_section = 'example'
            md.append(ClamInfoMarkdown._example(text))
        elif len(is_field_section) > 0 and len(md) > 0:
            if is_field_section == 'example':
                md.append(ClamInfoMarkdown._example(text))
            else:
                md[-1] = '{:s} {:s}'.format(md[-1], text)
        else:
            md.append(text)
    return '\n'.join(md)
```

*Convert reStructuredText of a docstring to Markdown.*

##### Parameters

- **docstring**: (*str*) The docstring of any source code.


##### Returns

- (*str*) Docstring in Markdown.



### Private functions

#### _extract_fieldname

```python
@staticmethod
def _extract_fieldname(text: str) -> (str, str):
    """Extract a supposed field name from the given text.

         Text field can be of type `@field:` (epydoc) or `:field:` (reST).

         Some examples of supported input text and the returned tuple:

         - "@param name: THE name" returns ("name", "THE name")
         - :param name: THE name" returns ("name", "THE name")
         - ":example:" returns ("example", "")
         - ":return: Something" returns ("return", "Something")
         - "Something here" returns (None, "Something here")

        :param text: (str) Any line of text starting by a field.
        :return: (field_name, description)

        """
    if len(text) == 0:
        return (None, '')
    if text[0] not in ('@', ':'):
        return (None, text)
    try:
        sep_whitespace = text.index(' ')
    except ValueError:
        sep_whitespace = len(text)
    try:
        sep_dots = text[1:].index(':')
    except ValueError:
        sep_dots = len(text)
    pos = min(sep_whitespace, sep_dots)
    if pos < len(text):
        field_name = ClamInfoMarkdown._fieldname_variant(text[1:pos + 1])
        if field_name in ClamInfoMarkdown.IGNORE_FIELDS:
            return (None, '')
        if pos == sep_whitespace:
            content = text[pos + 1:].strip()
        else:
            content = text[pos + 2:].strip()
        if field_name in ClamInfoMarkdown.MARKDOWN_SECTION.keys():
            return (field_name, content)
    return (None, text)
```

*Extract a supposed field name from the given text.*

Text field can be of type `@field:` (epydoc) or `:field:` (reST).

Some examples of supported input text and the returned tuple:

- "@param name: THE name" returns ("name", "THE name")
- :param name: THE name" returns ("name", "THE name")
- ":example:" returns ("example", "")
- ":return: Something" returns ("return", "Something")
- "Something here" returns (None, "Something here")

##### Parameters

- **text**: (*str*) Any line of text starting by a field.


##### Returns

- (field_name, description)

#### _fieldname_variant

```python
@staticmethod
def _fieldname_variant(name: str) -> str:
    """Return the corresponding normalized field.

        Some examples of supported input text and the returned string:

        - "return" returns "return"
        - "Returns" returns "return"
        - "ANYTHING returns "anything"

        :param name: (str) A supposed field-name or one of the variants
        :return: (str) normalized field

        """
    name = name.lower().strip()
    if name in ClamInfoMarkdown.VARIANT_FIELDS:
        return ClamInfoMarkdown.VARIANT_FIELDS[name]
    return name
```

*Return the corresponding normalized field.*

Some examples of supported input text and the returned string:

- "return" returns "return"
- "Returns" returns "return"
- "ANYTHING returns "anything"

##### Parameters

- **name**: (*str*) A supposed field-name or one of the variants


##### Returns

- (*str*) normalized field

#### _ptype

```python
@staticmethod
def _ptype(text: str) -> str:
    """Surround an indicated python type with *".

        Some examples of supported input text and the returned string:

        - "(str)" returns "(*str*)"
        - "(str,int)" returns "(*str*,*int*)"
        - "list(str)" returns "list(*str*)"
        - "(list[str])" returns "(*list*[*str*])"
        - "(any)" returns "(any)"
        - "some text" returns "some text"
        - " (some text) " returns "(some text)"

        :param text: (str) Text to be analyzed to emphasize python types
        :return: (str) analyzed text

        """
    text = text.strip()
    if '(' in text and ')' in text:
        b = text.index('(')
        e = text.index(')')
        if e > b:
            parenthesis = text[b:e].strip()
            for py_type in ClamInfoMarkdown.PY_TYPES:
                if py_type in parenthesis:
                    parenthesis = parenthesis.replace(py_type, '*{:s}*'.format(py_type))
            return '{:s}{:s}{:s}'.format(text[:b].strip(), parenthesis.strip(), text[e:].strip())
    return text
```

*Surround an indicated python type with *".*

Some examples of supported input text and the returned string:

- "(str)" returns "(*str*)"
- "(str,int)" returns "(*str*,*int*)"
- "list(str)" returns "list(*str*)"
- "(list[str])" returns "(*list*[*str*])"
- "(any)" returns "(any)"
- "some text" returns "some text"
- " (some text) " returns "(some text)"

##### Parameters

- **text**: (*str*) Text to be analyzed to emphasize python types


##### Returns

- (*str*) analyzed text

#### _param

```python
@staticmethod
def _param(text: str) -> str:
    """Make param text a list item and surround the param name with '**'.

         Some examples of supported input text and the returned string:

         - "name: THE name" returns "- **name**: THE name"
         - "name: (str) THE name" returns "- **name**: (*str*) THE name"
         - "name: (str|int) THE name" returns "- **name**: (*str*|*int*) THE name"
         - "THE name" returns "THE name"

        :param text: (str) Any line of text that started by a param field.
        :return: analyzed text with surrounded field

        """
    text = text.strip()
    if len(text) == 0:
        return ''
    if ':' in text:
        sep_dots = text.index(':')
        param_name = text[:sep_dots].strip()
        param_descr = text[sep_dots + 1:].strip()
        if len(param_descr) > 0:
            return '- **{:s}**: {:s}'.format(param_name, ClamInfoMarkdown._ptype(param_descr))
        else:
            return '- **{:s}**'.format(param_name)
    return ClamInfoMarkdown._ptype(text)
```

*Make param text a list item and surround the param name with '**'.*

Some examples of supported input text and the returned string:

- "name: THE name" returns "- **name**: THE name"
- "name: (str) THE name" returns "- **name**: (*str*) THE name"
- "name: (str|int) THE name" returns "- **name**: (*str*|*int*) THE name"
- "THE name" returns "THE name"

##### Parameters

- **text**: (*str*) Any line of text that started by a param field.


##### Returns

- analyzed text with surrounded field

#### _raise

```python
@staticmethod
def _raise(text: str) -> str:
    """Make raise text a list item.

        Some examples of supported input text and the returned string:

         - "THE error" returns "- THE error"
         - "ValueError: THE problem" returns "- **ValueError**: THE problem"

        :param text: (str) Any line of text that started by a raise field.
        :return: analyzed text with surrounded exception name

        """
    text = text.strip()
    if len(text) == 0:
        return ''
    if ':' in text:
        sep_dots = text.index(':')
        raise_tag = text[:sep_dots].strip()
        raise_descr = text[sep_dots + 1:].strip()
        if len(raise_descr) > 0:
            return '- *{:s}*: {:s}'.format(raise_tag, raise_descr)
        else:
            return '- *{:s}*'.format(raise_tag)
    return text
```

*Make raise text a list item.*

Some examples of supported input text and the returned string:

- "THE error" returns "- THE error"
- "ValueError: THE problem" returns "- **ValueError**: THE problem"

##### Parameters

- **text**: (*str*) Any line of text that started by a raise field.


##### Returns

- analyzed text with surrounded exception name

#### _return

```python
@staticmethod
def _return(text: str) -> str:
    """Make return text a list item.

        Some examples of supported input text and the returned string:

         - "THE name" returns "- THE name"
         - "(str|int) THE name" returns "- (*str*|*int*) THE name"
         - "tag: THE name" returns "- **tag**: THE name"
         - "tag:" returns "- **tag**"

        :param text: (str) Any line of text that started by a return field.
        :return: analyzed text with surrounded tag

        """
    text = text.strip()
    if len(text) == 0:
        return ''
    if ':' in text:
        sep_dots = text.index(':')
        return_tag = text[:sep_dots].strip()
        return_descr = text[sep_dots + 1:].strip()
        if len(return_descr) > 0:
            return '- **{:s}**: {:s}'.format(return_tag, ClamInfoMarkdown._ptype(return_descr))
        else:
            return '- **{:s}**'.format(return_tag)
    return '- {:s}'.format(ClamInfoMarkdown._ptype(text))
```

*Make return text a list item.*

Some examples of supported input text and the returned string:

- "THE name" returns "- THE name"
- "(str|int) THE name" returns "- (*str*|*int*) THE name"
- "tag: THE name" returns "- **tag**: THE name"
- "tag:" returns "- **tag**"

##### Parameters

- **text**: (*str*) Any line of text that started by a return field.


##### Returns

- analyzed text with surrounded tag

#### _example

```python
@staticmethod
def _example(text: str) -> str:
    """Make example text a >>> item.

        Some examples of supported input text and the returned string:

         - ">>>print('Hello')" returns "    >>> print('Hello')"
         - "print('Hello')" returns "    >>> print('Hello')"

        :param text: (str) Any line of code in an example section.
        :return: analyzed text with ">>>" pre-pended

        """
    text = text.strip()
    if text.startswith('>>>'):
        code = text[3:].strip()
        return '    >>> {:s}'.format(code)
    else:
        return '    > {:s}'.format(text)
```

*Make example text a >>> item.*

Some examples of supported input text and the returned string:

- ">>>print('Hello')" returns "    >>> print('Hello')"
- "print('Hello')" returns "    >>> print('Hello')"

##### Parameters

- **text**: (*str*) Any line of code in an example section.


##### Returns

- analyzed text with ">>>" pre-pended

#### _plist

```python
@staticmethod
def _plist(text: str) -> str:
    """Turn an indicated field list into a list item.

        Some examples of supported input text and the returned string:

         - ":Author: someone" returns "- **Author**: someone"
         - ":Author: " returns "- **Author**"
         - "Author: no " returns "Author: no"

        :param text: (str) Any line of text that started by any field.
        :return: analyzed text with surrounded field

        """
    text = str(text)
    text = text.strip()
    if len(text) < 3:
        return text
    if text.startswith(':') and ':' in text[1:]:
        e = text[1:].index(':') + 1
        item = text[1:e].strip()
        descr = text[e + 1:].strip()
        if len(descr) > 0:
            return '- **{:s}**: {:s}'.format(item, descr)
        else:
            return '- **{:s}**'.format(item)
    else:
        return text
```

*Turn an indicated field list into a list item.*

Some examples of supported input text and the returned string:

- ":Author: someone" returns "- **Author**: someone"
- ":Author: " returns "- **Author**"
- "Author: no " returns "Author: no"

##### Parameters

- **text**: (*str*) Any line of text that started by any field.


##### Returns

- analyzed text with surrounded field



### Overloads

#### __str__

```python
def __str__(self):
    return '{:s}\n{:s}\n{:s}\n'.format(self.name, self.source, self.docstring)
```





## Class `ClammingClassParser`

### Description

*Inspect a python class and store relevant information for further doc.*




### Constructor

#### __init__

```python
def __init__(self, obj: Any):
    """Create lists of ClamInfo from a given Python object.

    List of public members:

    - obj_clams (ClamInfo): describes the object. It has a name and a docstring.
    - init_clams (ClamInfo): describes the constructor of the object, if the object does.
    - fct_clams (list of ClamInfo): describes all the functions of the object.

    :param obj: Any class object; its source code must be available.
    :raises TypeError: if the object is not a class.
    :raises TypeError: if the object is a built-in class.

    """
    if isinstance(obj, object) is False:
        raise TypeError('Expected a class object for clamming.')
    try:
        self.__obj_src = textwrap.dedent(inspect.getsource(obj))
        self.__obj = obj
    except TypeError:
        raise TypeError('Expected a class object for clamming but not a built-in one.')
    self.__obj_clams = self._inspect_class()
    self.__init_clams = self._inspect_constructor()
    self.__fct_clams = self._inspect_functions()
```

*Create lists of ClamInfo from a given Python object.*

List of public members:

- obj_clams (ClamInfo): describes the object. It has a name and a docstring.
- init_clams (ClamInfo): describes the constructor of the object, if the object does.
- fct_clams (list of ClamInfo): describes all the functions of the object.

##### Parameters

- **obj**: Any class object; its source code must be available.


##### Raises

- *TypeError*: if the object is not a class.
- *TypeError*: if the object is a built-in class.



### Public functions

#### get_obj_clams

```python
def get_obj_clams(self) -> ClamInfo:
    """Parse the information of the class.

        :return: (ClamInfo) Information of the object.

        """
    return self.__obj_clams
```

*Parse the information of the class.*

##### Returns

- (ClamInfo) Information of the object.

#### get_init_clams

```python
def get_init_clams(self) -> ClamInfo:
    """Inspect constructor of the given object.

        :return: (ClamInfo) Information of the constructor of the object.

        """
    return self.__init_clams
```

*Inspect constructor of the given object.*

##### Returns

- (ClamInfo) Information of the constructor of the object.

#### get_fct_clams

```python
def get_fct_clams(self) -> dict:
    """Inspect functions of the given object.

        :return: (dict) key=function name, value=ClamInfo()

        """
    return self.__fct_clams
```

*Inspect functions of the given object.*

##### Returns

- (*dict*) key=function name, value=ClamInfo()



### Private functions

#### _inspect_class

```python
def _inspect_class(self) -> ClamInfo:
    """Inspect constructor of the given object.

        """
    class_name = self.__obj.__name__
    tree = ast.parse(self.__obj_src)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            return ClamInfo(class_name, [], '', ast.get_docstring(node))
    return ClamInfo(class_name, [], '', None)
```

*Inspect constructor of the given object.*



#### _inspect_constructor

```python
def _inspect_constructor(self) -> ClamInfo:
    """Inspect constructor of the given object."""
    try:
        init_src = textwrap.dedent(inspect.getsource(self.__obj.__init__))
    except OSError:
        return ClamInfo('')
    except TypeError:
        return ClamInfo('')
    init_tree = ast.parse(textwrap.dedent(init_src))
    init_args = list()
    init_src = ''
    init_doc = None
    for node in ast.walk(init_tree):
        if isinstance(node, ast.FunctionDef):
            init_args = [arg.arg for arg in node.args.args]
            init_src = ast.unparse(node)
            init_doc = ast.get_docstring(node)
            break
    return ClamInfo(node.name, init_args, init_src, init_doc)
```

*Inspect constructor of the given object.*

#### _inspect_functions

```python
def _inspect_functions(self) -> dict:
    """Inspect the documented functions of the given object.

        :return: (dict) key=function name, value=ClamInfo()

        """
    fct_infos = dict()
    tree = ast.parse(self.__obj_src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
            if name in ('__init__', '__new__'):
                continue
            fct_infos[name] = ClamInfo(name, [arg.arg for arg in node.args.args], ast.unparse(node), ast.get_docstring(node))
    return fct_infos
```

*Inspect the documented functions of the given object.*

##### Returns

- (*dict*) key=function name, value=ClamInfo()



## Class `ClamsClass`

### Description

*Convert a parsed class object into Markdown or HTML content.*

##### Example

    >>> clamming = ClammingClassParser(Vehicle)
    >>> clams = ClamsClass(clamming)
    >>> md = clams.markdown()


### Constructor

#### __init__

```python
def __init__(self, parsed_obj: ClammingClassParser):
    """Create documentation from the given parsed class object.

    HTML conversion depends on external libraries. It could be disabled
    if any of them is missing. If not, customizing the HTML export can
    be done by assigning different values to members or by changing their
    optional parameters.

    See `Pygments` documentation:
    [HtmlFormatter](https://pygments.org/docs/formatters/#HtmlFormatter)
    and
    [Lexer](https://pygments.org/docs/lexers/#pygments.lexers.python.PythonLexer)

    :example:
    >>> self.markdowner = markdown2.Markdown()
    >>> self.formatter = pygments_formatter.HtmlFormatter(**ClamsClass.HTML_FORMATTER_ARGS)
    >>> self.lexer = pygments_lexers.PythonLexer()

    :param parsed_obj: A parsed object.

    """
    self.__utils = ClamUtils()
    self.__info_class_name = parsed_obj.get_obj_clams().name
    self.__info_class_description = parsed_obj.get_obj_clams()
    self.__info_short_description = self.__info_class_name + '. '
    if self.__info_class_description.docstring is not None:
        lines = self.__info_class_description.docstring.split('\n')
        self.__info_short_description += lines[0]
    self.__info_constructor = parsed_obj.init_clams
    self.__info_public_fcts = list()
    for fct_name in parsed_obj.fct_clams:
        if fct_name.startswith('_') is False:
            self.__info_public_fcts.append(parsed_obj.fct_clams[fct_name])
    self.__info_private_fcts = list()
    for fct_name in parsed_obj.fct_clams:
        if fct_name.startswith('_') is True and fct_name.startswith('__') is False:
            self.__info_private_fcts.append(parsed_obj.fct_clams[fct_name])
    self.__info_protected_fcts = list()
    for fct_name in parsed_obj.fct_clams:
        if fct_name.startswith('__') is True and fct_name.endswith('__') is False:
            self.__info_protected_fcts.append(parsed_obj.fct_clams[fct_name])
    self.__info_overloads = list()
    for fct_name in parsed_obj.fct_clams:
        if fct_name.startswith('__') is True and fct_name.endswith('__') is True:
            self.__info_overloads.append(parsed_obj.fct_clams[fct_name])
```

*Create documentation from the given parsed class object.*

HTML conversion depends on external libraries. It could be disabled
if any of them is missing. If not, customizing the HTML export can
be done by assigning different values to members or by changing their
optional parameters.

See `Pygments` documentation:
[HtmlFormatter](https://pygments.org/docs/formatters/#HtmlFormatter)
and
[Lexer](https://pygments.org/docs/lexers/#pygments.lexers.python.PythonLexer)

##### Example

    >>> self.markdowner = markdown2.Markdown()
    >>> self.formatter = pygments_formatter.HtmlFormatter(**ClamsClass.HTML_FORMATTER_ARGS)
    >>> self.lexer = pygments_lexers.PythonLexer()

##### Parameters

- **parsed_obj**: A parsed object.



### Public functions

#### get_name

```python
def get_name(self) -> str:
    """Return the name of the documented class."""
    return self.__info_class_name
```

*Return the name of the documented class.*

#### get_short_description

```python
def get_short_description(self) -> str:
    """Return the 160 chars max description of the documented class."""
    return self.__info_short_description
```

*Return the 160 chars max description of the documented class.*

#### markdown

```python
def markdown(self) -> str:
    """Get Markdown content of the parsed object.

        :return: (str) Content in Markdown format

        """
    md = list()
    md.append('## Class `{:s}`\n'.format(self.__info_class_name))
    if self.__info_class_description.docstring is not None:
        md.append('### Description\n')
        md.append(ClamInfoMarkdown.convert_docstring(self.__info_class_description.docstring))
        md.append('\n')
    if len(self.__info_constructor.name) > 0:
        md.append('### Constructor\n')
        md.append(str(ClamInfoMarkdown(self.__info_constructor)))
        md.append('\n')
    if len(self.__info_public_fcts) > 0:
        md.append('### Public functions\n')
        for info in self.__info_public_fcts:
            md.append(str(ClamInfoMarkdown(info)))
        md.append('\n')
    if len(self.__info_private_fcts) > 0:
        md.append('### Private functions\n')
        for info in self.__info_private_fcts:
            md.append(str(ClamInfoMarkdown(info)))
        md.append('\n')
    if len(self.__info_protected_fcts) > 0:
        md.append('### Protected functions\n')
        for info in self.__info_protected_fcts:
            md.append(str(ClamInfoMarkdown(info)))
        md.append('\n')
    if len(self.__info_overloads) > 0:
        md.append('### Overloads\n')
        for info in self.__info_overloads:
            md.append(str(ClamInfoMarkdown(info)))
        md.append('\n')
    return '\n'.join(md)
```

*Get Markdown content of the parsed object.*

##### Returns

- (*str*) Content in Markdown format

#### html

```python
def html(self) -> str:
    """Get HTML content of the parsed object.

        :return: (str) Content in HTML format
        :raises: ImportError: if one of the requirements is not installed

        """
    if self.__utils.markdowner is None:
        logging.warning('Markdown to HTML conversion is disabled.')
        return ''
    hd = list()
    cid = self.__info_class_name
    hd.append('<section id="#{:s}">'.format(cid))
    hd.append('<h2>Class {:s}</h2>\n'.format(self.__info_class_name))
    if self.__info_class_description.docstring is not None:
        hd.append('<section>')
        hd.append('<h3 id="#description_{:s}">Description</h3>'.format(cid))
        _html = self.__docstring_to_html(self.__info_class_description.docstring)
        hd.append(ClamsClass._docstring_article(_html))
        hd.append('</section>')
    if len(self.__info_constructor.name) > 0:
        hd.append('<section>')
        hd.append('<h3 id="#constructor_{:s}">Constructor</h3>'.format(cid))
        _html = self.__claminfo_to_html(self.__info_constructor, with_name=False)
        hd.append(_html)
        hd.append('</section>')
    if len(self.__info_public_fcts) > 0:
        hd.append('<section>')
        hd.append('<h3 id="#public_fct_{:s}">Public functions</h3>'.format(cid))
        for info in self.__info_public_fcts:
            hd.append(self.__claminfo_to_html(info))
        hd.append('</section>')
    if len(self.__info_private_fcts) > 0:
        hd.append('<section>')
        hd.append('<h3 id="#private_fct_{:s}">Private functions</h3>'.format(cid))
        for info in self.__info_private_fcts:
            hd.append(self.__claminfo_to_html(info))
        hd.append('</section>')
    if len(self.__info_protected_fcts) > 0:
        hd.append('<section>')
        hd.append('<h3 id="#protected_fct_{:s}">Protected functions</h3>'.format(cid))
        for info in self.__info_protected_fcts:
            hd.append(self.__claminfo_to_html(info))
        hd.append('</section>')
    if len(self.__info_overloads) > 0:
        hd.append('<section>')
        hd.append('<h3 id="#overloads_{:s}">Overloads</h3>'.format(cid))
        for info in self.__info_overloads:
            hd.append(self.__claminfo_to_html(info))
        hd.append('</section>')
    hd.append('</section>')
    html_result = '\n'.join(hd)
    return html_result.replace('<p></p>', '')
```

*Get HTML content of the parsed object.*

##### Returns

- (*str*) Content in HTML format


##### Raises

- *ImportError*: if one of the requirements is not installed



### Private functions

#### _source_accordion

```python
@staticmethod
def _source_accordion(header_content: str, main_content: str) -> str:
    """Return the given content embedded into a details element.

        :param header_content: (str) Content of the collapsed part
        :param main_content: (str) Content of the expanded part
        :return: (str) HTML-5 of an article

        """
    h = list()
    h.append('    <details>')
    h.append('    <summary>')
    h.append(header_content)
    h.append('    </summary>')
    h.append(main_content)
    h.append('    </details>')
    return '\n'.join(h)
```

*Return the given content embedded into a details element.*

##### Parameters

- **header_content**: (*str*) Content of the collapsed part
- **main_content**: (*str*) Content of the expanded part


##### Returns

- (*str*) HTML-5 of an article

#### _docstring_article

```python
@staticmethod
def _docstring_article(content: str) -> str:
    """Return the given content embedded into an article.

        :param content: Content of the article
        :return: (str) HTML-5 of an article

        """
    h = list()
    h.append('    <article class="docstring">')
    h.append(content)
    h.append('    </article>')
    html_result = '\n'.join(h)
    return html_result.replace('<p></p>', '')
```

*Return the given content embedded into an article.*

##### Parameters

- **content**: Content of the article


##### Returns

- (*str*) HTML-5 of an article



### Protected functions

#### __docstring_to_html

```python
def __docstring_to_html(self, docstring: str) -> str:
    """Return the HTML of the given docstring.

        :param docstring: (str)
        :return: (str) HTML

        """
    _md = ClamInfoMarkdown.convert_docstring(docstring)
    return self.__utils.markdown_to_html(_md)
```

*Return the HTML of the given docstring.*

##### Parameters

- **docstring**: (*str*)


##### Returns

- (*str*) HTML

#### __claminfo_to_html

```python
def __claminfo_to_html(self, claminfo: ClamInfo, with_name=True) -> str:
    """Return the HTML of the given ClamInfo instance.

        :return: (str) HTML

        """
    h = list()
    if with_name is True:
        h.append('<h4>{:s}</h4>\n'.format(claminfo.name))
    params = [p for p in claminfo.args]
    if 'self' in params:
        params.remove('self')
    if claminfo.docstring is not None:
        _html = self.__docstring_to_html(claminfo.docstring)
        if len(params) > 0 and '<h5>Parameters</h5>' not in _html:
            _md = '\n\n##### Parameters\n'
            _md += '\n'.join(['- **{:s}**'.format(p) for p in params])
            _html += self.__utils.markdown_convert(_md)
        h.append(ClamsClass._docstring_article(_html))
        h.append('\n')
    if len(claminfo.source) > 0:
        _html = ClamUtils().source_to_html(claminfo.source)
        h.append(ClamsClass._source_accordion('View Source', _html))
    h.append('\n')
    html_result = '\n'.join(h)
    return html_result.replace('<p></p>', '')
```

*Return the HTML of the given ClamInfo instance.*

##### Returns

- (*str*) HTML



## Class `ClamsPack`

### Description

*Create documentation of a module into Markdown or HTML.*

##### Example

    >>> clams = ClamsPack(clamming)
    >>> md = clams.markdown()


### Constructor

#### __init__

```python
def __init__(self, pack: Any):
    """Create documentation from the given package name.

    :param pack: (module) A Python module
    :raises: TypeError: given 'pack' is not a module

    """
    if inspect.ismodule(pack) is False:
        raise TypeError('Expected a Python module. Got {:s} instead.'.format(str(pack)))
    self.__pack = pack
    self.__clams = list()
    try:
        for class_name in pack.__all__:
            class_inst = ClamUtils.get_class(class_name, self.__pack.__name__)
            if class_inst is not None:
                clammer = ClammingClassParser(class_inst)
                self.__clams.append(ClamsClass(clammer))
    except AttributeError:
        logging.warning('Attribute __all__ is missing in package {:s} => No auto documentation.'.format(self.__pack.__name__))
```

*Create documentation from the given package name.*

##### Parameters

- **pack**: (module) A Python module


##### Raises

- *TypeError*: given 'pack' is not a module



### Public functions

#### get_name

```python
def get_name(self) -> str:
    """Return the name of the package."""
    return self.__pack.__name__
```

*Return the name of the package.*

#### get_readme

```python
def get_readme(self) -> str:
    """Return the content of the README file of the package, if any."""
    path_to_readme = os.path.dirname(self.__pack.__file__)
    readme_content = ''
    for f in os.listdir(path_to_readme):
        if 'readme' in f.lower():
            readme_file = os.path.join(path_to_readme, f)
            try:
                with open(readme_file, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
            except Exception as e:
                logging.warning('A README file was found but could not be read: {:s}'.format(str(e)))
            break
    return readme_content
```

*Return the content of the README file of the package, if any.*

#### markdown

```python
def markdown(self, exporter: ExportOptions | None=None) -> str:
    """Return the documentation of the package as a standalone Markdown content.

        """
    md = list()
    md.append('# {:s} module\n'.format(self.name))
    if exporter is not None:
        if exporter.readme is True and len(HTML) == 0:
            readme_content = self.get_readme()
            if len(readme_content) > 0:
                md.append(readme_content)
    md.append('## List of classes\n')
    for clams in self.__clams:
        md.append(clams.markdown())
    md.append('\n\n~ Created using [Clamming](https://clamming.sf.net) version {:s} ~\n'.format(clamming.__version__))
    return '\n'.join(md)
```

*Return the documentation of the package as a standalone Markdown content.*



#### html

```python
def html(self, exporter: ExportOptions | None=None) -> str:
    """Return the documentation of the package as an HTML content."""
    html = list()
    html.append('<h1>{:s} module</h1>\n'.format(self.name))
    if exporter is not None:
        if exporter.readme is True and len(HTML) == 0:
            readme_content = self.get_readme()
            if len(readme_content) > 0:
                html.append('    <section id="readme">\n')
                html.append(ClamUtils().markdown_to_html(readme_content))
                html.append('    </section>\n')
    html.append('<h2>List of classes</h2>\n')
    for clams in self.__clams:
        html.append(clams.html())
    html.append('\n\n<p>~ Created using <a href="https://clamming.sf.net">ClammingPy</a> version {:s} ~</p>\n'.format(clamming.__version__))
    return '\n'.join(html)
```

*Return the documentation of the package as an HTML content.*

#### html_index

```python
def html_index(self, path_name: str | None=None, exporter: ExportOptions | None=None) -> str:
    """Create the HTML content of an index for the package.

        :param path_name: (str) Path where the exported HTML files are, or None for a standalone content.
        :param exporter: (HTMLDocExport) Options for HTML output files
        :return: (str) HTML code

        """
    out = list()
    out.append('    <section id="#{:s}">'.format(self.name))
    out.append('    <h1>{:s} module</h1>'.format(self.name))
    if exporter is not None:
        if exporter.readme is True and len(HTML) == 0:
            readme_content = self.get_readme()
            if len(readme_content) > 0:
                out.append('    <section id="readme">\n')
                out.append(ClamUtils().markdown_to_html(readme_content))
                out.append('    </section>\n')
    out.append('<h2>List of classes</h2>\n')
    out.append('        <section class="cards-panel">')
    for i in range(len(self.__clams)):
        clams = self.__clams[i]
        out.append('        <article class="card">')
        out.append('            <header><span>{:d}</span></header>'.format(i + 1))
        out.append('            <main>')
        out.append('                <h3>{:s}</h3>'.format(clams.name))
        out.append('            </main>')
        out.append('            <footer>')
        if path_name is not None:
            out.append('                <a role="button" href="{:s}">Read me →</a>'.format(os.path.join(path_name, clams.name + '.html')))
        else:
            out.append('                <a role="button" href="#{:s}">Read me →</a>'.format(clams.name))
        out.append('            </footer>')
        out.append('        </article>')
    out.append('        </section>')
    out.append('    </section>')
    return '\n'.join(out)
```

*Create the HTML content of an index for the package.*

##### Parameters

- **path_name**: (*str*) Path where the exported HTML files are, or None for a standalone content.
- **exporter**: (HTMLDocExport) Options for HTML output files


##### Returns

- (*str*) HTML code

#### html_export_clams

```python
def html_export_clams(self, path_name: str, exporter: ExportOptions) -> list[str]:
    """Create the HTML pages of all classes of the package.

        :param path_name: (str) Path where to add the exported HTML files
        :param exporter: (HTMLDocExport) Options for HTML output files
        :return: (list) Exported file names

        """
    out = list()
    if os.path.exists(path_name) is False:
        os.mkdir(path_name)
    logging.info('Export module index')
    out_html = os.path.join(path_name, self.name + '.html')
    self.__module_index(out_html, exporter)
    out.append(out_html)
    for i in range(len(self.__clams)):
        clams = self.__clams[i]
        out_html = os.path.join(path_name, clams.name + '.html')
        logging.info('Export {:s}'.format(out_html))
        exporter.prev_class = None if i == 0 else self.__clams[i - 1].name + '.html'
        exporter.next_class = None if i + 1 == len(self.__clams) else self.__clams[i + 1].name + '.html'
        exporter.description = clams.get_short_description()
        html_content = clams.html()
        self.__module_class(out_html, exporter, html_content)
    return out
```

*Create the HTML pages of all classes of the package.*

##### Parameters

- **path_name**: (*str*) Path where to add the exported HTML files
- **exporter**: (HTMLDocExport) Options for HTML output files


##### Returns

- (*list*) Exported file names



### Protected functions

#### __module_index

```python
def __module_index(self, out_html, exporter):
    """Export an index for the module.

        """
    with codecs.open(out_html, 'w', 'utf-8') as fp:
        fp.write('<!DOCTYPE html>\n')
        fp.write('<html>\n')
        fp.write(exporter.get_head())
        fp.write('<body class="{:s}">\n'.format(exporter.get_theme()))
        fp.write('    {:s}\n'.format(exporter.get_header()))
        fp.write('    {:s}\n'.format(exporter.get_nav()))
        fp.write('    <main id="main-content">\n')
        fp.write(self.html_index(path_name='', exporter=exporter))
        fp.write('    </main>\n')
        fp.write('    {:s}\n'.format(exporter.get_footer()))
        fp.write('</body>\n')
        fp.write('</html>\n')
```

*Export an index for the module.*



#### __module_class

```python
def __module_class(self, out_html, exporter, content):
    """Export a content for the module.

        """
    with codecs.open(out_html, 'w', 'utf-8') as fp:
        fp.write('<!DOCTYPE html>\n')
        fp.write('<html>\n')
        fp.write(exporter.get_head())
        fp.write('<body class="{:s}">\n'.format(exporter.get_theme()))
        fp.write('    {:s}\n'.format(exporter.get_header()))
        fp.write('    {:s}\n'.format(exporter.get_nav()))
        fp.write('    <main id="main-content">\n')
        fp.write('    <section id="#{:s}">'.format(self.name))
        fp.write('    <h1>Module {:s}</h1>\n'.format(self.name))
        fp.write(content)
        fp.write('    </section>')
        fp.write('    </main>\n')
        fp.write('    {:s}\n'.format(exporter.get_footer()))
        fp.write('</body>\n')
        fp.write('</html>\n')
```

*Export a content for the module.*





### Overloads

#### __len__

```python
def __len__(self):
    """Return the number of documented pages of the package."""
    return len(self.__clams)
```

*Return the number of documented pages of the package.*



## Class `ClamsModules`

### Description

*Create documentation of a list of modules into Markdown or HTML.*

##### Example

    >>> clams = ClamsModules(clamming)
    >>> md = clams.markdown()


### Constructor

#### __init__

```python
def __init__(self, modules: list):
    """Create documentation from the given package name.

    :param modules: list(modules) A list of Python modules
    :raises: TypeError: a given entry is not a module

    """
    if isinstance(modules, list) is False:
        raise TypeError('Expected a list of Python modules. Got {:s} instead.'.format(str(modules)))
    self.__clams_packs = list()
    for m in modules:
        self.__clams_packs.append(ClamsPack(m))
```

*Create documentation from the given package name.*

##### Parameters

- **modules**: list(modules) A list of Python modules


##### Raises

- *TypeError*: a given entry is not a module



### Public functions

#### markdown_export_packages

```python
def markdown_export_packages(self, path_name: str, exporter: ExportOptions) -> list[str]:
    """Create a Markdown file for each of the packages.

        :param path_name: (str) Path where to add the exported md files
        :param exporter: (HTMLDocExport) Options for HTML output files
        :return: (list) Exported file names

        """
    out = list()
    for clams_pack in self.__clams_packs:
        out_md = os.path.join(path_name, clams_pack.name + '.md')
        if os.path.exists(path_name) is False:
            os.mkdir(path_name)
        logging.info('Export {:s}'.format(out_md))
        with codecs.open(out_md, 'w', 'utf-8') as fp:
            fp.write(clams_pack.markdown())
        out.append(out_md)
    return out
```

*Create a Markdown file for each of the packages.*

##### Parameters

- **path_name**: (*str*) Path where to add the exported md files
- **exporter**: (HTMLDocExport) Options for HTML output files


##### Returns

- (*list*) Exported file names

#### html_export_index

```python
def html_export_index(self, path_name: str, exporter: ExportOptions, readme: str | None=None) -> str:
    """Write the index.html file from the list of packages.

        :param path_name: (str) Path where to add the exported index.html file
        :param exporter: (HTMLDocExport) Options for HTML output files
        :param readme: (str) A markdown README filename to be added into the index.html
        :return: (str) Filename of the created HTML index file

        """
    logging.info('Export index.html')
    out = os.path.join(path_name, 'index.html')
    if os.path.exists(path_name) is False:
        os.mkdir(path_name)
    with codecs.open(out, 'w', 'utf-8') as fp:
        fp.write('<!DOCTYPE html>\n')
        fp.write('<html>\n')
        fp.write(exporter.get_head())
        fp.write('<body class="{:s}">\n'.format(exporter.get_theme()))
        fp.write('    {:s}\n'.format(exporter.get_header()))
        fp.write('    {:s}\n'.format(exporter.get_nav()))
        fp.write('    <main id="main-content">\n')
        if readme is not None:
            try:
                with codecs.open(readme, 'r', 'utf-8') as readme_fp:
                    readme_content = readme_fp.read()
                    if len(readme_content) > 0:
                        fp.write('    <section id="readme">\n')
                        fp.write(ClamUtils().markdown_to_html(readme_content))
                        fp.write('    </section>\n')
            except Exception as e:
                logging.error(e)
                traceback.print_exc()
        fp.write('<h1>List of packages:</h1>\n')
        for clams_pack in self.__clams_packs:
            fp.write('      <h2>{:s}</h2>\n'.format(clams_pack.name))
            fp.write("      <p><a href='{:s}'>Get documentation</a></p>\n".format(clams_pack.name + '.html'))
        fp.write('    </main>\n')
        fp.write('    {:s}\n'.format(exporter.get_footer()))
        fp.write('</body>\n')
        fp.write('</html>\n')
    return out
```

*Write the index.html file from the list of packages.*

##### Parameters

- **path_name**: (*str*) Path where to add the exported index.html file
- **exporter**: (HTMLDocExport) Options for HTML output files
- **readme**: (*str*) A markdown README filename to be added into the index.html


##### Returns

- (*str*) Filename of the created HTML index file

#### html_export_packages

```python
def html_export_packages(self, path_name: str, exporter: ExportOptions, readme: str | None=None) -> list:
    """Create all the HTML files from the list of packages.

        - create the HTML file for each class of each given module;
        - create an index.html file.

        :param path_name: (str) Path where to add the exported index.html file
        :param exporter: (HTMLDocExport) Options for HTML output files
        :param readme: (str) A markdown README filename to be added into the index.html
        :return: (list) Exported file names

        """
    out = list()
    out_index = self.html_export_index(path_name, exporter, readme)
    out.append(out_index)
    for i in range(len(self.__clams_packs)):
        clams_pack = self.__clams_packs[i]
        exporter.prev_module = None if i == 0 else self.__clams_packs[i - 1].name + '.html'
        exporter.next_module = None if i + 1 == len(self.__clams_packs) else self.__clams_packs[i + 1].name + '.html'
        out_html = clams_pack.html_export_clams(path_name, exporter)
        out.extend(out_html)
    return out
```

*Create all the HTML files from the list of packages.*

- create the HTML file for each class of each given module;
- create an index.html file.

##### Parameters

- **path_name**: (*str*) Path where to add the exported index.html file
- **exporter**: (HTMLDocExport) Options for HTML output files
- **readme**: (*str*) A markdown README filename to be added into the index.html


##### Returns

- (*list*) Exported file names



## Class `ExportOptions`

### Description

*Store the options and content for an export to documented files.*

ExportOptions is a data class, used to store options and content for
exporting a documented file. It provides methods to set and get various
information such as software name, copyright, icon, title, favicon, and
theme. It also allows setting the names of the next and previous classes
or modules for generating a table of contents (HTML only).

##### Example

    >>> h = ExportOptions()
    >>> h.software = "Clamming"
    >>> h.theme = "light"
    >>> html_head = h.get_head()
    >>> html_nav = h.get_nav()
    >>> html_footer = h.get_footer()


### Constructor

#### __init__

```python
def __init__(self):
    """Create a documentation export system for a ClamsPack.

    Main functionalities:

    - Store options and content for exporting a standalone file;
    - Set and get HTML information such as software name, copyright, icon, title, favicon, and theme;
    - Set the names of the next and previous classes or modules for generating a table of contents.

    """
    self.__readme = True
    self.__software = ExportOptions.DEFAULT_SOFTWARE
    self.__copyright = ExportOptions.DEFAULT_COPYRIGHT
    self.__url = ExportOptions.DEFAULT_URL
    self.__icon = ExportOptions.DEFAULT_ICON
    self.__title = ExportOptions.DEFAULT_TITLE
    self.__favicon = ExportOptions.DEFAULT_FAVICON
    self.__theme = ExportOptions.DEFAULT_THEME
    self.__statics = ExportOptions.DEFAULT_STATICS
    self.__wexa_statics = ExportOptions.DEFAULT_WEXA_STATICS
    self.__descr = 'Python class documentation'
    self.__next_class = None
    self.__prev_class = None
    self.__next_pack = None
    self.__prev_pack = None
```

*Create a documentation export system for a ClamsPack.*

Main functionalities:

- Store options and content for exporting a standalone file;
- Set and get HTML information such as software name, copyright, icon, title, favicon, and theme;
- Set the names of the next and previous classes or modules for generating a table of contents.



### Public functions

#### get_add_readme

```python
def get_add_readme(self) -> bool:
    """Return whether the README of library is added or not."""
    return self.__readme
```

*Return whether the README of library is added or not.*

#### set_add_readme

```python
def set_add_readme(self, readme: bool) -> NoReturn:
    """Set whether the README of library is added or not.

        :param readme: (bool) whether the README is added or not.

        """
    self.__readme = bool(readme)
```

*Set whether the README of library is added or not.*

##### Parameters

- **readme**: (*bool*) whether the README is added or not.

#### get_software

```python
def get_software(self) -> str:
    """Return the name of the software."""
    return self.__software
```

*Return the name of the software.*

#### set_software

```python
def set_software(self, name: str=DEFAULT_SOFTWARE) -> NoReturn:
    """Set a software name.

        :param name: (str) Name of the documented software
        :raises: TypeError: Given name is not a string

        """
    if isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.software. Got {} instead.".format(name))
    self.__software = name
```

*Set a software name.*

##### Parameters

- **name**: (*str*) Name of the documented software


##### Raises

- *TypeError*: Given name is not a string

#### get_url

```python
def get_url(self) -> str:
    """Return the url of the software."""
    return self.__url
```

*Return the url of the software.*

#### set_url

```python
def set_url(self, name: str='') -> NoReturn:
    """Set a software url.

        :param name: (str) URL of the documented software
        :raises: TypeError: Given name is not a string

        """
    if isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.url. Got {} instead.".format(name))
    self.__url = name
```

*Set a software url.*

##### Parameters

- **name**: (*str*) URL of the documented software


##### Raises

- *TypeError*: Given name is not a string

#### get_copyright

```python
def get_copyright(self) -> str:
    """Return the copyright of the HTML page."""
    return self.__copyright
```

*Return the copyright of the HTML page.*

#### set_copyright

```python
def set_copyright(self, text: str=DEFAULT_COPYRIGHT) -> NoReturn:
    """Set a copyright text, added to the footer of the page.

        :param text: (str) Copyright of the documented software
        :raises: TypeError: Given text is not a string

        """
    if isinstance(text, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.copyright. Got {} instead.".format(text))
    self.__copyright = text
```

*Set a copyright text, added to the footer of the page.*

##### Parameters

- **text**: (*str*) Copyright of the documented software


##### Raises

- *TypeError*: Given text is not a string

#### get_icon

```python
def get_icon(self) -> str:
    """Return the icon filename of the software."""
    return self.__icon
```

*Return the icon filename of the software.*

#### set_icon

```python
def set_icon(self, name: str=DEFAULT_ICON) -> NoReturn:
    """Set an icon filename.

        :param name: (str) Filename of the icon of the documented software
        :raises: TypeError: Given name is not a string

        """
    if isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.icon. Got {} instead.".format(name))
    self.__icon = name
```

*Set an icon filename.*

##### Parameters

- **name**: (*str*) Filename of the icon of the documented software


##### Raises

- *TypeError*: Given name is not a string

#### get_title

```python
def get_title(self) -> str:
    """Return the title of the HTML page."""
    return self.__title
```

*Return the title of the HTML page.*

#### set_title

```python
def set_title(self, text: str=DEFAULT_TITLE) -> NoReturn:
    """Set a title to the output HTML pages.

        :param text: (str) Title of the HTML pages
        :raises: TypeError: Given text is not a string

        """
    if isinstance(text, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.title. Got {} instead.".format(text))
    self.__title = text
```

*Set a title to the output HTML pages.*

##### Parameters

- **text**: (*str*) Title of the HTML pages


##### Raises

- *TypeError*: Given text is not a string

#### get_statics

```python
def get_statics(self) -> str:
    """Return the static path of the CSS, JS, etc."""
    return self.__statics
```

*Return the static path of the CSS, JS, etc.*

#### set_statics

```python
def set_statics(self, name: str=DEFAULT_STATICS) -> NoReturn:
    """Set the static path of the customs CSS, JS, etc.

        :param name: (str) Path of the static elements
        :raises: TypeError: Given name is not a string

        """
    if isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.statics. Got {} instead.".format(name))
    self.__statics = name
```

*Set the static path of the customs CSS, JS, etc.*

##### Parameters

- **name**: (*str*) Path of the static elements


##### Raises

- *TypeError*: Given name is not a string

#### get_wexa_statics

```python
def get_wexa_statics(self) -> str:
    """Return the static path of the CSS, JS, etc. of Whakerexa. """
    return self.__wexa_statics
```

*Return the static path of the CSS, JS, etc. of Whakerexa.*

#### set_wexa_statics

```python
def set_wexa_statics(self, name: str=DEFAULT_WEXA_STATICS) -> NoReturn:
    """Set the static path of the customs CSS, JS, etc. of Whakerexa.

        :param name: (str) Path of the static elements
        :raises: TypeError: Given name is not a string

        """
    if isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.wexa_statics. Got {} instead.".format(name))
    self.__wexa_statics = name
```

*Set the static path of the customs CSS, JS, etc. of Whakerexa.*

##### Parameters

- **name**: (*str*) Path of the static elements


##### Raises

- *TypeError*: Given name is not a string

#### get_favicon

```python
def get_favicon(self) -> str:
    """Return the favicon filename of the HTML pages."""
    return self.__favicon
```

*Return the favicon filename of the HTML pages.*

#### set_favicon

```python
def set_favicon(self, name: str=DEFAULT_FAVICON) -> NoReturn:
    """Set a favicon to the output HTML pages.

        :param name: (str) Favicon of the HTML pages
        :raises: TypeError: Given name is not a string

        """
    if isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.favicon. Got {} instead.".format(name))
    self.__favicon = name
```

*Set a favicon to the output HTML pages.*

##### Parameters

- **name**: (*str*) Favicon of the HTML pages


##### Raises

- *TypeError*: Given name is not a string

#### get_theme

```python
def get_theme(self) -> str:
    """Return the theme of the HTML page."""
    return self.__theme
```

*Return the theme of the HTML page.*

#### set_theme

```python
def set_theme(self, name: str=DEFAULT_THEME) -> NoReturn:
    """Set a theme name.

        :param name: (str) Name of the theme of the HTML pages
        :raises: TypeError: Given name is not a string

        """
    if isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.theme. Got {} instead.".format(name))
    self.__theme = name
```

*Set a theme name.*

##### Parameters

- **name**: (*str*) Name of the theme of the HTML pages


##### Raises

- *TypeError*: Given name is not a string

#### get_description

```python
def get_description(self) -> str:
    """Return the 160 chars description of the HTML page."""
    return self.__theme
```

*Return the 160 chars description of the HTML page.*

#### set_description

```python
def set_description(self, descr: str='') -> NoReturn:
    """Set a 160 chars max description text.

        :param descr: (str) Description of the documented document
        :raises: TypeError: Given descr is not a string

        """
    if isinstance(descr, (str, bytes)) is False:
        raise TypeError("Expected a 'str' for the HTMLDocExport.descr. Got {} instead.".format(descr))
    descr = descr.replace('\n', ' ')
    descr = descr.replace("'", ' ')
    descr = descr.replace('"', ' ')
    if len(descr) < 90:
        logging.warning(f'Given description is a little bit shorted than the 90 expected characters: {descr}')
        descr = 'Python Class Documentation of ' + descr
    if len(descr) > 160:
        logging.warning(f'Given description is longer than 160 characters: {descr}.')
    self.__descr = descr[:160]
```

*Set a 160 chars max description text.*

##### Parameters

- **descr**: (*str*) Description of the documented document


##### Raises

- *TypeError*: Given descr is not a string

#### get_next_class

```python
def get_next_class(self) -> str:
    """Return the name of the next documented class."""
    return self.__next_class
```

*Return the name of the next documented class.*

#### set_next_class

```python
def set_next_class(self, name: str | None=None) -> NoReturn:
    """Set the name of the next documented class.

        :param name: (str|None) Name of the next documented class
        :raises: TypeError: Given name is not a string

        """
    if name is not None and isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' or None for the HTMLDocExport.next_class. Got {} instead.".format(name))
    self.__next_class = name
```

*Set the name of the next documented class.*

##### Parameters

- **name**: (*str*|None) Name of the next documented class


##### Raises

- *TypeError*: Given name is not a string

#### get_prev_class

```python
def get_prev_class(self) -> str:
    """Return the name of the previous documented class, for the ToC."""
    return self.__prev_class
```

*Return the name of the previous documented class, for the ToC.*

#### set_prev_class

```python
def set_prev_class(self, name: str | None=None) -> NoReturn:
    """Set the name of the previous documented class.

        :param name: (str|None) Name of the previous documented class
        :raises: TypeError: Given name is not a string

        """
    if name is not None and isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' or None for the HTMLDocExport.prev_class. Got {} instead.".format(name))
    self.__prev_class = name
```

*Set the name of the previous documented class.*

##### Parameters

- **name**: (*str*|None) Name of the previous documented class


##### Raises

- *TypeError*: Given name is not a string

#### get_next_module

```python
def get_next_module(self) -> str:
    """Return the name of the next documented module."""
    return self.__next_pack
```

*Return the name of the next documented module.*

#### set_next_module

```python
def set_next_module(self, name: str | None=None) -> NoReturn:
    """Set the name of the next documented module.

        :param name: (str|None) Name of the next documented module
        :raises: TypeError: Given name is not a string

        """
    if name is not None and isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' or None for the HTMLDocExport.next_module. Got {} instead.".format(name))
    self.__next_pack = name
```

*Set the name of the next documented module.*

##### Parameters

- **name**: (*str*|None) Name of the next documented module


##### Raises

- *TypeError*: Given name is not a string

#### get_prev_module

```python
def get_prev_module(self) -> str:
    """Return the name of the previous documented module, for the ToC."""
    return self.__prev_pack
```

*Return the name of the previous documented module, for the ToC.*

#### set_prev_module

```python
def set_prev_module(self, name: str | None=None) -> NoReturn:
    """Set the name of the previous documented module.

        :param name: (str|None) Name of the previous documented module
        :raises: TypeError: Given name is not a string

        """
    if name is not None and isinstance(name, (str, bytes)) is False:
        raise TypeError("Expected a 'str' or None for the HTMLDocExport.prev_module. Got {} instead.".format(name))
    self.__prev_pack = name
```

*Set the name of the previous documented module.*

##### Parameters

- **name**: (*str*|None) Name of the previous documented module


##### Raises

- *TypeError*: Given name is not a string

#### get_head

```python
def get_head(self) -> str:
    """Return the HTML 'head' of the page."""
    return ExportOptions.HTML_HEAD.format(TITLE=self.__title, FAVICON=self.__favicon, THEME=self.__theme, STATICS=self.__statics, WEXA_STATICS=self.__wexa_statics, META_DESCRIPTION=self.__descr)
```

*Return the HTML 'head' of the page.*

#### get_header

```python
def get_header(self) -> str:
    """Return the 'header' of the HTML->body of the page."""
    h = list()
    h.append('    <header>')
    h.append(ExportOptions.HTML_BUTTONS_ACCESSIBILITY.format(WEXA_STATICS=self.__wexa_statics))
    if len(self.__software) > 0:
        h.append('    <h1>{SOFTWARE}</h1>'.format(SOFTWARE=self.__software))
    if len(self.__icon) > 0:
        h.append('        <p><img class="small-logo" src="{STATICS}/{ICON}" alt="Software logo"/></p>'.format(STATICS=self.__statics, ICON=self.__icon))
    if len(self.__url) > 0:
        h.append('        <p><a class="external-link" href="{URL}">{URL}</a></p>'.format(URL=self.__url))
    h.append('    </header>')
    return '\n'.join(h)
```

*Return the 'header' of the HTML->body of the page.*

#### get_nav

```python
def get_nav(self) -> str:
    """Return the 'nav' of the HTML->body of the page."""
    nav = list()
    nav.append('<nav id="nav-book" class="side-nav">')
    if self.__software == ExportOptions.DEFAULT_SOFTWARE:
        nav.append('    <h1>Documentation</h1>')
    else:
        nav.append('    <h1>{SOFTWARE}</h1>'.format(SOFTWARE=self.__software))
    if len(self.__icon) > 0:
        nav.append('    <img class="small-logo center" src="{STATICS}/{ICON}" alt=""/>'.format(STATICS=self.__statics, ICON=self.__icon))
    if len(self.__url) > 0:
        nav.append('        <p><a class="external-link" href="{URL}">{URL}</a></p>'.format(URL=self.__url))
    nav.append('    <ul>')
    nav.append(ExportOptions.__nav_link('&crarr; Prev. Module', self.__prev_pack))
    nav.append(ExportOptions.__nav_link('&uarr; Prev. Class', self.__prev_class))
    nav.append(ExportOptions.__nav_link('&#8962; Index', 'index.html'))
    nav.append(ExportOptions.__nav_link('&darr; Next Class', self.__next_class))
    nav.append(ExportOptions.__nav_link('&rdsh; Next Module', self.__next_pack))
    nav.append('    </ul>')
    nav.append('    <h2>Table of Contents</h2>')
    nav.append('    <ul id="toc"></ul>')
    nav.append('    <hr>')
    nav.append('    <p><small>Automatically created</small></p><p><small>by <a class="external-link" href="https://clamming.sf.net">ClammingPy</a></small></p>')
    nav.append('</nav>')
    return '\n'.join(nav)
```

*Return the 'nav' of the HTML->body of the page.*

#### get_footer

```python
def get_footer(self) -> str:
    """Return the 'footer' of the HTML->body of the page."""
    return ExportOptions.HTML_FOOTER.format(COPYRIGHT=self.__copyright)
```

*Return the 'footer' of the HTML->body of the page.*



### Protected functions

#### __nav_link

```python
@staticmethod
def __nav_link(text: str, link: str | None) -> str:
    if link is None:
        a = 'aria-disabled="true"'
    else:
        a = 'href="{:s}"'.format(link)
    return '<li><a role="button" tabindex="0" {LINK}> {TEXT}</a></li>'.format(LINK=a, TEXT=text)
```







~ Created using [Clamming](https://clamming.sf.net) version 2.1 ~
