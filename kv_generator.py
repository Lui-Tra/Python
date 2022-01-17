

def mirror_kv_h(kv, new_var):
    res = kv
    for i, line in enumerate(kv):
        new_line = []
        for vars in line:
            new_vars = dict(vars)
            new_vars[new_var] = True
            new_line.append(new_vars)
        res[i] += reversed(new_line)
    return res


def mirror_kv_v(kv, new_var):
    res = kv
    for line in reversed(kv):
        new_line = []
        for vars in line:
            new_vars = dict(vars)
            new_vars[new_var] = 1
            new_line.append(vars | {new_var:True})
        res.append(new_line)
    return res


def __generate_kv__(variables, current_variables):
    if len(current_variables) == 0:
        return [[{v: False for v in variables}]]
    else:
        prev_variables = current_variables[:-1]
        new_var = current_variables[-1]

        prev_kv = __generate_kv__(variables, prev_variables)

        if len(prev_variables) % 2 == 0:
            return mirror_kv_h(prev_kv, new_var)
        else:
            return mirror_kv_v(prev_kv, new_var)


def generate_kv(variables):
    return __generate_kv__(variables, variables)


def print_matrix(matrix):
    for line in matrix:
        for elem in line:
            print(elem, end=" ")
        print()


if __name__ == '__main__':
    print("res:")
    matrix = generate_kv([1, 2])
    print_matrix(matrix)
    matrix = generate_kv([1, 2, 3])
    print_matrix(matrix)
