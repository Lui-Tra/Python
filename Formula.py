import kv_generator
from Operator import NotOperator, AndOperator, OrOperator
from Variable import Variable
from constants import center
from kv_generator import generate_kv, render_kv_diagramm


class Formula:
    def __init__(self, root=None, variables=None):
        if variables is None:
            variables = {}
        self.root = root
        self.variables = variables

    def print_truth_table(self):
        print("print truth table")

        variables = [var for var in self.variables.values() if var.name not in ["true", "false"]]
        for var in variables:
            var.value = False

        self.print_table_header()

        self.root.calculate_value()
        self.print_values()

        for i in range(2 ** len(variables) - 1):
            index = -1
            while index < 0 and variables[index].value:
                variables[index].value = False
                index -= 1
            if index <= 0:
                variables[index].value = True

            self.root.calculate_value()
            self.print_values()

    def print_table_header(self):
        for name in self.variables:
            print(name, end=" | ")
        print(self.root.get_truth_table_header(0))

    def print_values(self):
        for name, var in self.variables.items():
            val = center(str(int(var.value)), len(name))
            print(val, end=" | ")
        print(self.root.get_truth_table_entry(0))

    def simplify(self):
        very_previous_form = ''
        while very_previous_form != str(self):
            very_previous_form = str(self)
            previous_form = ''
            while previous_form != str(self):
                previous_form = str(self)
                self.root = self.root.replace_with_and_or()
                self.root = self.root.associative_law()
                self.root = self.root.absorption()
                self.root = self.root.idempotence()
                self.root = self.root.trivial_simplification()
                self.root = self.root.dominance()
                self.root = self.root.identity()
                self.root = self.root.not_operator_simplify()
                self.root = self.root.smart_expand()

            previous_form = ''
            while previous_form != str(self):
                previous_form = str(self)
                self.root = self.root.smart_exclude()
        return self

    def get_values(self):
        return {name: var.value for name, var in self.variables.items()}

    def get_truth_table(self):
        variables = [var for var in self.variables.values() if var.name not in ["true", "false"]]
        for var in variables:
            var.value = False
        yield self.get_values(), self.root.calculate_value()
        for i in range(2 ** len(variables) - 1):

            index = -1
            while index < 0 and variables[index].value:
                variables[index].value = False
                index -= 1
            if index <= 0:
                variables[index].value = True
            yield self.get_values(), self.root.calculate_value()

    def canonical_dnf(self):
        truth_table = self.get_truth_table()
        terms = [term for term, val in truth_table if val]
        new_terms = []
        for term in terms:
            children = []
            for name, val in term.items():
                if val:
                    children.append(self.variables[name])
                else:
                    children.append(NotOperator([self.variables[name]]))
            new_terms.append(AndOperator(children))
        if len(new_terms) == 1:
            self.root = new_terms[0]
        else:
            self.root = OrOperator(new_terms)
        return self

    def canonical_cnf(self):
        truth_table = self.get_truth_table()
        terms = [term for term, val in truth_table if not val]
        new_terms = []
        for term in terms:
            children = []
            for name, val in term.items():
                if not val:
                    children.append(self.variables[name])
                else:
                    children.append(NotOperator([self.variables[name]]))
            new_terms.append(OrOperator(children))
        if len(new_terms) == 1:
            self.root = new_terms[0]
        else:
            self.root = AndOperator(new_terms)
        return self

    def simple_cnf(self):
        self.canonical_cnf()

        for or1 in self.root.children:
            for or2 in self.root.children:
                if or1 != or2 and len(or1.children) <= len(or2.children):
                    difference = [val for val in or1.children
                                  if val not in or2.children]

                    if len(difference) == 1:
                        if isinstance(difference[0], Variable):
                            inverted_diff_var = NotOperator(difference[0])
                        else:
                            inverted_diff_var = difference[0].children[0]

                        if inverted_diff_var in or2.children:
                            or2.children.remove(inverted_diff_var)

        for i in range(len(self.root.children)):
            for j in range(len(self.root.children)):
                or1 = self.root.children[i]
                or2 = self.root.children[j]
                if i != j and 0 < len(or1.children) <= len(or2.children):
                    difference = [val for val in or1.children
                                  if val not in or2.children]
                    if len(difference) == 0:
                        or2.children = []

        self.root.children = list(filter(lambda it: len(it.children) > 0, self.root.children))

        return self

    def simple_dnf(self):
        self.canonical_dnf()

        return self

    def to_nand(self):
        self.simplify()
        self.root = self.root.to_nand()

        return self

    def to_nor(self):
        self.simplify()
        self.root = self.root.to_nor()

        return self

    def clone(self):
        return Formula(self.root.clone())

    def set_values(self, dict):
        for key, value in dict.items():
            self.variables[key].value = value

    def kv(self, scale=1, order=None):
        values = generate_kv(order or list(self.variables.keys()))
        matrix = []
        for row in values:
            new_row = []
            for cell in row:
                self.set_values(cell)
                val = self.root.calculate_value()
                new_row.append(val)
            matrix.append(new_row)
        kv_generator.render_kv_diagramm(matrix, order or list(self.variables.keys()), scale=scale)

    def to_clause_list(self):
        res = []

        if isinstance(self.root, AndOperator):
            for it in self.root.children:
                if isinstance(it, OrOperator):
                    res.append(sorted(it.children, key=lambda i: i.children[0] if isinstance(i, NotOperator) else i))
                elif isinstance(it, Variable) or isinstance(it, NotOperator):
                    res.append([it])
                else:
                    raise TypeError("Nicht in KNF")
        elif isinstance(self.root, OrOperator):
            res = [[it] for it in self.root.children]
        else:
            raise TypeError("Nicht in KNF")

        res.sort(key=lambda i: (len(i), i[0] if isinstance(i[0], Variable) else i[0].children[0]))
        return res

    @staticmethod
    def print_dpll_with_steps(clause_list, assignment):
        print(clause_list)

        def remove_var(lst, vr):
            neg_vr = vr.children[0] if isinstance(vr, NotOperator) else NotOperator(vr)
            rem = []
            lst.remove(lst[0])
            for item in lst:
                if vr in item:
                    rem.append(item)
                elif neg_vr in item:
                    item.remove(neg_vr)
            for item in rem:
                lst.remove(item)

        if len(clause_list) == 0:
            print("Erfüllbar")
            return
        elif len(clause_list[0]) == 0:
            print("Unerfüllbar")
            return
        else:
            if len(clause_list[0]) == 1:
                var = clause_list[0][0]
                print("OLR:", var)
                remove_var(clause_list, var)
                Formula.print_dpll_with_steps(clause_list, assignment)
            else:
                all_vars = set()
                for it in clause_list:
                    for i in it:
                        all_vars.add(i)
                all_vars = sorted(list(all_vars))

                for var in all_vars:
                    neg_var = var.children[0] if isinstance(var, NotOperator) else NotOperator(var)
                    if neg_var not in all_vars:
                        print("PLR:", var)
                        remove_var(clause_list, var)
                        Formula.print_dpll_with_steps(clause_list, assignment)
                        return

                var = all_vars[0]
                print("Fallunterscheidung:", var)
                remove_var(clause_list, var)
                Formula.print_dpll_with_steps(clause_list, assignment)#
                return

    def dpll(self):
        Formula.print_dpll_with_steps(self.to_clause_list(), {})

    def __str__(self):
        return str(self.root)
