import libcst as cst
import libcst.matchers as m
from libcst.metadata import PositionProvider

from pybetter.transformers.base import NoqaAwareTransformer


class RemoveParenthesesFromReturn(NoqaAwareTransformer):
    def leave_Return(
        self, original_node: cst.Return, updated_node: cst.Return
    ) -> cst.Return:
        if updated_node.value is None:
            return original_node

        if not m.matches(updated_node.value, m.Tuple()):
            return original_node

        if not updated_node.value.lpar:
            return original_node

        # We get position of the `original_node`, since `updated_node` is
        # by definition different and was not processed by metadata provider.
        position: cst.CodeRange = self.get_metadata(PositionProvider, original_node)

        # Removing parentheses which are used to enable multi-line expression
        # will lead to invalid code, so we do nothing.
        if position.start.line != position.end.line:
            return original_node

        changed_tuple: cst.Return = updated_node.value.with_changes(lpar=[], rpar=[])

        return updated_node.with_changes(value=changed_tuple)
