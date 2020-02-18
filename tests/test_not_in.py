import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixEqualsNone, FixNotInConditionOrder

NO_CHANGES_MADE = None

TRIVIAL_NOT_A_IN_B_CASE = (
    """
    if not a in b:
        pass 
    """,
    """
    if a not in b:
        pass
    """,
)

PARENS_NOT_A_IN_B_CASE = (
    """
    if not (a in b):
        pass 
    """,
    """
    if a not in b:
        pass
    """,
)

NESTED_COMPARISONS = (
    """
    if not ((not a in b) in d):
        pass
    """,
    """
    if (a not in b) not in d:
        pass
    """,
)

DIFFERENT_COMPARISONS_IN_ROW = (
    """
    if not (a in b and a > 42):
        pass
    """,
    NO_CHANGES_MADE,
)

CONSECUTIVE_COMPARISONS_UNCHANGED = (
    """
    if not (a in b in c in d):
        pass
    """,
    NO_CHANGES_MADE,
)


@pytest.mark.parametrize(
    "original,expected",
    [
        TRIVIAL_NOT_A_IN_B_CASE,
        PARENS_NOT_A_IN_B_CASE,
        NESTED_COMPARISONS,
        DIFFERENT_COMPARISONS_IN_ROW,
        CONSECUTIVE_COMPARISONS_UNCHANGED,
    ],
    ids=[
        "trivial 'not A in B'",
        "parenthesized 'not A in B'",
        "nested comparisons",
        "several types of comparisons",
        "consecutive comparisons",
    ],
)
def test_not_in_transformation(original, expected):
    processed, _ = process_file(original.strip(), [FixNotInConditionOrder])

    assert processed.strip() == (expected or original).strip()
