import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixBooleanEqualityChecks


@pytest.mark.parametrize(
    "original,expected",
    [
        ("a == False", "not a"),
        ("a == True", "a"),
        ("a == b < 42 == True", "a == b < 42"),
        ("(a == True) == False", "not (a == True)"),
    ],
)
def test_boolean_equality_fix(original, expected):
    processed, _ = process_file(original, [FixBooleanEqualityChecks()])

    assert processed == expected
