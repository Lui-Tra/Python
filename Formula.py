from parser import parse


class Formula:
    def __init__(self, root):
        if isinstance(root, str):
            self.root = parse(root)
        self.root = root

    def nnf(self):
        self.root = self.root.nnf()

