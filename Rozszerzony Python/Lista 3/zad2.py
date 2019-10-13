def square(n):
    sum = 0
    i = 0
    while sum <= n:
        i += 1
        sum += 2 * i - 1

    return i - 1


for i in range(16):
    print(str(i) + ':\t' + str(square(i)))
