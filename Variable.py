from Token import Token
from constants import center


class Variable(Token):
    def __init__(self, name, value=True):
        super().__init__()
        self.name = name
        self.value = value

    def calculate_value(self):
        return self.value

    def get_truth_table_header(self):
        return center(self.name, len(self.name))

    def get_truth_table_entry(self):
        return center(self.value, len(self.name))

    def nnf(self):
        return self

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        return False
