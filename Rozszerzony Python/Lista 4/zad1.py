import time


def czy_pierwsza(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    i = 5
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def pierwsze_imperatywna(n):
    res = []
    for i in range(2, n + 1):
        if czy_pierwsza(i):
            res.append(i)
    return res


def pierwsze_skladana(n):
    return [x for x in range(2, n + 1) if czy_pierwsza(x)]


def pierwsze_funkcyjna(n):
    return list(filter(czy_pierwsza, range(2, n + 1)))


t = time.time()
pierwsze_imperatywna(50)
print(time.time() - t)

t = time.time()
pierwsze_skladana(50)
print(time.time() - t)

t = time.time()
pierwsze_funkcyjna(50)
print(time.time() - t)
