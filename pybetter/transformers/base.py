import libcst as cst


class BaseStatementLine(object):
    pass


class NoqaAwareTransformer(cst.CSTTransformer):
    def __init__(self, code):
        self.check_code = code
        super().__init__()

    def on_visit(self, node: cst.If):
        comment_string = None

        if (
            isinstance(node, cst.SimpleStatementLine)
            and node.trailing_whitespace
            and node.trailing_whitespace.comment
        ):
            comment_string = node.trailing_whitespace.comment.value

        if isinstance(node, cst.BaseCompoundStatement) and node.leading_lines:
            for line in node.leading_lines:
                if line.comment:
                    comment_string = line.comment.value
                    break

        if comment_string:
            return f"noqa: {self.check_code}" not in comment_string

        return super().on_visit(node)
