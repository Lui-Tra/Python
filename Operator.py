from abc import ABC

from Token import Token
from Variable import Variable
from constants import operators, center


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
        super().__init__()
        if isinstance(children[0], list):
            self.children = children[0]
        else:
            self.children = list(children)

    def unary_traverse(self, operator):
        return operator + str(self.children[0])

    def multiple_traverse(self, operator):
        return "(" + (" " + operator + " ").join(map(str, self.children)) + ")"

    def get_truth_table_entry(self, depth):
        res = "("
        op_str = center(self.value, 3, depth)
        for child in self.children:
            res += child.get_truth_table_entry(depth + 1)
            res += op_str
        res = res[:-len(op_str)]
        res += ")"
        return res

    def nnf(self):
        for i in range(len(self.children)):
            self.children[i] = self.children[i].nnf()

        return self

    def clone(self):
        return self.__class__([child.clone for child in self.children])


class AndOrOperator(Operator, ABC):
    def basic_simplify(self, my_class, other_class):
        super().nnf()

        to_remove = []
        for i in range(len(self.children)):
            if isinstance(self.children[i], Operator):
                if isinstance(self.children[i], other_class):
                    for var in self.children:
                        if isinstance(var, Variable) \
                                and (isinstance(self.children[i], Variable) or var in self.children[i].children):
                            self.children[i] = var
                elif isinstance(self.children[i], my_class):
                    self.children.extend(self.children[i].children)
                    to_remove.append(self.children[i])

        for t in to_remove:
            self.children.remove(t)

        for c in self.children:
            while self.children.count(c) > 1:
                self.children.remove(c)

        to_remove = []
        for child in self.children:
            if NotOperator(child) in self.children:
                to_remove.append(child)

        for t in to_remove:
            self.children.remove(t)
            self.children.remove(NotOperator(t))
            if my_class == AndOperator:
                self.children.append(Variable("false", False))
            else:
                self.children.append(Variable("true", True))

        return super().nnf()


class NotOperator(Operator):
    def calculate_value(self):
        self.value = not self.children[0].calculate_value()
        return self.value

    def get_truth_table_header(self, depth):
        return center(operators["not"], 2, depth) + self.children[0].get_truth_table_header(depth + 1)

    def get_truth_table_entry(self, depth):
        return center(self.value, 2, depth) + self.children[0].get_truth_table_entry(depth + 1)

    def nnf(self):
        super().nnf()

        if isinstance(self.children[0], NotOperator):
            return self.children[0].children[0].nnf()
        elif isinstance(self.children[0], AndOperator):
            return OrOperator(list(map(NotOperator, self.children[0].children))).nnf()
        elif isinstance(self.children[0], OrOperator):
            return AndOperator(list(map(NotOperator, self.children[0].children))).nnf()
        elif isinstance(self.children[0], Variable) and self.children[0] == Variable("true", True):
            return Variable("false", False)
        elif isinstance(self.children[0], Variable) and self.children[0] == Variable("false", False):
            return Variable("true", True)

        return super().nnf()

    def __str__(self):
        return self.unary_traverse(operators["not"])

    def __eq__(self, other):
        if isinstance(other, NotOperator):
            return self.children == other.children
        return False


class AndOperator(AndOrOperator):
    def calculate_value(self):
        self.value = True
        for c in self.children:
            if not c.calculate_value():
                self.value = False
        return self.value

    def get_truth_table_header(self, depth):
        res = "("
        op_str = center(operators["and"], 3, depth)
        for child in self.children:
            res += child.get_truth_table_header(depth + 1)
            res += op_str
        res = res[:-len(op_str)]
        res += ")"
        return res

    def nnf(self):
        super().basic_simplify(AndOperator, OrOperator)

        if Variable("false", False) in self.children:
            return Variable("false", False)
        elif Variable("true", True) in self.children:
            self.children.remove(Variable("true", True))

        if len(self.children) == 1:
            return self.children[0].nnf()

        return super().nnf()

    def __str__(self):
        return self.multiple_traverse(operators["and"])


