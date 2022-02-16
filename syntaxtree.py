from dpll_tree import create_dpll_tree, display_dpll_tree
import parser

if __name__ == "__main__":
    form = parser.parse(" ((w ↔ (y ↔ z)) ↔ (w ∨ (w ∧ y)))")

    form.print_truth_table()
