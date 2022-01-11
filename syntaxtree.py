from parser import parse

root = parse("ITE(A, B, C)")
operators = {
    "not": "¬",
    "and": "∧",
    "or": "∨",
    "xor": "⊕",
    "implication": "→",
    "bi-conditional": "↔",
    "ite": "ITE"
}
if __name__ == "__main__":
    print(root)
    root = root.nnf()
    print(root)
