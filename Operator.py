from abc import ABC

from Token import Token
from constants import operators


operator_registry = {}


def get_operator(operator_name, children):
    return operator_registry[operator_name](children)


def register_operator(operator_name, cls):
    operator_registry[operator_name] = cls


class Operator(Token, ABC):
    def __init__(self, children):
        self.children = children

    def negate(self):
        if self.operator == operators["not"]:
            return self.children[0]
        elif self.operator == operators["and"]:
            self.operator = operators["or"]
        elif self.operator == operators["or"]:
            self.operator = operators["and"]
        elif self.operator == operators["implication"]:
            tmp = self.children[0]
            self.children[0] = self.children[1]
            self.children[1] = tmp

        for i in range(len(self.children)):
            self.children[i] = self.children[i].negate()
        return self

    def unary_traverse(self, operator):
        return operator + self.children[0].traverse()

    def multiple_traverse(self, operator):
        string = " ("

        return " (" + self.children[0].traverse() + operator + self.children[1].traverse() + ") "

    def simplify(self):
        for i in range(len(self.children)):
            self.children[i] = self.children[i].simplify()

        return self
