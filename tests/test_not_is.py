import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixNotIsConditionOrder

NO_CHANGES_MADE = None

TRIVIAL_NOT_A_IS_B_CASE = (
    """
    if not a is B:
        pass
    """,
    """
    if a is not B:
        pass
    """,
)


MULTIPLE_NOT_A_IS_B_CASE = (
    """
    if foo is not None and not bar is None:
        pass
    """,
    """
    if foo is not None and bar is not None:
        pass
    """,
)


NESTED_NOT_A_IS_B_CASE = (
    """
    if not foo is (not A is B):
        pass
    """,
    """
    if foo is not (A is not B):
        pass
    """,
)


@pytest.mark.parametrize(
    "original,expected",
    [
        TRIVIAL_NOT_A_IS_B_CASE,
        MULTIPLE_NOT_A_IS_B_CASE,
        NESTED_NOT_A_IS_B_CASE,
    ],
    ids=[
        "trivial 'not A is B' case",
        "multiple 'not A is B' in same expression",
        "nested 'not A is B' case",
    ],
)
def test_not_in_transformation(original, expected):
    processed, _ = process_file(original.strip(), [FixNotIsConditionOrder])

    assert processed.strip() == (expected or original).strip()
