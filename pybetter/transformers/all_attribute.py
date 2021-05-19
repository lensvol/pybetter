from typing import Optional, Union

import libcst as cst
from libcst.metadata import ScopeProvider, GlobalScope
import libcst.matchers as m

from pybetter.transformers.base import NoqaAwareTransformer


class AllAttributeTransformer(NoqaAwareTransformer):
    METADATA_DEPENDENCIES = (ScopeProvider,)  # type: ignore

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.names = []
        self.already_exists = False

    def process_node(
        self,
        node: Union[cst.FunctionDef, cst.ClassDef, cst.BaseAssignTargetExpression],
        name: str,
    ) -> None:
        scope = self.get_metadata(ScopeProvider, node)
        if isinstance(scope, GlobalScope) and not name.startswith("_"):
            self.names.append(name)

    def visit_AssignTarget(self, node: cst.AssignTarget) -> Optional[bool]:
        if m.matches(node, m.AssignTarget(target=m.Name())):
            target = cst.ensure_type(node.target, cst.Name)
            if target.value == "__all__":
                self.already_exists = True
            else:
                self.process_node(node.target, target.value)
        return None

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        self.process_node(node, node.name.value)
        return None

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        self.process_node(node, node.name.value)
        return None

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        if not self.names or self.already_exists:
            return original_node

        modified_body = list(original_node.body)
        config = original_node.config_for_parsing

        list_of_names = f",{config.default_newline}{config.default_indent}".join(
            [repr(name) for name in sorted(dict.fromkeys(self.names))]
        )

        all_names = cst.parse_statement(
            f"""

__all__ = [
{config.default_indent}{list_of_names}
]
        """,
            config=original_node.config_for_parsing,
        )

        modified_body.append(all_names)
        return updated_node.with_changes(body=modified_body)


__all__ = ["AllAttributeTransformer"]
