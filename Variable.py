from Token import Token


class Variable(Token):
    def __init__(self, name, value=True):
        super().__init__([])
        self.name = name
        self.value = value

    def negate(self):
        return Operator([self], operators["not"])

    def traverse(self):
        print(f"{self.name}", end="")

    def simplify(self):
        return self

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        return False