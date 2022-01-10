from abc import ABC

from Token import Token
from Variable import Variable
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
    def __init__(self, *children):
        if isinstance(children[0], list):
            self.children = children[0]
        else:
            self.children = list(children)

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
            return OrOperator(list(map(NotOperator, self.children[0].children))).simplify()
        elif isinstance(self.children[0], OrOperator):
            return AndOperator(list(map(NotOperator, self.children[0].children))).simplify()

        return super().simplify()

    def __str__(self):
        return self.unary_traverse(operators["not"])


class AndOperator(Operator):
    def __str__(self):
        return self.multiple_traverse(operators["and"])


class OrOperator(Operator):
    def __str__(self):
        return self.multiple_traverse(operators["or"])

    def simplify(self):
        to_remove = []
        for i in range(len(self.children)):
            if isinstance(self.children[i], Operator):
                if isinstance(self.children[i], AndOperator):
                    for var in self.children:
                        if isinstance(var, Variable) \
                                and (isinstance(self.children[i], Variable) or var in self.children[i].children):
                            self.children[i] = var
                elif isinstance(self.children[i], OrOperator):
                    self.children.extend(self.children[i].children)
                    to_remove.append(self.children[i])

        for t in to_remove:
            self.children.remove(t)

        for c in self.children:
            while self.children.count(c) > 1:
                self.children.remove(c)

        return super().simplify()


class XorOperator(Operator):
    def simplify(self):
        return AndOperator([
            OrOperator(self.children),
            OrOperator(list(map(NotOperator, self.children)))
        ])

    def __str__(self):
        return self.multiple_traverse(operators["xor"])


class ImplicationOperator(Operator):
    def simplify(self):
        return OrOperator(
            NotOperator(self.children[0]),
            self.children[1]
        )

    def __str__(self):
        return self.multiple_traverse(operators["implication"])


class BiConditionalOperator(Operator):
    def __str__(self):
        return self.multiple_traverse(operators["bi-conditional"])

    def simplify(self):
        return NotOperator(XorOperator(self.children)).simplify()


class ITEOperator(Operator):
    def simplify(self):
        return AndOperator(
            ImplicationOperator(self.children),
            ImplicationOperator(list(map(NotOperator, self.children)))
        )

    def __str__(self):
        return operators["ite"] + "(" + ", ".join(list(map(str, self.children))) + ")"
