def romb(n):
    for i in range(n + 1):
        print(' ' * (n - i) + '#' * (2 * i + 1) + ' ' * (n - i))
    for i in range(n):
        print(' ' * (i + 1) + '#' * (2 * (n - i) - 1) + ' ' * (i + 1))


romb(4)
