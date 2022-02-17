import math


def sterling2(k, n):
    s = 0
    for i in range(n + 1):
        s += (-1) ** (n - i) * math.comb(n, i) * i ** k
    return s // math.factorial(n)


if __name__ == '__main__':
    m = 17
    n = 7
    print(sterling2(m - n, n))
