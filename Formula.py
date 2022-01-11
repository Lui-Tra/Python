import math


def center(string, size):
    return " " * math.floor(size / 2) + string + " " * math.ceil(size / 2)


class Formula:
    def __init__(self, root=None, variables=None):
        if variables is None:
            variables = {}
        self.root = root
        self.variables = variables

    def print_truth_table(self):
        vars = list(self.variables.values())
        for var in vars:
            var.value = False

        self.print_table_header()

        self.root.calculate_value()
        self.print_values()

        for i in range(2 ** len(vars) - 1):

            index = -1
            while index < 0 and vars[index].value:
                vars[index].value = False
                index -= 1
            if index <= 0:
                vars[index].value = True

            self.root.calculate_value()
            self.print_values()

    def print_table_header(self):
        for name in self.variables:
            print(name, end=" | ")
        print(str(self))

    def print_values(self):
        for name, var in self.variables.items():
            val = center(str(int(var.value)), len(name) - 1)
            print(val, end=" | ")
        print(center(str(int(self.root.value)), len(str(self.root)) / 2))

    def nnf(self):
        self.root = self.root.nnf()
        return self

    def __str__(self):
        return str(self.root)
