from typing import Union

import libcst as cst
from libcst import matchers as m

from pybetter.transformers.base import NoqaAwareTransformer


class EqualsNoneIsNoneTransformer(NoqaAwareTransformer):
    @m.leave(m.ComparisonTarget(comparator=m.Name(value="None"), operator=m.Equal()))
    def convert_none_cmp(
        self, _, updated_node: cst.ComparisonTarget
    ) -> Union[cst.ComparisonTarget, cst.RemovalSentinel]:
        original_op = cst.ensure_type(updated_node.operator, cst.Equal)

        return updated_node.with_changes(
            operator=cst.Is(
                whitespace_after=original_op.whitespace_after,
                whitespace_before=original_op.whitespace_before,
            )
        )


__all__ = ["EqualsNoneIsNoneTransformer"]
