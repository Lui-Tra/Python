from NotOperator import NotOperator
from Token import Token
from constants import operators


def get_operator(operator_name, children):
    if operator_name == operators["not"]:
        return NotOperator(children)


class Operator(Token):
    def __init__(self, children, operator):
        super().__init__(children)
        self.operator = operator

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

    def traverse(self):
        if self.operator == operators["not"]:
            print(f"{self.operator}", end="")
            self.children[0].traverse()
        else:
            print("(", end="")
            self.children[0].traverse()
            for c in self.children[1:]:
                print("", self.operator, end=" ")
                c.traverse()
            print(")", end="")

    def simplify(self):
        if self.operator == operators["or"] or self.operator == operators["and"]:
            to_remove = []
            for i in range(len(self.children)):
                if isinstance(self.children[i], Operator):
                    if self.operator == operators["or"] and self.children[i].operator == operators["and"] \
                             or self.operator == operators["and"] and self.children[i].operator == operators["or"]:
                        for var in self.children:
                            if isinstance(var, Variable) and var in self.children[i].children:
                                self.children[i] = var
                    elif self.operator == self.children[i].operator:
                        self.children.extend(self.children[i].children)
                        to_remove.append(self.children[i])

            for t in to_remove:
                self.children.remove(t)

            for c in self.children:
                while self.children.count(c) > 1:
                    self.children.remove(c)
        elif self.operator == operators["not"]:
            if isinstance(self.children[0], Operator) and self.children[0].operator == operators["not"]:
                return self.children[0].children[0]

        for i in range(len(self.children)):
            self.children[i] = self.children[i].simplify()

        return self
