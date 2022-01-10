from parser import parse

root = parse("A ∧ true")

if __name__ == "__main__":
    print(root)
    root = root.simplify()
    print(root)
