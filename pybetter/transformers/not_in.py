from typing import List

import libcst as cst
import libcst.matchers as m

from pybetter.transformers.base import NoqaAwareTransformer


class NotInConditionTransformer(NoqaAwareTransformer):
    @m.leave(
        m.UnaryOperation(
            operator=m.Not(),
            expression=m.Comparison(comparisons=[m.ComparisonTarget(operator=m.In())]),
        )
    )
    def replace_not_in_condition(
        self, original_node: cst.UnaryOperation, _
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

        # FIXME: For some reason, new node is discarded when doing nested fixes.
        return cst.Comparison(left=comparison_node.left, comparisons=fixed_comparisons)


__all__ = ["NotInConditionTransformer"]
