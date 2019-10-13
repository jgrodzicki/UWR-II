def sudan(n, x, y):
    def to_hash(n, x, y):
        return str([n, x, y])

    global sd

    if to_hash(n, x, y) in sd:
        return sd[to_hash(n, x, y)]

    if n == 0:
        return x + y
    if y == 0:
        return x

    sd[to_hash(n, x, y)] = sudan(n - 1, sudan(n, x, y - 1), sudan(n, x, y - 1) + y)
    return sd[to_hash(n, x, y)]


sd = {}

print(sudan(2, 3, 2))

