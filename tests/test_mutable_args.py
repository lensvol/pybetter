import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixMutableDefaultArgs

NO_CHANGES_MADE = None

# In these samples we do not use indents for formatting,
# since this transformer uses module's inferred indentation
# settings, and those will be like _8_ spaces or such.
NON_MUTABLE_DEFAULTS_IGNORED = (
    """
def f(a=None, b=frozenset(), c=42):
    pass
    """,
    NO_CHANGES_MADE,
)

EMPTY_MUTABLE_DEFAULT_EXTRACTED = (
    """
def f(a=[]):
    pass
    """,
    """
def f(a=None):

    if a is None:
        a = []

    pass
    """,
)

NONEMPTY_MUTABLE_DEFAULT_EXTRACTED = (
    """
def f(a=[42]):
    pass
    """,
    """
def f(a=None):

    if a is None:
        a = [42]

    pass
    """,
)

NESTED_FUNCTIONS_ARE_PROCESSED = (
    """
def outer(a=[53]):
    def inner(b=[42]):
        pass
    """,
    """
def outer(a=None):

    if a is None:
        a = [53]

    def inner(b=None):

        if b is None:
            b = [42]

        pass
    """,
)


@pytest.mark.wip
@pytest.mark.parametrize(
    "original,expected",
    [
        NON_MUTABLE_DEFAULTS_IGNORED,
        EMPTY_MUTABLE_DEFAULT_EXTRACTED,
        NONEMPTY_MUTABLE_DEFAULT_EXTRACTED,
        NESTED_FUNCTIONS_ARE_PROCESSED,
    ],
    ids=[
        "non-mutable defaults are ignored",
        "empty mutable default is extracted",
        "non-empty mutable default",
        "nested functions with defaults",
    ],
)
def test_mutable_defaults_extraction(original, expected):
    processed, _ = process_file(original.strip(), [FixMutableDefaultArgs()])
    assert processed.strip() == (expected or original).strip()
