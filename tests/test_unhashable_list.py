import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixUnhashableList

NO_CHANGES_MADE = None

TRIVIAL_LIST_LITERAL = (
    """
    {[1, 2]}
    """,
    """
    {(1, 2)}
    """,
)


SET_FUNCTION_LIST_ARGUMENT = (
    """
    set([["a", "b"], "c"])
    """,
    """
    set([("a", "b"), "c"])
    """,
)


FROZENSET_FUNCTION_LIST_ARGUMENT = (
    """
    frozenset([["a", "b"], "c"])
    """,
    """
    frozenset([("a", "b"), "c"])
    """,
)


SET_FUNCTION_SET_ARGUMENT = (
    """
    set({["a", "b"], "c"})
    """,
    """
    set({("a", "b"), "c"})
    """,
)


FROZENSET_FUNCTION_SET_ARGUMENT = (
    """
    frozenset({["a", "b"], "c"})
    """,
    """
    frozenset({("a", "b"), "c"})
    """,
)

SET_FUNCTION_TUPLE_ARGUMENT = (
    """
    set((["a", "b"], "c"))
    """,
    """
    set((("a", "b"), "c"))
    """,
)


FROZENSET_FUNCTION_TUPLE_ARGUMENT = (
    """
    frozenset((["a", "b"], "c"))
    """,
    """
    frozenset((("a", "b"), "c"))
    """,
)

NESTED_LIST_LITERAL = (
    """
    {[["a", "b"], 2]}
    """,
    """
    {(("a", "b"), 2)}
    """,
)

TUPLES_ARE_UNCHANGED = (
    """
    {(1, 2), "a"}
    """,
    NO_CHANGES_MADE,
)


REGULAR_LIST_ARGUMENTS_ARE_UNCHANGED = (
    """
    {func([1, 2, 3])}
    """,
    NO_CHANGES_MADE,
)


COMPLEX_LIST_ARGUMENTS_ARE_UNCHANGED = (
    """
    {frozenset(set([func([1, 2, 3])]))}
    """,
    NO_CHANGES_MADE,
)


NESTED_SETS_ARE_PROCESSED = (
    """
    {
        {[1, 2]},
        {
            set([[1, 2], ["a", "b"]])
        },
    }
    """,
    """
    {
        {(1, 2)},
        {
            set([(1, 2), ("a", "b")])
        },
    }
    """,
)


@pytest.mark.parametrize(
    "original,expected",
    [
        TRIVIAL_LIST_LITERAL,
        SET_FUNCTION_LIST_ARGUMENT,
        SET_FUNCTION_SET_ARGUMENT,
        SET_FUNCTION_TUPLE_ARGUMENT,
        FROZENSET_FUNCTION_LIST_ARGUMENT,
        FROZENSET_FUNCTION_SET_ARGUMENT,
        FROZENSET_FUNCTION_TUPLE_ARGUMENT,
        NESTED_LIST_LITERAL,
        TUPLES_ARE_UNCHANGED,
        NESTED_SETS_ARE_PROCESSED,
        COMPLEX_LIST_ARGUMENTS_ARE_UNCHANGED,
    ],
)
def test_replacement_of_list_literal_in_sets(original, expected):
    processed, _ = process_file(original.strip(), [FixUnhashableList()])

    assert processed.strip() == (expected or original).strip()
