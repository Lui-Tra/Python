from parser import parse

root = parse("(B ∨ B ⊕ A ∨ A ∨ ((B ∨ B ∨ A ∨ A ∨ (B ∧ F)) ∧ C))")

if __name__ == "__main__":
    print(root)
    root.simplify()
    print(root)
