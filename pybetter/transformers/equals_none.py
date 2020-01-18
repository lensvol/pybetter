from typing import Union

import libcst as cst
from libcst import matchers as m


class EqualsNoneIsNoneTransformer(cst.CSTTransformer):
    def leave_ComparisonTarget(
        self, original_node: cst.ComparisonTarget, updated_node: cst.ComparisonTarget
    ) -> Union[cst.ComparisonTarget, cst.RemovalSentinel]:
        if not m.matches(
            updated_node,
            m.ComparisonTarget(comparator=m.Name(value="None"), operator=m.Equal()),
        ):
            return original_node

        return updated_node.with_changes(
            operator=cst.Is(
                # For some reason, mypy cannot understand that operator is cst.Equal,
                # even with explicit direction by cst.ensure_type :/
                whitespace_after=updated_node.operator.whitespace_after,  # type: ignore
                whitespace_before=updated_node.operator.whitespace_before,  # type: ignore
            )
        )
