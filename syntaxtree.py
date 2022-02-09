from dpll_tree import create_dpll_tree, display_dpll_tree
import parser

if __name__ == "__main__":
    form = parser.parse("{{p, ¬w}, {p, y}, {¬p, ¬r, ¬w, y}, {r}, {¬r, w, ¬y}, {w, y}, {¬w, ¬y}}")

    root = create_dpll_tree(form.to_clause_list())

    display_dpll_tree(root, 2)
