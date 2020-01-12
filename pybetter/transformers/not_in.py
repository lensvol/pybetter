from typing import List

import libcst as cst
import libcst.matchers as m


class NotInConditionTransformer(cst.CSTTransformer):
    @m.call_if_inside(
        m.UnaryOperation(
            operator=m.Not(),
            expression=m.Comparison(comparisons=[m.ComparisonTarget(operator=m.In())]),
        )
    )
    def leave_UnaryOperation(
        self, original_node: cst.UnaryOperation, updated_node: cst.UnaryOperation
    ) -> cst.BaseExpression:
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
