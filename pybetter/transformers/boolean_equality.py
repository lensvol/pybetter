from typing import List

import libcst as cst
from libcst import matchers as m

from pybetter.transformers.base import NoqaAwareTransformer


class BooleanLiteralEqualityTransformer(NoqaAwareTransformer):
    def leave_Comparison(
        self, original_node: cst.Comparison, updated_node: cst.Comparison
    ) -> cst.BaseExpression:
        remaining_targets: List[cst.ComparisonTarget] = []

        for target in original_node.comparisons:
            if m.matches(
                target,
                m.ComparisonTarget(comparator=m.Name("False"), operator=m.Equal()),
            ):
                return cst.UnaryOperation(
                    operator=cst.Not(), expression=original_node.left
                )

            if not m.matches(
                target,
                m.ComparisonTarget(comparator=m.Name("True"), operator=m.Equal()),
            ):
                remaining_targets.append(target)

        # FIXME: Explicitly check for `a == False == True ...` case and
        # short-circuit it to `not a`.

        if not remaining_targets:
            return original_node.left

        return updated_node.with_changes(comparisons=remaining_targets)


__all__ = ["BooleanLiteralEqualityTransformer"]
