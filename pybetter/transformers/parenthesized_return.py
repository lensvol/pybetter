import libcst as cst
import libcst.matchers as m


class RemoveParenthesesFromReturn(cst.CSTTransformer):
    def leave_Return(
        self, original_node: cst.Return, updated_node: cst.Return
    ) -> cst.Return:
        if not m.matches(original_node.value, m.Tuple()):
            return original_node

        if not original_node.value.lpar:
            return original_node

        changed_tuple = original_node.value.with_changes(lpar=[], rpar=[])

        return original_node.with_changes(value=changed_tuple)
