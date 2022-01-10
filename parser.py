import re
from constants import operators
from constants import prefix_operators
from Operator import get_operator
from Variable import Variable


def remove_parenthesis(token):
    indent_level = 1
    index = 1
    remove = True
    if len(token) > 2 and token[0] == "(" and token[-1] == ")":
        while index < len(token) - 1:
            if token[index] == "(":
                indent_level += 1
            elif token[index] == ")":
                indent_level -= 1
            if indent_level <= 0:
                remove = False
            index += 1
    else:
        remove = False
    if remove:
        return token[1:-1]
    else:
        return token


def find_operator(formel, index):
    char = formel[index]
    if char in operators.values():
        return char
    else:
        for operator in operators.values():
            if index + (len(operator) - 1) <= len(formel):
                if operator.startswith(char):
                    if formel[index:index + len(operator)] == operator:
                        return operator
        return None

def preproc_prefix(formel):
    index = 0
    new_formel = ""
    while index < len(formel):
        char = formel[index]
        for operator in prefix_operators:
            if operator.startswith(char) and formel[index:index+len(operator)] == operator:
                index += len(operator)
                char = formel[index]
                if char != "(":
                    raise SyntaxError
                indent_level = 1
                index += 1
                tokens = []
                current_token = ""
                while indent_level > 0 and index < len(formel):
                    char = formel[index]
                    if char == "(":
                        current_token += char
                        indent_level += 1
                    elif char == ")":
                        if indent_level > 1:
                            current_token += char
                        indent_level -= 1
                    elif indent_level == 1 and char == ",":
                        tokens.append(current_token)
                        current_token = ""
                    else:
                        current_token += char
                    index += 1
                tokens.append(current_token)
                if indent_level > 0:
                    raise SyntaxError

                tokens = [preproc_prefix(token) for token in tokens]

                new_formel += "("+(" "+operator+" ").join(tokens)+")"
                break
        else:
            new_formel += char
        index += 1
    return new_formel


def __parse__(formel):
    formel = re.sub(r"\s", "", formel)
    formel = remove_parenthesis(formel)

    index = 0
    indent_level = 0
    min_binding_priority = -1
    while index < len(formel):
        char = formel[index]
        if char == "(":
            indent_level += 1
        elif char == ")":
            indent_level -= 1
        elif indent_level == 0:
            operator = find_operator(formel, index)
            if operator is not None:
                binding_priority = list(operators.values()).index(operator)
                if binding_priority > min_binding_priority:
                    min_binding_priority = binding_priority
        index += 1
    if indent_level != 0:
        raise ValueError("invalid")

    index = 0
    indent_level = 0
    current_token = ""
    tokens = []
    seperator = list(operators.values())[min_binding_priority]
    while index < len(formel):
        char = formel[index]
        if char == "(":
            current_token += char
            indent_level += 1
        elif char == ")":
            current_token += char
            indent_level -= 1
        elif indent_level == 0 and find_operator(formel, index) == seperator:
            tokens.append(remove_parenthesis(current_token))
            current_token = ""
            index += len(seperator) - 1
        else:
            current_token += char
        index += 1
    tokens.append(remove_parenthesis(current_token))

    if len(tokens) == 1:
        return Variable(tokens[0])
    else:
        if seperator == "¬":
            op = get_operator(seperator, [parse(tokens[-1])])
            for i in range(len(tokens) - 2):
                op = get_operator(seperator, [op])
            return op
        else:
            return get_operator(seperator, [parse(token) for token in tokens])


def parse(formel):
    formel = preproc_prefix(formel)
    return __parse__(formel)


if __name__ == "__main__":
    formel = "ITE(a, b, ITE(d, e))"

    formel = preproc_prefix(formel)

    print(formel)

    root = parse(formel)
    print(root)
