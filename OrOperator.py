from constants import operators
from Operator import Operator


class OrOperator(Operator):
    def traverse(self):
        return self.multiple_traverse(operators["or"])
