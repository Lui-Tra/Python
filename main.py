from syntaxtree import *
import re


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


def parse(formel):
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
        elif indent_level == 0 and char in operators.values():
            binding_priority = list(operators.values()).index(char)
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
        elif indent_level == 0 and char == seperator:
            tokens.append(remove_parenthesis(current_token))
            current_token = ""
        else:
            current_token += char
        index += 1
    tokens.append(remove_parenthesis(current_token))
    if len(tokens) == 1:
        return Variable(tokens[0])
    else:
        if seperator == "¬":
            op = Operator([parse(tokens[-1])], "¬")
            print(len(tokens))
            for i in range(len(tokens) - 2):
                op = Operator([op], "¬")
            return op
        else:
            return Operator([parse(token) for token in tokens], seperator)


if __name__ == "__main__":
    print("test")
    formel = "¬a ∧ b ∨ c ∧ b"

    root = parse(formel)
    root.traverse()
    root = root.simplify().simplify()
    print()
    root.traverse()
