from Operator import NotOperator, AndOperator, OrOperator
from constants import center


class Formula:
    def __init__(self, root=None, variables=None):
        if variables is None:
            variables = {}
        self.root = root
        self.variables = variables

    def print_truth_table(self):
        variables = list(self.variables.values())
        for var in variables:
            var.value = False

        self.print_table_header()

        self.root.calculate_value()
        self.print_values()

        for i in range(2 ** len(variables) - 1):
            index = -1
            while index < 0 and variables[index].value:
                variables[index].value = False
                index -= 1
            if index <= 0:
                variables[index].value = True

            self.root.calculate_value()
            self.print_values()

    def print_table_header(self):
        for name in self.variables:
            print(name, end=" | ")
        print(self.root.get_truth_table_header(0))

    def print_values(self):
        for name, var in self.variables.items():
            val = center(str(int(var.value)), len(name))
            print(val, end=" | ")
        print(self.root.get_truth_table_entry(0))

    def nnf(self):
        self.root = self.root.nnf()
        return self

    def get_values(self):
        return {name: var.value for name, var in self.variables.items()}

    def get_truth_table(self):
        variables = list(self.variables.values())
        for var in variables:
            var.value = False
        yield self.get_values(), self.root.calculate_value()
        for i in range(2 ** len(variables) - 1):

            index = -1
            while index < 0 and variables[index].value:
                variables[index].value = False
                index -= 1
            if index <= 0:
                variables[index].value = True
            yield self.get_values(), self.root.calculate_value()

    def dnf(self):
        truth_table = self.get_truth_table()
        terms = [term for term, val in truth_table if val]
        new_terms = []
        for term in terms:
            children = []
            for name, val in term.items():
                if val:
                    children.append(self.variables[name])
                else:
                    children.append(NotOperator([self.variables[name]]))
            new_terms.append(AndOperator(children))
        if len(new_terms) == 1:
            self.root = new_terms[0]
        else:
            self.root = OrOperator(new_terms)
        return self

    def knf(self):
        truth_table = self.get_truth_table()
        terms = [term for term, val in truth_table if not val]
        new_terms = []
        for term in terms:
            children = []
            for name, val in term.items():
                if not val:
                    children.append(self.variables[name])
                else:
                    children.append(NotOperator([self.variables[name]]))
            new_terms.append(OrOperator(children))
        if len(new_terms) == 1:
            self.root = new_terms[0]
        else:
            self.root = AndOperator(new_terms)
        return self

    def __str__(self):
        return str(self.root)
