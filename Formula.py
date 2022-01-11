from parser import parse
from Variable import Variable


class Formula:
    def __init__(self, root=None):
        if isinstance(root, str):
            root = parse(root)
        self.root = root
        self.variables = {}

    def set_root(self, root):
        self.root = root

    def __create_variable__(self, name):
        if name not in self.variables:
            self.variables[name] = Variable(name)
        return self.variables[name]

    def nnf(self):
        self.root = self.root.nnf()


