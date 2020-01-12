import libcst as cst
import libcst.matchers as m
from libcst import Tuple


class RemoveParenthesesFromReturn(cst.CSTTransformer):
    @m.call_if_inside(m.Return(value=m.Tuple()))
    @m.leave(m.DoesNotMatch(m.Tuple(lpar=[])))
    def leave_Tuple(self, original_node: "Tuple", updated_node: "Tuple") -> "Tuple":
        return original_node.with_changes(lpar=[], rpar=[])