class OrOperator(AndOrOperator):
    def calculate_value(self):
        self.value = False
        for c in self.children:
            if c.calculate_value():
                self.value = True
        return self.value

    def get_truth_table_header(self, depth):
        res = "("
        op_str = center(operators["or"], 3, depth)
        for child in self.children:
            res += child.get_truth_table_header(depth + 1)
            res += op_str
        res = res[:-len(op_str)]
        res += ")"
        return res

    def nnf(self):
        super().basic_simplify(OrOperator, AndOperator)

        if Variable("true", True) in self.children:
            return Variable("true", True)
        elif Variable("false", False) in self.children:
            self.children.remove(Variable("false", False))

        if len(self.children) == 1:
            return self.children[0].nnf()

        return super().nnf()

    def __str__(self):
        return self.multiple_traverse(operators["or"])


class XorOperator(Operator):
    def calculate_value(self):
        a = self.children[0].calculate_value()
        b = self.children[1].calculate_value()
        self.value = (a and not b) or (not a and b)
        return self.value

    def get_truth_table_header(self, depth):
        res = "("
        op_str = center(operators["xor"], 3, depth)
        for child in self.children:
            res += child.get_truth_table_header(depth + 1)
            res += op_str
        res = res[:-len(op_str)]
        res += ")"
        return res

    def nnf(self):
        super().nnf()

        return AndOperator([
            OrOperator(self.children),
            OrOperator(list(map(NotOperator, self.children)))
        ]).nnf()

    def __str__(self):
        return self.multiple_traverse(operators["xor"])


class ImplicationOperator(Operator):
    def calculate_value(self):
        a = self.children[0].calculate_value()
        b = self.children[1].calculate_value()
        self.value = not a or b
        return self.value

    def get_truth_table_header(self, depth):
        res = "("
        for child in self.children:
            res += child.get_truth_table_header(depth + 1)
            res += center(operators["implication"], 3, depth)
        res = res[:-3]
        res += ")"
        return res

    def nnf(self):
        super().nnf()

        return OrOperator(
            NotOperator(self.children[0]),
            self.children[1]
        ).nnf()

    def __str__(self):
        return self.multiple_traverse(operators["implication"])


class BiConditionalOperator(Operator):
    def calculate_value(self):
        a = self.children[0].calculate_value()
        b = self.children[1].calculate_value()
        self.value = (a and b) or (not a and not b)
        return self.value

    def get_truth_table_header(self, depth):
        res = "("
        op_str = center(operators["bi-conditional"], 3, depth)
        for child in self.children:
            res += child.get_truth_table_header(depth + 1)
            res += op_str
        res = res[:-len(op_str)]
        res += ")"
        return res

    def nnf(self):
        super().nnf()

        return NotOperator(XorOperator(self.children)).nnf()

    def __str__(self):
        return self.multiple_traverse(operators["bi-conditional"])


class ITEOperator(Operator):
    def calculate_value(self):
        a = self.children[0].calculate_value()
        b = self.children[1].calculate_value()
        c = self.children[2].calculate_value()
        self.value = (not a or b) and (a or c)
        return self.value

    def get_truth_table_header(self, depth):
        res = center("ITE", 3, depth) + "("
        for child in self.children:
            res += child.get_truth_table_header(depth + 1)
            res += ", "
        res = res[:-2]
        res += ")"
        return res

    def get_truth_table_entry(self, depth):
        res = center(self.value, 3, depth) + "("
        for child in self.children:
            res += child.get_truth_table_entry(depth + 1)
            res += ", "
        res = res[:-2]
        res += ")"
        return res

    def nnf(self):
        super().nnf()

        return AndOperator(
            ImplicationOperator(self.children[0], self.children[1]),
            ImplicationOperator(NotOperator(self.children[0]), self.children[2])
        ).nnf()

    def __str__(self):
        return operators["ite"] + "(" + ", ".join(list(map(str, self.children))) + ")"

# TODO: nur nand oder nor
# TODO: kv diagramm (pygame oder tkinter?)
# TODO: gueltigkeit, wahr oder falsch
