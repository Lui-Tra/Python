from abc import ABC

from Token import Token
from constants import operators


def get_operator(operator_name, children):
    return {
        operators["not"]: NotOperator,
        operators["and"]: AndOperator,
        operators["or"]: OrOperator,
        operators["xor"]: XorOperator,
        operators["implication"]: ImplicationOperator,
        operators["bi-conditional"]: BiConditionalOperator,
        operators["ite"]: ITEOperator,
    }[operator_name](children)


class Operator(Token, ABC):
    def __init__(self, children):
        self.children = children

    def unary_traverse(self, operator):
        return operator + str(self.children[0])

    def multiple_traverse(self, operator):
        return "(" + (" " + operator + " ").join(map(str, self.children)) + ")"

    def simplify(self):
        for i in range(len(self.children)):
            self.children[i] = self.children[i].simplify()

        return self


class NotOperator(Operator):
    def simplify(self):
        super().simplify()

        if isinstance(self.children[0], NotOperator):
            return self.children[0].children[0].simplify()
        if isinstance(self.children[0], AndOperator):
            return OrOperator(list(map(lambda it: NotOperator([it]), self.children[0].children))).simplify()
        elif isinstance(self.children[0], OrOperator):
            return AndOperator(list(map(lambda it: NotOperator([it]), self.children[0].children))).simplify()

        return super().simplify()

    def __str__(self):
        return self.unary_traverse(operators["not"])


class AndOperator(Operator):
    def __str__(self):
        return self.multiple_traverse(operators["and"])


class OrOperator(Operator):
    def __str__(self):
        return self.multiple_traverse(operators["or"])


class XorOperator(Operator):
    def simplify(self):
        return AndOperator([
            OrOperator([
                self.children[0],
                self.children[1]
            ]),
            OrOperator([
                NotOperator([self.children[0]]),
                NotOperator([self.children[1]])
            ])
        ])

    def __str__(self):
        return self.multiple_traverse(operators["xor"])


class ImplicationOperator(Operator):
    def simplify(self):
        return OrOperator([
            NotOperator([self.children[0]]),
            self.children[1]
        ])

    def __str__(self):
        return self.multiple_traverse(operators["implication"])


class BiConditionalOperator(Operator):
    def __str__(self):
        return self.multiple_traverse(operators["bi-conditional"])

    def simplify(self):
        return NotOperator([XorOperator(self.children)]).simplify()


class ITEOperator(Operator):
    def __str__(self):
        return operators["ite"] + "(" + ", ".join(map(str, self.children)) + ")"
