import re
from typing import Dict, Set, Optional

import libcst as cst
from libcst.metadata import PositionProvider

NOQA_MARKUP_REGEX = re.compile(r"noqa: ((?:B[0-9]{3},)?(?:B[0-9]{3}))")


class NoqaDetectionVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self):
        self._line_to_code: Dict[int, Set[str]] = {}

        super().__init__()

    def visit_Comment(self, node: cst.Comment) -> Optional[bool]:
        m = re.search(NOQA_MARKUP_REGEX, node.value)
        if m:
            codes = m.group(1)
            comment_position: cst.CodeRange = self.get_metadata(PositionProvider, node)
            self._line_to_code[comment_position.start.line] = set(codes.split(","))

        return True

    def get_noqa_lines(self):
        return self._line_to_code


class NoqaAwareTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, code: str, noqa_lines: Dict[int, Set[str]]):
        self.check_code = code
        self.noqa_lines = noqa_lines
        super().__init__()

    def on_visit(self, node: cst.CSTNode):
        position = self.get_metadata(PositionProvider, node)
        applicable_noqa = self.noqa_lines.get(position.start.line, set())
        if self.check_code in applicable_noqa:
            return False

        return super().on_visit(node)
