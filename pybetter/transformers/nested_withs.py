from typing import Union, List

import libcst as cst
import libcst.matchers as m
from libcst.metadata import PositionProvider

from pybetter.transformers.base import NoqaAwareTransformer


class NestedWithTransformer(NoqaAwareTransformer):
    def has_leading_comment(
        self, node: Union[cst.SimpleStatementLine, cst.With]
    ) -> bool:
        return any([line.comment is not None for line in node.leading_lines])

    def has_comment(self, node: cst.BaseSuite):
        return m.matches(
            node,
            m.IndentedBlock(
                header=m.AllOf(
                    m.TrailingWhitespace(),
                    m.MatchIfTrue(lambda h: h.comment is not None),
                )
            ),
        )

    def leave_With(
        self, original_node: cst.With, updated_node: cst.With
    ) -> Union[cst.BaseStatement, cst.RemovalSentinel]:

        candidate_with: cst.With = original_node
        compound_items: List[cst.WithItem] = []
        final_body: BaseSuite = None

        while True:
            if self.has_leading_comment(candidate_with):
                break

            if self.has_comment(candidate_with.body):
                break

            compound_items.extend(candidate_with.items)
            final_body = candidate_with.body

            if not isinstance(candidate_with.body.body[0], cst.With):
                break

            candidate_with = cst.ensure_type(candidate_with.body.body[0], cst.With)

        if not compound_items:
            return original_node

        return updated_node.with_changes(body=final_body, items=compound_items)
