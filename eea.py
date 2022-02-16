def eea(a, b):
    print("     a     b     k    al    be")
    while a != 0:
        al, be = _eea(a, b)
        print("".join([str(it).rjust(6, " ") for it in [a, b, b // a, al, be]]))
        a, b = b % a, a

    al, be = _eea(a, b)
    print("".join([str(it).rjust(6, " ") for it in [a, b, "-", al, be]]))


def _eea(a, b):
    if a == 0:
        return 0, 1
    else:
        alpha, beta = _eea(b % a, a)
        return beta - (b // a) * alpha, alpha


if __name__ == '__main__':
    eea(a=935, b=1491)
