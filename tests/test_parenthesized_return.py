import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixParenthesesInReturn


@pytest.mark.parametrize(
    "original,expected",
    [
        ("""def f(): return (42,)""", """def f(): return 42,"""),
        (
            """def f(): return (True, 'User is not welcome')""",
            """def f(): return True, 'User is not welcome'""",
        ),
        (
            """
def f():
    return (
        True, 
        "User is not welcome"
    )
            """,
            None,
        ),
    ],
)
def test_removal_of_parentheses_in_return(original, expected):
    processed, _ = process_file(original, [FixParenthesesInReturn()])

    assert processed == (expected or original)
