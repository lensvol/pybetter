from typing import List, Sequence

import libcst as cst
from libcst import matchers as m

from pybetter.transformers.base import NoqaAwareTransformer


def convert_lists_to_tuples(
    elements: Sequence[cst.BaseElement],
) -> List[cst.BaseElement]:
    result: List[cst.BaseElement] = []

    for element in elements:
        if m.matches(element, m.Element(value=m.List())):
            unhashable_list: cst.List = cst.ensure_type(element.value, cst.List)
            result.append(
                element.with_changes(
                    value=cst.Tuple(
                        elements=convert_lists_to_tuples(unhashable_list.elements)
                    )
                )
            )
        else:
            result.append(element)

    return result


class UnhashableListTransformer(NoqaAwareTransformer, m.MatcherDecoratableTransformer):
    def leave_Set(
        self, original_node: cst.Set, updated_node: cst.Set
    ) -> cst.BaseExpression:

        return updated_node.with_changes(
            elements=convert_lists_to_tuples(updated_node.elements)
        )

    @m.call_if_inside(
        m.Call(
            func=m.OneOf(m.Name(value="set"), m.Name(value="frozenset")),
            args=[m.Arg(value=m.OneOf(m.List(), m.Tuple(), m.Set()))],
        )
    )
    def leave_Call(
        self, original_node: cst.Call, updated_node: cst.Call
    ) -> cst.BaseExpression:
        modified_elements = convert_lists_to_tuples(updated_node.args[0].value.elements)  # type: ignore
        return updated_node.with_deep_changes(
            updated_node.args[0].value, elements=modified_elements
        )
