class Formula:
    def __init__(self, root=None, variables={}):
        self.root = root
        self.variables = variables

    def nnf(self):
        self.root = self.root.nnf()


