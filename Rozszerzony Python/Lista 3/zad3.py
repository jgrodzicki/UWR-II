def sudan(n, x, y):
    global sd

    if (n, x, y) in sd:
        return sd[(n, x, y)]

    if n == 0:
        return x + y
    if y == 0:
        return x

    sd[(n, x, y)] = sudan(n - 1, sudan(n, x, y - 1), sudan(n, x, y - 1) + y)
    return sd[(n, x, y)]


sd = {}

print(sudan(2, 3, 2))
