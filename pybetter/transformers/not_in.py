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
        self, _, updated_node: cst.UnaryOperation
    ) -> cst.BaseExpression:
        comparison_node: cst.Comparison = cst.ensure_type(
            updated_node.expression, cst.Comparison
        )

        # TODO: Implement support for multiple consecutive 'not ... in B',
        # even if it does not make any sense in practice.
        return cst.Comparison(
            left=comparison_node.left,
            lpar=updated_node.lpar,
            rpar=updated_node.rpar,
            comparisons=[
                comparison_node.comparisons[0].with_changes(operator=cst.NotIn())
            ],
        )


__all__ = ["NotInConditionTransformer"]
