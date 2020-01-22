from typing import List

import libcst as cst
import libcst.matchers as m

from pybetter.transformers.base import NoqaAwareTransformer


class NotInConditionTransformer(NoqaAwareTransformer):
    def leave_UnaryOperation(
        self, original_node: cst.UnaryOperation, updated_node: cst.UnaryOperation
    ) -> cst.BaseExpression:
        if not m.matches(
            original_node,
            m.UnaryOperation(
                operator=m.Not(),
                expression=m.Comparison(
                    comparisons=[m.ComparisonTarget(operator=m.In())]
                ),
            ),
        ):
            return original_node

        fixed_comparisons: List[cst.ComparisonTarget] = []
        comparison_node: cst.Comparison = cst.ensure_type(
            original_node.expression, cst.Comparison
        )

        for target in comparison_node.comparisons:
            if m.matches(target, m.ComparisonTarget(operator=m.In())):
                fixed_comparisons.append(target.with_changes(operator=cst.NotIn()))
            else:
                fixed_comparisons.append(target)

        return cst.Comparison(left=comparison_node.left, comparisons=fixed_comparisons)
