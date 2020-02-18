import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixMutableDefaultArgs

NO_CHANGES_MADE = None

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


@pytest.mark.wip
@pytest.mark.parametrize(
    "original,expected",
    [NON_MUTABLE_DEFAULTS_IGNORED, EMPTY_MUTABLE_DEFAULT_EXTRACTED],
    ids=["non-mutable defaults are ignored", "empty mutable default is extracted"],
)
def test_mutable_defaults_extraction(original, expected):
    processed, _ = process_file(original.strip(), [FixMutableDefaultArgs()])
    assert processed.strip() == (expected or original).strip()
