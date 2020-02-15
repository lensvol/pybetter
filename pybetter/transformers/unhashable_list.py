from typing import List, Sequence, Union

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


class UnhashableListTransformer(NoqaAwareTransformer):
    @m.call_if_inside(
        m.Call(
            func=m.OneOf(m.Name(value="set"), m.Name(value="frozenset")),
            args=[m.Arg(value=m.OneOf(m.List(), m.Tuple(), m.Set()))],
        )
        | m.Set()  # noqa: W503
    )
    @m.leave(m.List() | m.Set() | m.Tuple())
    def convert_list_arg(
        self, _, updated_node: Union[cst.Set, cst.List, cst.Tuple]
    ) -> cst.BaseExpression:
        modified_elements = convert_lists_to_tuples(updated_node.elements)
        return updated_node.with_changes(elements=modified_elements)


__all__ = ["UnhashableListTransformer"]
