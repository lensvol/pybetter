from abc import ABC

import libcst as cst
from libcst import MetadataWrapper
from typing_extensions import Type

from pybetter.transformers.all_attribute import AllAttributeTransformer
from pybetter.transformers.base import NoqaDetectionVisitor
from pybetter.transformers.boolean_equality import BooleanLiteralEqualityTransformer
from pybetter.transformers.empty_fstring import TrivialFmtStringTransformer
from pybetter.transformers.equals_none import EqualsNoneIsNoneTransformer
from pybetter.transformers.mutable_args import ArgEmptyInitTransformer
from pybetter.transformers.not_in import NotInConditionTransformer
from pybetter.transformers.parenthesized_return import RemoveParenthesesFromReturn


class BaseImprovement(ABC):
    CODE: str
    NAME: str
    DESCRIPTION: str
    TRANSFORMER: Type[cst.CSTTransformer]

    def improve(self, tree: cst.Module):
        noqa_detector = NoqaDetectionVisitor()
        wrapper = MetadataWrapper(tree)

        with noqa_detector.resolve(wrapper):
            wrapper.visit(noqa_detector)
            transformer = self.TRANSFORMER(self.CODE, noqa_detector.get_noqa_lines())
            return wrapper.visit(transformer)


class FixNotInConditionOrder(BaseImprovement):
    NAME = "not_in"
    DESCRIPTION = "Replace 'not A in B' with 'A not in B'"
    CODE = "B001"
    TRANSFORMER = NotInConditionTransformer


class FixMutableDefaultArgs(BaseImprovement):
    NAME = "mutable_defaults"
    DESCRIPTION = "Default values for **kwargs are mutable."
    CODE = "B002"
    TRANSFORMER = ArgEmptyInitTransformer


class FixParenthesesInReturn(BaseImprovement):
    NAME = "parenthesis_return"
    DESCRIPTION = "Remove parentheses from the tuple in 'return' statement."
    CODE = "B003"
    TRANSFORMER = RemoveParenthesesFromReturn


class FixMissingAllAttribute(BaseImprovement):
    NAME = "missing_all"
    DESCRIPTION = "__all__ attribute is missing."
    CODE = "B004"
    TRANSFORMER = AllAttributeTransformer


class FixEqualsNone(BaseImprovement):
    NAME = "equals_none"
    DESCRIPTION = "Replace 'a == None' with 'a is None'."
    CODE = "B005"
    TRANSFORMER = EqualsNoneIsNoneTransformer


class FixBooleanEqualityChecks(BaseImprovement):
    NAME = "false_true_equality"
    DESCRIPTION = "Remove comparisons with either 'False' or 'True'."
    CODE = "B006"
    TRANSFORMER = BooleanLiteralEqualityTransformer


class FixTrivialFmtStringCreation(BaseImprovement):
    NAME = "trivial_fstring"
    DESCRIPTION = "Convert f-strings without expressions into regular strings."
    CODE = "B007"
    TRANSFORMER = TrivialFmtStringTransformer
