from abc import ABC

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
    DESCRIPTION = "Replace 'not ... in ...' with '... not in ...'"
    CODE = "W001"
    TRANSFORMER = NotInConditionTransformer
