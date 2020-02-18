import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixEqualsNone

NO_CHANGES_MADE = None

TRIVIAL_NONE_COMPARISON = (
    """
    if a == None:
        pass 
    """,
    """
    if a is None:
        pass
    """,
)


NONE_IDENTITY_CHECK_IGNORED = (
    """
    if a is None:
        pass
    """,
    NO_CHANGES_MADE,
)


NESTED_NONE_CMPS_PROCESSED = (
    """
    if a == None == None == None:
        pass
    """,
    """
    if a is None is None is None:
        pass
    """,
)


@pytest.mark.parametrize(
    "original,expected",
    [TRIVIAL_NONE_COMPARISON, NONE_IDENTITY_CHECK_IGNORED, NESTED_NONE_CMPS_PROCESSED],
    ids=[
        "trivial comparison with None",
        "identity check with None",
        "multiple comparisons with None",
    ],
)
def test_trivial_fmt_string_conversion(original, expected):
    processed, _ = process_file(original.strip(), [FixEqualsNone])

    assert processed.strip() == (expected or original).strip()
