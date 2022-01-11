from Token import Token


class Variable(Token):
    def __init__(self, name, value=True):
        super().__init__()
        self.name = name
        self.value = value

    def calculate_value(self):
        self.current_value = self.value
        return self.current_value

    def nnf(self):
        return self

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        return False
