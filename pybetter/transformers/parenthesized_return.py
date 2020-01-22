import libcst as cst
import libcst.matchers as m

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

        changed_tuple = updated_node.value.with_changes(lpar=[], rpar=[])

        return updated_node.with_changes(value=changed_tuple)
