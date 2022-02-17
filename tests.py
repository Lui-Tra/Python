import parser

if __name__ == "__main__":
    form = parser.parse("(p ∧ ((q ∧ (r ∨ (¬r ∧ x ∧ ¬z))) ∨ (¬q ∧ ((r ∧ x ∧ z) ∨ (¬r ∧ (x ∨ (¬x ∧ ¬y ∧ ¬z)))))))∨(¬p ∧ ((q ∧ ((r ∧ x) ∨ (¬r ∧ z))) ∨ (¬q ∧ ((r ∧ (x ∨ (¬x ∧ (y ∨ (¬y ∧ z))))) ∨ (¬r ∧ x ∧ z)))))")

    form.kv(3, order="pqrxyz", color=(155, 124, 220))
