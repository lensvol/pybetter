import pytest

from pybetter.cli import process_file
from pybetter.improvements import FixTrivialNestedWiths


NO_CHANGES_MADE = None

TRIVIAL_NESTED_WITH = (
    """
with a():
    with b():
        print("Hello, world!")
    """,
    """
with a(), b():
    print("Hello, world!")
    """,
)

MULTIPLE_LEVEL_NESTED_WITH = (
    """
with a():
    with b():
        with c():
            print("Hello, world!")
    """,
    """
with a(), b(), c():
    print("Hello, world!")
    """,
)

STATEMENTS_BETWEEN_WITHS = (
    """
with a():
    constant = 42
    with b():
        print("Hello, world!")
    """,
    NO_CHANGES_MADE,
)

INLINE_COMMENT_PREVENTS_COLLAPSE = (
    """
with a(): # TODO: something
    with b():
        print("Hello, world!")
    """,
    NO_CHANGES_MADE,
)

LEADING_COMMENT_PREVENTS_COLLAPSE = (
    """
with a():
    # TODO: something
    with b():
        print("Hello, world!")
    """,
    NO_CHANGES_MADE,
)

COMMENT_IN_OUTERMOST_FOOTER_IS_PRESERVED = (
    """
with a():
    with b():
        print("Hello, world!")

    # Roses are red,
    # Violets are blue,
    # Sugar is sweet,
    # And so are you.
    """,
    """
with a(), b():
    print("Hello, world!")

    # Roses are red,
    # Violets are blue,
    # Sugar is sweet,
    # And so are you.
    """,
)

SINGLE_LINE_BODY_IS_PRESERVED = (
    """
with a():
    with b():
        import pdb; pdb.set_trace()
    """,
    """
with a(), b():
    import pdb; pdb.set_trace()
    """,
)

ALIASES_ARE_PRESERVED = (
    """
with a() as another_a:
    with b() as other_b:
        another_a.call()
        other_b.call()
    """,
    """
with a() as another_a, b() as other_b:
    another_a.call()
    other_b.call()
    """,
)

UNRELATED_CODE_IS_NOT_PROCESSED = (
    """
a = 2
b = 3
assert a + b == 5
    """,
    NO_CHANGES_MADE,
)

SINGLE_WITH_IS_LEFT_ALONE = (
    """
with logger():
    print("Hello, world!")
    """,
    NO_CHANGES_MADE,
)


@pytest.mark.parametrize(
    "original,expected",
    [
        TRIVIAL_NESTED_WITH,
        MULTIPLE_LEVEL_NESTED_WITH,
        STATEMENTS_BETWEEN_WITHS,
        INLINE_COMMENT_PREVENTS_COLLAPSE,
        LEADING_COMMENT_PREVENTS_COLLAPSE,
        COMMENT_IN_OUTERMOST_FOOTER_IS_PRESERVED,
        SINGLE_LINE_BODY_IS_PRESERVED,
        UNRELATED_CODE_IS_NOT_PROCESSED,
        SINGLE_WITH_IS_LEFT_ALONE,
        ALIASES_ARE_PRESERVED,
    ],
    ids=[
        "trivial nested 'with'",
        "multiple nested 'with's",
        "statements between 'with's",
        "inline comment prevents collapse",
        "leading comment prevents collapse",
        "outermost comment is preserved",
        "single line body is preserved",
        "unrelated code",
        "single 'with' is left alone",
        "'with' aliases are preserved",
    ],
)
def test_collapse_of_nested_with_statements(original, expected):
    processed, _ = process_file(original.strip(), [FixTrivialNestedWiths])

    assert processed.strip() == (expected or original).strip()
