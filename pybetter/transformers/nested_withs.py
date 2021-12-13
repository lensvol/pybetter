from typing import Union, List

import libcst as cst
import libcst.matchers as m

from pybetter.transformers.base import NoqaAwareTransformer


def has_leading_comment(node: Union[cst.SimpleStatementLine, cst.With]) -> bool:
    return any([line.comment is not None for line in node.leading_lines])


def has_inline_comment(node: cst.BaseSuite):
    return m.matches(
        node,
        m.IndentedBlock(
            header=m.AllOf(
                m.TrailingWhitespace(), m.MatchIfTrue(lambda h: h.comment is not None)
            )
        ),
    )


def has_footer_comment(body):
    return m.matches(
        body,
        m.IndentedBlock(
            footer=[m.ZeroOrMore(), m.EmptyLine(comment=m.Comment()), m.ZeroOrMore()]
        ),
    )


class NestedWithTransformer(NoqaAwareTransformer):
    def leave_With(
        self, original_node: cst.With, updated_node: cst.With
    ) -> Union[cst.BaseStatement, cst.RemovalSentinel]:

        candidate_with: cst.With = original_node
        compound_items: List[cst.WithItem] = []
        final_body: cst.BaseSuite = candidate_with.body

        while True:
            # There is no way to meaningfully represent comments inside
            # multi-line `with` statements due to how Python grammar is
            # written, so we do not try to transform such `with` statements
            # lest we lose something important in the comments.
            if has_leading_comment(candidate_with):
                break

            if has_inline_comment(candidate_with.body):
                break

            # There is no meaningful way `async with` can be merged into
            # the compound `with` statement.
            if candidate_with.asynchronous:
                break

            compound_items.extend(candidate_with.items)
            final_body = candidate_with.body

            if not isinstance(final_body.body[0], cst.With):
                break

            if len(final_body.body) > 1:
                break

            candidate_with = cst.ensure_type(candidate_with.body.body[0], cst.With)

        if len(compound_items) <= 1:
            return original_node

        final_body = cst.ensure_type(final_body, cst.IndentedBlock)
        topmost_body = cst.ensure_type(original_node.body, cst.IndentedBlock)

        if has_footer_comment(topmost_body) and not has_footer_comment(final_body):
            final_body = final_body.with_changes(
                footer=(*final_body.footer, *topmost_body.footer)
            )

        return updated_node.with_changes(body=final_body, items=compound_items)


__all__ = ["NestedWithTransformer"]
