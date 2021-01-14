import libcst as cst

from pybetter.transformers.base import NoqaAwareTransformer


class TrivialFmtStringTransformer(NoqaAwareTransformer):
    def leave_FormattedString(
        self, original_node: cst.FormattedString, updated_node: cst.FormattedString
    ) -> cst.BaseExpression:
        if len(updated_node.parts) == 1 and isinstance(
            updated_node.parts[0], cst.FormattedStringText
        ):
            # We need to explicitly specify quotation marks here, otherwise we
            # will fail SimpleString's internal validation. This is due to
            # SimpleString._get_prefix treating everything before quotation
            # marks as a prefix. (sic!)
            return cst.SimpleString(
                value=f'{updated_node.start.replace("f", "")}{updated_node.parts[0].value}{updated_node.end}'
            )

        return original_node


__all__ = ["TrivialFmtStringTransformer"]
