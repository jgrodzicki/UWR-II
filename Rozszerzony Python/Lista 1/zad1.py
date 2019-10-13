zakupy = [0.2, 0.5, 4.59, 6]


def vat_faktura(lista):
    return round(sum(lista) * .23, 2)


def vat_paragon(lista):
    return sum([round(l * .23, 2) for l in lista])


print(vat_faktura(zakupy) == vat_paragon(zakupy))
