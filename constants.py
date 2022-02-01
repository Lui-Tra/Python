from termcolor import colored

operators = {
    "not": "¬",
    "and": "∧",
    "or": "∨",
    "xor": "⊕",
    "implication": "→",
    "bi-conditional": "↔",
    "ite": "ITE",
    "nand": "NAND",
    "nor": "NOR",
}

prefix_operators = ("ITE", )

aliases = {
    "x̄":"¬x",
}

def center(string, size, depth=-1):
    depth_to_color = {
        0: "red",
        1: "yellow",
        2: "magenta",
        3: "blue"
    }

    if isinstance(string, bool):
        if string:
            string = "1"
        elif not string:
            string = "0"
    if 0 <= depth <= 3:
        if string is None:
            string = "?"
        return colored(string.center(size, " "), depth_to_color[depth])
    else:
        return string.center(size, " ")
