import re
from abc import ABCMeta
from typing import Dict, Optional, FrozenSet

import libcst as cst
from libcst.matchers import MatcherDecoratableTransformer
from libcst.metadata import PositionProvider

NOQA_MARKUP_REGEX = re.compile(r"noqa(?:: ((?:B[0-9]{3},)+(?:B[0-9]{3})|(B[0-9]{3})))?")
NOQA_CATCHALL: str = "B999"

NoqaLineMapping = Dict[int, FrozenSet[str]]


class NoqaDetectionVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self):
        self._line_to_code: NoqaLineMapping = {}

        super().__init__()

    def visit_Comment(self, node: cst.Comment) -> Optional[bool]:
        m = re.search(NOQA_MARKUP_REGEX, node.value)
        if m:
            codes = m.group(1)
            position: cst.metadata.CodeRange = self.get_metadata(PositionProvider, node)
            if codes:
                self._line_to_code[position.start.line] = frozenset(codes.split(","))
            else:
                self._line_to_code[position.start.line] = frozenset({NOQA_CATCHALL})

        return True

    def get_noqa_lines(self) -> NoqaLineMapping:
        return self._line_to_code


class PositionProviderEnsuranceMetaclass(ABCMeta):
    def __new__(cls, name, bases, attrs):
        providers = attrs.get("METADATA_DEPENDENCIES", ())
        if PositionProvider not in providers:
            attrs["METADATA_DEPENDENCIES"] = (PositionProvider,) + providers

        return super().__new__(cls, name, bases, attrs)


class NoqaAwareTransformer(
    MatcherDecoratableTransformer, metaclass=PositionProviderEnsuranceMetaclass
):
    METADATA_DEPENDENCIES = (PositionProvider,)  # type: ignore

    def __init__(self, code: str, noqa_lines: NoqaLineMapping):
        self.check_code: str = code
        self.noqa_lines: NoqaLineMapping = noqa_lines
        super().__init__()

    def on_visit(self, node: cst.CSTNode):
        position: cst.metadata.CodeRange = self.get_metadata(PositionProvider, node)
        applicable_noqa: FrozenSet[str] = self.noqa_lines.get(
            position.start.line, frozenset()
        )

        if self.check_code in applicable_noqa or NOQA_CATCHALL in applicable_noqa:
            return False

        return super().on_visit(node)


__all__ = ["NoqaAwareTransformer", "NoqaDetectionVisitor", "NoqaLineMapping"]
