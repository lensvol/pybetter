from typing import Union

import libcst as cst
from libcst import RemovalSentinel, ComparisonTarget
from libcst import matchers as m


class EqualsNoneIsNoneTransformer(cst.CSTTransformer):
    def leave_ComparisonTarget(
        self, original_node: ComparisonTarget, updated_node: ComparisonTarget
    ) -> Union[ComparisonTarget, RemovalSentinel]:
        if not m.matches(
            original_node,
            m.ComparisonTarget(comparator=m.Name(value="None"), operator=m.Equal()),
        ):
            return original_node

        return updated_node.with_changes(
            operator=cst.Is(
                whitespace_after=original_node.operator.whitespace_after,
                whitespace_before=original_node.operator.whitespace_before,
            )
        )
