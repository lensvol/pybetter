import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixParenthesesInReturn


NO_CHANGES_MADE = None

TRIVIAL_RETURNED_TUPLE = (
    """
    def f():
        return (42,)
    """,
    """
    def f():
        return 42,
    """,
)

MULTIPLE_ELEMENT_TUPLE = (
    """
    def f():
        return (True, 'User is not welcome')
    """,
    """
    def f():
        return True, 'User is not welcome'
    """,
)

MULTILINE_RETURN_TUPLE = (
    """
    def f():
        return (
            True, 
            "User is not welcome"
        )
    """,
    NO_CHANGES_MADE,
)


TUPLE_INSIDE_RETURN_EXPR = (
    """
    def f():
        return {"42", ("abcdef",)} 
    """,
    NO_CHANGES_MADE,
)


EMPTY_TUPLE_RETURN_EXPR = (
    """
    def foo() -> typing.Tuple:
        return ()
    """,
    NO_CHANGES_MADE,
)


@pytest.mark.parametrize(
    "original,expected",
    [
        TRIVIAL_RETURNED_TUPLE,
        MULTIPLE_ELEMENT_TUPLE,
        MULTILINE_RETURN_TUPLE,
        TUPLE_INSIDE_RETURN_EXPR,
        EMPTY_TUPLE_RETURN_EXPR,
    ],
    ids=[
        "trivial returned tuple",
        "multiple elements in returned tuple",
        "multi-line returns not processed",
        "tuple inside returned expression",
        "function returns empty tuple",
    ],
)
def test_removal_of_parentheses_in_return(original, expected):
    processed, _ = process_file(original.strip(), [FixParenthesesInReturn])

    assert processed.strip() == (expected or original).strip()
