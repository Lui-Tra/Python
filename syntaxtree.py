from operator import Operator
from Variable import Variable
from constants import operators

root = Operator([
    Variable("A"),
    Variable("B"),
    Variable("B"),
    Operator([
        Variable("A"),
        Variable("B"),
        Variable("B"),
        Variable("D"),
    ], operators["and"]),
    Variable("C"),
    Variable("E"),
    Variable("E"),
    Variable("C"),
    Variable("C"),
    Operator([
        Operator([
            Variable("E")
        ], operators["not"])
    ], operators["not"])
], operators["and"])

if __name__ == "__main__":
    root.traverse()
    root = root.simplify().simplify()
    print()
    root.traverse()
