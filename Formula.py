class Formula:
    def __init__(self, root=None, variables=None):
        if variables is None:
            variables = {}
        self.root = root
        self.variables = variables

    def print_truth_table(self):
        self.root.calculate_value()

    def nnf(self):
        self.root = self.root.nnf()
        return self

    def __str__(self):
        return str(self.root)
