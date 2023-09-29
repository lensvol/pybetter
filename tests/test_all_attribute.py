import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixMissingAllAttribute

NO_CHANGES_MADE = None

TRIVIAL_CASE_ONLY_GLOBALS = (
    """
def f():
    pass

class A:
    pass

abc = None
    """,
    """
def f():
    pass

class A:
    pass

abc = None


__all__ = [
    'A',
    'abc',
    'f'
]
    """,
)


NESTED_DEFINITIONS_ARE_IGNORED = (
    """
def f():
    def inner():
        pass

class A:
    def method(self):
        self.inner_abc = 42


abc = None
    """,
    """
def f():
    def inner():
        pass

class A:
    def method(self):
        self.inner_abc = 42


abc = None


__all__ = [
    'A',
    'abc',
    'f'
]
    """,
)

PRIVATE_DEFINITIONS_ARE_IGNORED = (
    """
def _private_func():
    pass

class _A:
    pass

_abc = None

def public():
    pass
    """,
    """
def _private_func():
    pass

class _A:
    pass

_abc = None

def public():
    pass


__all__ = [
    'public'
]
    """,
)

EXISTING_ALL_IS_UNCHANGED = (
    """
def func():
    pass

class A:
    pass

abc = None

__all__ = ["A"]
    """,
    NO_CHANGES_MADE,
)

EMPTY_ALL_IS_NOT_GENERATED = (
    """
def _func():
    pass

class _A:
    pass

_abc = None
    """,
    NO_CHANGES_MADE,
)

DUPLICATES_REMOVED = (
    """
from typing import overload

@overload
def a(v: int) -> int: ...

@overload
def a(v: str) -> str: ...

def b() -> int: ...

def a(v: int | str ) -> int | str: ...
    """,
    """
from typing import overload

@overload
def a(v: int) -> int: ...

@overload
def a(v: str) -> str: ...

def b() -> int: ...

def a(v: int | str ) -> int | str: ...


__all__ = [
    'a',
    'b'
]
    """,
)


@pytest.mark.parametrize(
    "original,expected",
    [
        TRIVIAL_CASE_ONLY_GLOBALS,
        NESTED_DEFINITIONS_ARE_IGNORED,
        PRIVATE_DEFINITIONS_ARE_IGNORED,
        EXISTING_ALL_IS_UNCHANGED,
        EMPTY_ALL_IS_NOT_GENERATED,
        DUPLICATES_REMOVED,
    ],
    ids=[
        "trivial case",
        "nested definitions are ignored",
        "private definitions are ignored",
        "existing __all__ is unchanged",
        "empty __all__ is not generated",
        "duplicates removed",
    ],
)
def test_generation_of_dunder_all(original, expected):
    processed, _ = process_file(original.strip(), [FixMissingAllAttribute])

    assert processed.strip() == (expected or original).strip()
