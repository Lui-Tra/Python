from constants import operators
from Operator import Operator


class AndOperator(Operator):
    def traverse(self):
        return self.binary_traverse(operators["and"])
