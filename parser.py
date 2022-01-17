import re

from Formula import Formula
from constants import operators
from constants import prefix_operators
from Operator import get_operator
from Variable import Variable, TRUE, FALSE
import Variable as Variables


class Parser:
    def __init__(self):
        self.formula = None
        self.variables = {}

    def __create_variable__(self, name):
        if name not in self.variables:
            if name == "false":
                self.variables[name] = Variables.FALSE
            elif name == "true":
                self.variables[name] = Variables.TRUE
            else:
                self.variables[name] = Variable(name)
        return self.variables[name]

    def parse(self, formula):
        formula = self.preproc_names(formula)
        formula = self.preproc_prefix(formula)
        return Formula(self.__parse__(formula), self.variables)

    @classmethod
    def remove_parenthesis(cls, token):
        indent_level = 1
        index = 1
        remove = True
        if len(token) > 2 and token[0] == "(" and token[-1] == ")":
            while index < len(token) - 1:
                if token[index] == "(":
                    indent_level += 1
                elif token[index] == ")":
                    indent_level -= 1
                if indent_level <= 0:
                    remove = False
                index += 1
        else:
            remove = False
        if remove:
            return token[1:-1]
        else:
            return token

    @classmethod
    def find_operator(cls, formula, index):
        char = formula[index]
        if char in operators.values():
            return char
        else:
            for operator in operators.values():
                if index + (len(operator) - 1) <= len(formula):
                    if operator.startswith(char):
                        if formula[index:index + len(operator)] == operator:
                            return operator
            return None

    @classmethod
    def preproc_names(cls, formula):
        sorted_operators = list(operators.items())
        sorted_operators.sort(key=lambda item: len(item[0]), reverse=True)
        for name, symbol in sorted_operators:
            formula = formula.replace(name, symbol)
        return formula

    @classmethod
    def preproc_prefix(cls, formula):
        index = 0
        new_formula = ""
        while index < len(formula):
            char = formula[index]
            for operator in prefix_operators:
                if operator.startswith(char) and formula[index:index + len(operator)] == operator:
                    index += len(operator)
                    char = formula[index]
                    if char != "(":
                        raise SyntaxError
                    indent_level = 1
                    index += 1
                    tokens = []
                    current_token = ""
                    while indent_level > 0 and index < len(formula):
                        char = formula[index]
                        if char == "(":
                            current_token += char
                            indent_level += 1
                        elif char == ")":
                            if indent_level > 1:
                                current_token += char
                            indent_level -= 1
                        elif indent_level == 1 and char == ",":
                            tokens.append(current_token)
                            current_token = ""
                        else:
                            current_token += char
                        index += 1
                    tokens.append(current_token)
                    if indent_level > 0:
                        raise SyntaxError
                    tokens = [cls.preproc_prefix(token) for token in tokens]
                    new_formula += "(" + (" " + operator + " ").join(tokens) + ")"
                    break
            else:
                new_formula += char
            index += 1
        return new_formula

    def __parse__(self, formula):
        formula = re.sub(r"\s", "", formula)
        formula = self.remove_parenthesis(formula)

        index = 0
        indent_level = 0
        min_binding_priority = -1
        while index < len(formula):
            char = formula[index]
            if char == "(":
                indent_level += 1
            elif char == ")":
                indent_level -= 1
            elif indent_level == 0:
                operator = self.find_operator(formula, index)
                if operator is not None:
                    binding_priority = list(operators.values()).index(operator)
                    if binding_priority > min_binding_priority:
                        min_binding_priority = binding_priority
            index += 1
        if indent_level != 0:
            raise ValueError("invalid")

        index = 0
        indent_level = 0
        current_token = ""
        tokens = []
        seperator = list(operators.values())[min_binding_priority]
        while index < len(formula):
            char = formula[index]
            if char == "(":
                current_token += char
                indent_level += 1
            elif char == ")":
                current_token += char
                indent_level -= 1
            elif indent_level == 0 and self.find_operator(formula, index) == seperator:
                tokens.append(self.remove_parenthesis(current_token))
                current_token = ""
                index += len(seperator) - 1
            else:
                current_token += char
            index += 1
        tokens.append(self.remove_parenthesis(current_token))

        if len(tokens) == 1:
            return self.__create_variable__(tokens[0])
        else:
            if seperator == "¬":
                op = get_operator(seperator, [self.__parse__(tokens[-1])])
                for i in range(len(tokens) - 2):
                    op = get_operator(seperator, [op])
                return op
            else:
                return get_operator(seperator, [self.__parse__(token) for token in tokens])


def parse(formula):
    return Parser().parse(formula)


if __name__ == "__main__":
    formula = "a xor b xor c xor d xor e xor f"

    root = parse(formula)
    root.kv()
