from itertools import takewhile, dropwhile
from typing import Union, Dict, List, Optional, Tuple

import libcst as cst
from libcst import matchers as m
from libcst.helpers import parse_template_statement

from pybetter.transformers.base import NoqaAwareTransformer

DEFAULT_INIT_TEMPLATE = """if {arg} is None:
    {arg} = {init}
"""
# If you do not explicitly set `indent` to False, then even empty line
# will contain at least one indent worth of whitespaces.
EMPTY_LINE = cst.EmptyLine(indent=False, newline=cst.Newline())


def is_docstring(node):
    return m.matches(node, m.SimpleStatementLine(body=[m.Expr(value=m.SimpleString())]))


class ArgEmptyInitTransformer(NoqaAwareTransformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_config = None

    def visit_Module(self, node: cst.Module) -> Optional[bool]:
        self.module_config = node.config_for_parsing
        return True

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> Union[cst.BaseStatement, cst.RemovalSentinel]:
        modified_defaults: List = []
        mutable_args: List[Tuple[cst.Name, Union[cst.List, cst.Dict]]] = []

        for param in updated_node.params.params:
            if not m.matches(param, m.Param(default=m.OneOf(m.List(), m.Dict()))):
                modified_defaults.append(param)
                continue

            # This line here is just for type checkers peace of mind,
            # since it cannot reason about variables from matchers result.
            if not isinstance(param.default, (cst.List, cst.Dict)):
                continue

            mutable_args.append((param.name, param.default))
            modified_defaults.append(param.with_changes(default=cst.Name("None"),))

        if not mutable_args:
            return original_node

        modified_params: cst.Parameters = updated_node.params.with_changes(
            params=modified_defaults
        )

        initializations: List[
            Union[cst.SimpleStatementLine, cst.BaseCompoundStatement]
        ] = [
            # We use generation by template here since construction of the
            # resulting 'if' can be burdensome due to many nested objects
            # involved. Additional line is attached so that we may control
            # exact spacing between generated statements.
            parse_template_statement(
                DEFAULT_INIT_TEMPLATE, config=self.module_config, arg=arg, init=init
            ).with_changes(leading_lines=[EMPTY_LINE])
            for arg, init in mutable_args
        ]

        # Docstring should always go right after the function definition,
        # so we take special care to insert our initializations after the
        # last docstring found.
        docstrings = takewhile(is_docstring, updated_node.body.body)
        function_code = dropwhile(is_docstring, updated_node.body.body)

        # It is not possible to insert empty line after the statement line,
        # because whitespace is owned by the next statement after it.
        stmt_with_empty_line = next(function_code).with_changes(
            leading_lines=[EMPTY_LINE]
        )

        modified_body = (
            *docstrings,
            *initializations,
            stmt_with_empty_line,
            *function_code,
        )

        return updated_node.with_changes(
            params=modified_params,
            body=updated_node.body.with_changes(body=modified_body),
        )


__all__ = ["ArgEmptyInitTransformer"]
