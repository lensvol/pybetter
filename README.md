# pybetter
![PyPI](https://img.shields.io/pypi/v/pybetter) 
![Downloads](https://img.shields.io/pypi/dm/pybetter)
![Travis CI](https://img.shields.io/travis/com/lensvol/pybetter)
![Code coverage](https://img.shields.io/codecov/c/github/lensvol/pybetter)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybetter)
![License](https://img.shields.io/github/license/lensvol/pybetter)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tool for fixing trivial problems with your code.

Originally intended as an example for my PyCon Belarus 2020 talk about [LibCST](https://github.com/Instagram/LibCST).

## Usage

Simply provide a valid Python source code file as one of the argument and it will try to fix any issues it could find.

```
Usage: pybetter [OPTIONS] [PATHS]...

Options:
  --noop              Do not make any changes to the source files.
  --diff              Show diff-like output of the changes made.
  --select CODES      Apply only improvements with the provided codes.
  --exclude CODES     Exclude improvements with the provided codes.
  --exit-code <CODE>  Exit with provided code if fixes were applied.
  --help              Show this message and exit.
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

  As described in [Common Gotchas](https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments) section of "The Hitchhiker's Guide to Python", mutable arguments can be a tricky thing. This fixer replaces any default values that happen to be lists or dicts with **None** value, moving initialization from function definition into function body.

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

* **B004: `__all__` attribute is missing.**

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
  
* **B006: Remove comparisons with either 'False' or 'True'.**

  [PEP8](https://www.python.org/dev/peps/pep-0008/) recommends that conditions should be evaluated without explicit equality comparison with `True`/`False` singletons. In Python, every non-empty value is treated as `True` and vice versa,

  so in most cases those comparisons can be safely eliminated.

  *NB*: `is True` and `is False` checks are not affected, since they can be used to explicitly check for equality with a specific singleton, instead of using abovementioned "non-empty" heuristic.

  ```python
  # BEFORE:
  
  if a == False or b == True or c == False == True:
      pass
    
  # AFTER:
  
  if a or b or c:
      pass
  ```
  
* **B007: Convert f-strings without expressions into regular strings.**

  It is wasteful to use f-string mechanism if there are no expressions to be extrapolated. 

  ```python
  # BEFORE:
  a = f"Hello, world"
  
  # AFTER:
  a = "Hello, world"
  ```

* **B008: Collapse nested `with` statements**

  Degenerate `with` statements can be rewritten as a single compound `with` statement, if following conditions are satisfied:

  * There are no statements between `with` statements being collapsed;
  * Neither of `with` statements has any leading or inline comments.

  ```python
  # BEFORE:
  with a():
      with b() as other_b:
          print("Hello, world!")

  # AFTER:
  with a(), b() as other_b:
      print("Hello, world!")
  ```

* **B009: Replace unhashable list literals in set constructors**

  Lists cannot be used as elements of the sets due to them being mutable and hence "unhashable". We can fix the more trivial cases of list literals being used to create a set by converting them into tuples.

  ```python
  # BEFORE:
  a = {
    [1, 2, 3],
  }
  b = set([[1, 2], ["a", "b"]])
  c = frozenset([[1, 2], ["a", "b"]])

  # AFTER:
  a = {
    (1, 2, 3)
  }
  b = set([(1, 2), ("a", "b")])
  c = frozenset([(1, 2), ("a", "b")])
  ```

* **B010: Replace 'not A is B' with 'A is not B'**

  Usage of `A is not B` over `not A is B` is recommended both by Google and [PEP-8](https://www.python.org/dev/peps/pep-0008/#programming-recommendations). Both of those forms are compiled to the same bytecode, but second form has some potential of confusion for the reader.
  (thanks to @rs2 for submitting this!).  

  ```python
  # BEFORE:
  if not obj is Record:
      sys.exit(-1)
  
  # AFTER:
  if obj is not Record:
      sys.exit(-1)
  ```

**NB:** Each of the fixers can be disabled on per-line basis using [flake8's "noqa" comments](http://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html#in-line-ignoring-errors).

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
