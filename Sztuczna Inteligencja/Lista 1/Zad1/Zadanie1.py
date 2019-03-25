import time
import collections


def rysuj(ck, bk, bw):
    for j in range(0, 8):
        for i in range(0, 8):
            if [i, j] == ck:
                print("CK", end="  ")
            elif [i, j] == bk:
                print("BK", end="  ")
            elif [i, j] == bw:
                print("BW", end="  ")
            else:
                print("--", end="  ")
        print("\t")

    print("\n\n")


def czy_legalne_ck(poz, bk, bw, state):
    if poz == bk or poz[0] == bw[0] or poz[1] == bw[1]:
        return False

    if poz[0] < 0 or poz[0] > 7 or poz[1] < 0 or poz[1] > 7:
        return False

    if poz[0] == bw[0] or poz[1] == bw[1] or (abs(poz[0] - bk[0]) <= 1 and abs(poz[1] - bk[1]) <= 1):
        return False

    if str((poz, bk, bw)) in state:
        return False

    return True


def czy_legalne_bk(ck, poz, bw, state):
    if poz == ck or poz == bw:
        return False

    if poz[0] < 0 or poz[0] > 7 or poz[1] < 0 or poz[1] > 7 or (abs(poz[0] - ck[0]) <= 1 and abs(poz[1] - ck[1]) <= 1):
        return False

    if str((ck, poz, bw)) in state:
        return False

    return True


def czy_legalne_bw(ck, bk, poz, state, last, typ):
    if poz == ck or poz == bk:
        return False

    if poz[0] < 0 or poz[0] > 7 or poz[1] < 0 or poz[1] > 7:
        return False

    if abs(poz[0] - ck[0]) <= 1 and abs(poz[1] - ck[1]) <= 1:
        return False

    if str((ck, bk, poz)) in state:
        return False

    if typ == 2 and bk[0] == poz[0] and bk[1] < last[1]:
            return False
    elif typ == 4 and bk[1] == poz[1] and bk[0] < last[0]:
            return False
    elif typ == 6 and bk[1] == poz[1] and bk[0] > last[0]:
            return False
    elif bk[0] == poz[0] and bk[1] > last[1]:
            return False

    return True


def czy_mat(czarny_krol, bialy_krol, biala_wieza):
    # przypadki gdy w rogu
    if czarny_krol == [0, 0]:
        if (bialy_krol == [1, 2] and biala_wieza[1] == 0) or (bialy_krol == [2, 1] and biala_wieza[0] == 0):
            return True
        return False

    if czarny_krol == [7, 0]:
        if (bialy_krol == [6, 2] and biala_wieza[1] == 0) or (bialy_krol == [5, 1] and biala_wieza[0] == 7):
            return True
        return False

    if czarny_krol == [0, 7]:
        if (bialy_krol == [1, 5] and biala_wieza[1] == 7) or (bialy_krol == [2, 6] and biala_wieza[0] == 0):
            return True
        return False

    if czarny_krol == [7, 7]:
        if (bialy_krol == [6, 5] and biala_wieza[1] == 7) or (bialy_krol == [5, 6] and biala_wieza[0] == 7):
            return True
        return False

    # przypadki gdy przy scianie
    if (czarny_krol[0] == 0 or czarny_krol[0] == 7) and abs(czarny_krol[0] - bialy_krol[0]) == 2 and \
            czarny_krol[1] == bialy_krol[1] and czarny_krol[0] == biala_wieza[0]:
        return True

    if (czarny_krol[1] == 0 or czarny_krol[1] == 7) and abs(czarny_krol[1] - bialy_krol[1]) == 2 and \
            czarny_krol[0] == bialy_krol[0] and czarny_krol[1] == biala_wieza[1]:
        return True

    return False


def add(new_ck, new_bk, new_bw, ck, bk, bw, czy_b, poz_ruchy_bw):
    global state, przejscia, queue

    state.add(str((new_ck, new_bk, new_bw)))
    przejscia[str((new_ck, new_bk, new_bw))] = str((ck, bk, bw))
    queue.append([new_ck, new_bk, new_bw, czy_b, poz_ruchy_bw])


def constr_graph(czy_b, ck, bk, bw):
    global state, przejscia, queue
    queue = collections.deque([[ck, bk, bw, czy_b, 2]])
    count = 0
    state = {str((ck, bk, bw))}
    przejscia = {}
    og_pos = (ck, bk, bw)

    while True:
        count += 1
        cur = queue.popleft()

        ck = cur[0]
        bk = cur[1]
        bw = cur[2]
        czy_b = cur[3]
        poz_ruchow_bw = cur[4]

        if czy_b:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not i and not j:
                        continue

                    new_bk = [bk[0] + i, bk[1] + j]
                    if czy_legalne_bk(ck, new_bk, bw, state):
                        add(ck, new_bk, bw, ck, bk, bw, not czy_b, poz_ruchow_bw)

            if poz_ruchow_bw:
                new_bw = [bw[0], 0]
                if czy_legalne_bw(ck, bk, new_bw, state, bw, 2):
                    add(ck, bk, new_bw, ck, bk, bw, not czy_b, poz_ruchow_bw)

                new_bw = [bw[0], 7]
                if czy_legalne_bw(ck, bk, new_bw, state, bw, 8):
                    add(ck, bk, new_bw, ck, bk, bw, not czy_b, poz_ruchow_bw)

                new_bw = [0, bw[1]]
                if czy_legalne_bw(ck, bk, new_bw, state, bw, 4):
                    add(ck, bk, new_bw, ck, bk, bw, not czy_b, poz_ruchow_bw)

                new_bw = [7, bw[1]]
                if czy_legalne_bw(ck, bk, new_bw, state, bw, 6):
                    add(ck, bk, new_bw, ck, bk, bw, not czy_b, poz_ruchow_bw)

        else:
            if czy_mat(ck, bk, bw):
                koniec((ck, bk, bw), og_pos, przejscia)
                return

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not i and not j:
                        continue

                    new_ck = [ck[0] + i, ck[1] + j]
                    if czy_legalne_ck(new_ck, bk, bw, state):
                        add(new_ck, bk, bw, ck, bk, bw, not czy_b, poz_ruchow_bw)


def koniec(pos, og_pos, przejscia):
    count = 0

    pos = str(pos)
    og_pos = str(og_pos)

    int_pos = eval(pos)
    rysuj(int_pos[0], int_pos[1], int_pos[2])

    while pos != og_pos:
        count += 1
        pos = przejscia[pos]
        int_pos = eval(pos)
        rysuj(int_pos[0], int_pos[1], int_pos[2])

    print(count)
    # f = open("zad1_output.txt", "a")
    # f.write(str(count) + "\n")
    # f.close()

    return


def convert_pos_to_int(pos):
    dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    return [dict[pos[0]], eval(pos[1])-1]


state = {}
przejscia = {}
queue = []

input = open("zad1_input.txt", "r").read().split("\n")
out = open("zad1_output.txt", "w").close()

for line in input:
    line = line.split(" ")
    czy_b = line[0] == 'white'
    bialy_krol = convert_pos_to_int(line[1])
    biala_wieza = convert_pos_to_int(line[2])
    czarny_krol = convert_pos_to_int(line[3])

    start = time.time()

    constr_graph(czy_b, czarny_krol, bialy_krol, biala_wieza)
    print(f'\t---done in: {time.time() - start}')
