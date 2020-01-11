import libcst as cst
import libcst.matchers as m
from libcst import BaseExpression, UnaryOperation, Comparison, NotIn


class NotInConditionTransformer(cst.CSTTransformer):
    @m.call_if_inside(
        m.UnaryOperation(
            operator=m.Not(),
            expression=m.Comparison(comparisons=[m.ComparisonTarget(operator=m.In())]),
        )
    )
    def leave_UnaryOperation(
        self, original_node: "UnaryOperation", updated_node: "UnaryOperation"
    ) -> "BaseExpression":
        fixed_comparisons = []

        for target in original_node.expression.comparisons:
            if m.matches(target, m.ComparisonTarget(operator=m.In())):
                fixed_comparisons.append(target.with_changes(operator=NotIn()))
            else:
                fixed_comparisons.append(target)

        return Comparison(
            left=original_node.expression.left, comparisons=fixed_comparisons
        )
