import math


class ZSternGruppe:
    def __init__(self, n):
        self.n = n
        self.elements = []
        for i in range(1, n):
            if ggT(i, n) == 1:
                self.elements.append(i)

    def erzeuger(self):
        res = []
        for it in self.elements:
            if self.ist_erzeuger(it):
                res.append(it)
        return res

    def ist_erzeuger(self, a):
        return self.ord(a) == len(self.elements)

    def ord(self, a):
        return len(self.untergruppe(a))

    def untergruppe(self, a):
        res = [a, self.mul(a, a)]
        while res[0] != res[-1]:
            res.append(self.mul(res[-1], a))
        res = res[:-1]
        return res

    def mul(self, a, b):
        return (a * b) % self.n

    def inverses(self, a):
        inv, _ = _eea(a, self.n)
        return inv % self.n

    def pow(self, a, b):
        if b < 0:
            a = self.inverses(a)
            b = -b

        res = 1
        for i in range(b):
            res = self.mul(res, a)
        return res

    def gruppenexponent(self):
        exp = set()
        for it in self.elements:
            exp.add(self.ord(it))
        return math.lcm(*exp)


def ggT(a, b):
    if a == 0:
        return b
    if a > b:
        return ggT(a % b, b)
    else:
        return ggT(b % a, a)


def kgV(a, b):
    return math.lcm(a, b)


def primfaktoren(n):
    i = 2
    res = []
    while n != 1:
        if n % i == 0:
            n /= i
            res.append(i)
            i = 2
        else:
            i += 1
    return res


def phi(n):
    prf = set(primfaktoren(n))
    res = 1
    for k in prf:
        res *= k - 1
    return res


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
    g = ZSternGruppe(83)
    print(264 % 83)
    print(245 % 82)
