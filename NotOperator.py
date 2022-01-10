from constants import operators
from Operator import Operator
from Operator import register_operator


class NotOperator(Operator):
    def simplify(self):
        if isinstance(self.children[0], NotOperator):
            return self.children[0].children[0]

        return super().simplify()

    def traverse(self):
        return self.unary_traverse(operators["not"])


register_operator("not", NotOperator)


"""
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
"""
