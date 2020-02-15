from typing import Union

import libcst as cst
from libcst import matchers as m

from pybetter.transformers.base import NoqaAwareTransformer


class EqualsNoneIsNoneTransformer(NoqaAwareTransformer):
    def leave_ComparisonTarget(
        self, original_node: cst.ComparisonTarget, updated_node: cst.ComparisonTarget
    ) -> Union[cst.ComparisonTarget, cst.RemovalSentinel]:
        if not m.matches(
            updated_node,
            m.ComparisonTarget(comparator=m.Name(value="None"), operator=m.Equal()),
        ):
            return original_node

        original_op = cst.ensure_type(original_node.operator, cst.Equal)

        return updated_node.with_changes(
            operator=cst.Is(
                whitespace_after=original_op.whitespace_after,
                whitespace_before=original_op.whitespace_before,
            )
        )


__all__ = ["EqualsNoneIsNoneTransformer"]
