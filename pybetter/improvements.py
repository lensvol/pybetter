from abc import ABC

from pybetter.transformers.mutable_args import ArgEmptyInitTransformer
from pybetter.transformers.not_in import NotInConditionTransformer


class BaseImprovement(ABC):
    CODE = None
    NAME = None
    DESCRIPTION = None
    TRANSFORMER = None

    def improve(self, tree):
        assert self.TRANSFORMER, "Transformation should be specified!"

        return tree.visit(self.TRANSFORMER())


class FixNotInConditionOrder(BaseImprovement):
    NAME = "not_in"
    DESCRIPTION = "Replace 'not A in B' with 'A not in B'"
    CODE = "W001"
    TRANSFORMER = NotInConditionTransformer


class FixMutableDefaultArgs(BaseImprovement):
    NAME = "mutable_defaults"
    DESCRIPTION = "Default values for **kwargs are mutable."
    CODE = "W002"
    TRANSFORMER = ArgEmptyInitTransformer
