from Token import Token


class NotOperator(Token):
    def simplify(self):


        for i in range(len(self.children)):
            self.children[i] = self.children[i].simplify()

        return self

    def traverse(self):
        pass
