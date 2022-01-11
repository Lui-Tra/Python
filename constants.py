import math

operators = {
    "not": "¬",
    "and": "∧",
    "or": "∨",
    "xor": "⊕",
    "implication": "→",
    "bi-conditional": "↔",
    "ite": "ITE"
}

prefix_operators = ("ITE", )


def center(string, size):
    if isinstance(string, bool):
        if string:
            string = "1"
        elif not string:
            string = "0"
    return string.center(size, " ")
