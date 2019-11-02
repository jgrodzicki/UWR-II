import time


def czy_doskonala(n):
    dzielniki = []
    i = 1
    while i*i <= n:
        if n%i == 0:
            dzielniki.append(i)
        i+=1

    return n == sum(dzielniki)


def doskonala_imperatywna(n):
    res = []
    for i in range(1, n+1):
        if czy_doskonala(i):
            res.append(i)
    return res


def doskonala_skladana(n):
    return [x for x in range(1, n+1) if czy_doskonala(x)]


def doskonala_funkcyjna(n):
    return list(filter(czy_doskonala, range(1, n+1)))


t = time.time()
doskonala_imperatywna(1000)
print(time.time() - t)

t = time.time()
doskonala_skladana(1000)
print(time.time() - t)

t = time.time()
doskonala_funkcyjna(1000)
print(time.time() - t)