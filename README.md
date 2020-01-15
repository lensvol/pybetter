# pybetter
![PyPI](https://img.shields.io/pypi/v/pybetter) 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybetter)
![GitHub](https://img.shields.io/github/license/lensvol/pybetter)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tool for fixing trivial problems with your code.

Originally intended as an example for my PyCon Belarus 2020 talk about [LibCST](https://github.com/Instagram/LibCST).

## Usage

Simply provide a valid Python source code file as one of the argument and it will try to fix any issues it could find.

```
Usage: pybetter [OPTIONS] [SOURCES]...

Options:
  --noop  Do not make any changes to the source files.
  --help  Show this message and exit.
```



## Example

```shell
# cat test.py
def f():
    return (42, "Hello, world")

# pybetter test.py
--> Processing 'test.py'...
  [+] (B003) Remove parentheses from the tuple in 'return' statement.
All done!

# cat test.py
def f():
    return 42, "Hello, world"

```



## Available fixers

* **B001: Replace 'not A in B' with 'A not in B'**

  Usage of `A not in B` over `not A in B` is recommended both by Google and [PEP-8](https://www.python.org/dev/peps/pep-0008/#programming-recommendations). Both of those forms are compiled to the same bytecode, but second form has some potential of confusion for the reader. 

  ```python
  # BEFORE:
  if not 42 in counts:
      sys.exit(-1)
  
  # AFTER:
  if 42 not in counts:
      sys.exit(-1)
  ```

  

* **B002: Default values for `kwargs` are mutable.**

  As described in [Common Gotchas] (https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments) section of "The Hitchhiker's Guide to Python", mutable arguments can be a tricky thing. 

  This fixer replaces any default values that happen to be lists or dicts with **None** value, moving initialization from function definition into function body.

  ```python
  # BEFORE
  def p(a=[]):
      print(a)
    
  # AFTER
  def p(a=None):
      if a is None:
          a = []
      
      print(a)
  ```

  Be warned, that this fix may break code which *intentionally* uses mutable default arguments (e.g. caching).

* **B003: Remove parentheses from the tuple in 'return' statement.**

  If you are returning a tuple from the function by implicitly constructing it, then additional parentheses around it are redundant.

  ```python
  # BEFORE:
  def hello():
      return ("World", 42)
  
  # AFTER:
  def hello():
      return "World", 42
  ```

* **B004: `__all__` attribute is missing..**

  Regenerate missing `__all__` attribute, filling it with the list of top-level function and class names.

  *NB*: It will ignore any names starting with `_` to prevent any private members from ending up in the list.
  
  ```python
  # BEFORE:
def hello():
      return ("World", 42)
  
  class F:
      pass
  
  # AFTER:
  def hello():
      return "World", 42
  
  class F:
      pass
  
  __all__ = [
    "F",
    "hello",
  ]
  ```
  
* **B005: Replace "A == None" with "A is None"**

  "Comparisons to singletons like None should always be done with `is` or `is not`, never the equality operators." ([PEP8](https://www.python.org/dev/peps/pep-0008/))

  ```python
  # BEFORE:
  
  if a == None:
      pass
    
  # AFTER:
  
  if a is None:
      pass
  ```

## Installation

```shell script
# pip install pybetter
```

## Getting started with development

```shell script
# git clone https://github.com/lensvol/pybetter
# poetry install
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Authors

* **Kirill Borisov** ([lensvol@gmail.com](mailto:lensvol@gmail.com))
