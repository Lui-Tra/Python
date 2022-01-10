from parser import parse

root = parse("ITE(A, B, C)")

if __name__ == "__main__":
    print(root)
    root.simplify()
    print(root)
