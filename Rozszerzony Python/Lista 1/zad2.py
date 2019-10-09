pieniadze = [20, 10, 5, 2, 1]


def wydaj(kwota):
    do_wydania = {}
    for p in pieniadze:
        do_wydania[p] = kwota//p
        kwota = kwota % p

    return do_wydania


print(wydaj(123))