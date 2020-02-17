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


@pytest.mark.parametrize(
    "original,expected",
    [TRIVIAL_NOT_A_IN_B_CASE, PARENS_NOT_A_IN_B_CASE, NESTED_COMPARISONS],
)
def test_not_in_transformation(original, expected):
    processed, _ = process_file(original.strip(), [FixNotInConditionOrder()])

    assert processed.strip() == (expected or original).strip()
