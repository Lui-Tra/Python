from Operator import get_operator
from Variable import Variable
from constants import operators

root = get_operator(operators["and"], [
    get_operator(operators["not"], [
        get_operator(operators["or"], [
            Variable("D"),
            Variable("X"),
        ])
    ]),
    Variable("B")
])

if __name__ == "__main__":
    root.simplify()
    print(root)
    #root = root.simplify().simplify()
    #root.traverse()
