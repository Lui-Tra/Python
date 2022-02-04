from Operator import NotOperator
import parser


def copy_clauses(clauses):
    return [set(clause) for clause in clauses]


def get_base_var(var):
    return var.children[0] if isinstance(var, NotOperator) else var


def negate_var(var):
    return var.children[0] if isinstance(var, NotOperator) else NotOperator(var)


def remove_var(clauses, var):
    clauses = [clause for clause in clauses if var not in clause]
    neg_var = negate_var(var)
    for clause in clauses:
        if neg_var in clause:
            clause.remove(neg_var)
    return clauses


def get_olr_var(clauses):
    olr_var = None
    base_olr_var = None
    for clause in clauses:
        if len(clause) == 1:
            var = list(clause)[0]
            base_var = get_base_var(var)
            if base_olr_var is None or base_var.name < base_olr_var.name:
                olr_var = var
                base_olr_var = base_var
    return olr_var


def get_plr_var(clauses):
    variables = {var for clause in clauses for var in clause}
    plr_var_candidates = sorted(
        [var for var in variables if not (var in variables and negate_var(var) in variables)],
        key=lambda var: get_base_var(var).name)
    if len(plr_var_candidates) > 0:
        return plr_var_candidates[0]
    else:
        return None


def get_first_var(clauses):
    return sorted({get_base_var(var) for clause in clauses for var in clause}, key=lambda var: var.name)[0]


class DPLLSolver:
    def __init__(self, clauses):
        self.clauses = clauses

    def __dpll__(self, clauses):
        if len(clauses) == 0:
            return {}
        if any(len(clause) == 0 for clause in clauses):
            return None

        olr_var = get_olr_var(clauses)
        if olr_var is not None:
            olr = self.__dpll__(remove_var(clauses, olr_var))
            return OLRNode(get_base_var(olr_var), not isinstance(olr_var, NotOperator), olr)

        plr_var = get_plr_var(clauses)
        if plr_var is not None:
            plr = self.__dpll__(remove_var(clauses, plr_var))
            return PLRNode(get_base_var(plr_var), not isinstance(olr_var, NotOperator), plr)

        var = get_first_var(clauses)

        ast = self.__dpll__(remove_var(copy_clauses(clauses), var))
        asf = self.__dpll__(remove_var(copy_clauses(clauses), NotOperator(var)))
        return DecisionNode(var.name, ast, asf)


class DPLLNode:
    pass


class OLRNode(DPLLNode):
    def __init__(self, name, assignment, nextNode):
        self.name = name
        self.assignment = assignment
        self.nextNode = nextNode

class PLRNode(DPLLNode):
    def __init__(self, name, assignment, nextNode):
        self.name = name
        self.assignment = assignment
        self.nextNode = nextNode


class DecisionNode(DPLLNode):
    def __init__(self, name, trueNode, falseNode):
        self.trueNode = trueNode
        self.falseNode = falseNode


if __name__ == "__main__":
    form = parser.parse("{{q,r,¬x},{¬q,r},{¬q,¬x},{r,x},{¬r,x},{¬r,¬x}}")
    print(form)
    cl = form.to_clause_list_f()
    dpll = DPLLSolver(cl)
    print(dpll.__dpll__(cl))
