import re
import random


def draw():
    for i in range(rows):
        for j in range(cols):
            if monogram[i][j] == 0:
                print("-", end=" ")
            else:
                print("X", end=" ")
        print()


def change(row, col):
    global monogram

    if monogram[row][col] == 0:
        monogram[row][col] = 1
        monogram[rows+col][row] = 1
    else:
        monogram[row][col] = 0
        monogram[rows+col][row] = 0


def is_not_good(arr, specs):
    s = "^0*" + "1"*specs + "0*$"
    return re.search(s, ''.join(str(e) for e in arr)) is None


def are_cols_good():
    for i in range(cols):
        if is_not_good(monogram[rows+i], spec[rows+i]):
            return False
    return True


def random_row_not_good_row_index():
    res = []

    for i in range(rows):
        if is_not_good(monogram[i], spec[i]):
            res.append(i)

    if len(res) > 0:
        return res[random.randint(0, len(res)-1)]
    else:
        return -1


def random_not_good_col_index():
    res = []
    for i in range(rows, rows+cols):
        if is_not_good(monogram[i], spec[i]):
            res.append(i)
    if len(res) > 0:
        return res[random.randint(0, len(res)-1)]
    else:
        return -1


def opt_elem(index):
    def count_not_good(arr, sp):
        bin_ar = [1 for _ in range(sp)] + [0 for _ in range(len(arr) - sp)]
        min = len(arr)

        for _ in range(len(arr) - sp + 1):
            count = 0
            for j in range(len(arr)):
                if arr[j] != bin_ar[j]:
                    count += 1
            if count < min:
                min = count

            bin_ar = [0] + bin_ar[:-1]
        return min

    min = 2*len(monogram[index])+1
    good_ind = -1
    for i in range(len(monogram[index])):
        change(index, i)
        x = count_not_good(monogram[index], spec[index]) + count_not_good(monogram[rows+i], spec[rows+i])
        if x < min:
            min = x
            good_ind = i

        change(index, i)

    return good_ind


def run():
    count = 0
    ind = random_row_not_good_row_index()

    while ind != -1:
        if count%5 == 0:
            change(random.randint(0, rows-1), random.randint(0, cols-1))
        else:
            opt = opt_elem(ind)
            change(ind, opt)

        ind = random_row_not_good_row_index()
        count += 1
        if count > rows*cols*5:
            return -1

    return 0


def random_monogram():
    global monogram
    monogram = [[random.randint(0, 1) for _ in range(cols)] for _ in range(0, rows)]
    mono_vert = []

    # monogram = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(cols):
        to_add = []
        for row in monogram:
            to_add.append(row[i])
        mono_vert.append(to_add)
    monogram.extend(mono_vert)


def load():
    global rows, cols, spec
    input = open("input.txt", "r").read().split("\n")
    x = input[0].split(" ")
    rows = eval(x[0])
    cols = eval(x[1])
    for line in input[1:]:
        spec.append(eval(line))


spec = []
load()
monogram = []
random_monogram()
res = run()

while not are_cols_good():
    draw()
    print()
    random_monogram()
    res = run()
    while res == -1:
        random_monogram()
        res = run()

print("\n\n\n")
print(spec)
draw()
