from parser import parse

root = parse("(¬(D → X) ∧ B)")

if __name__ == "__main__":
    print(root)
    root.simplify()
    print(root)
