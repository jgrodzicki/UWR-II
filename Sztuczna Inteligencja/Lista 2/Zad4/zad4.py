import random
import itertools
import collections
import time


def load(map):
    global rows, cols, possible_pos, goals, walls

    # input = open(maps[map]).read().split("\n")
    input = open("zad_input.txt", "r").read().split("\n")

    rows = len(input)
    cols = len(input[0])

    for i in range(rows-1):
        for j in range(cols):
            if input[i][j] == '#':
                walls.add((j, i))
            elif input[i][j] == 'G':
                goals.add((j, i))
            elif input[i][j] == 'S':
                possible_pos.add((j, i))
            elif input[i][j] == 'B':
                possible_pos.add((j, i))
                goals.add((j, i))


# def draw(pos):
#     # print('#')
#     for j in range(rows):
#         for i in range(cols):
#             if (i, j) in pos and (i, j) in goals:
#                 print("B", end=" ")
#             elif (i, j) in pos:
#                 print("K", end=" ")
#             elif (i, j) in goals:
#                 print("G", end=" ")
#             elif (i, j) in walls:
#                 print("#", end=" ")
#             else:
#                 print(" ", end=" ")
#         print()
#     print()


def find_new_possible(possible_pos, dir):
    new_pos = set()

    for pos in possible_pos:
        new_x = pos[0] + x_dir[dir]
        new_y = pos[1] + y_dir[dir]

        if (new_x, new_y) not in walls:
            new_pos.add((new_x, new_y))
        else:
            new_pos.add((pos[0], pos[1]))
    return new_pos


def is_finished(possible):
    for pos in possible:
        if pos not in goals:
            return False

    return True


def convert_seq_to_string(moves):
    res = ""
    for m in moves:
        if m == 0:
            res += "R"
        elif m == 1:
            res += "L"
        elif m == 2:
            res += "D"
        else:
            res += "U"

    return res


def bfs(possible, moves):
    done = set()
    queue = collections.deque()
    queue.append((possible, moves))
    done.add(str(possible))
    min_leng_pos = len(possible)

    while True:
        cur = queue.popleft()
        possible = cur[0]
        moves = cur[1]

        if is_finished(possible):
            print(len(moves))
            print(convert_seq_to_string(moves))
            # draw(possible)
            output = open("zad_output.txt", "w")
            output.write(convert_seq_to_string(moves))
            output.close()
            break

        for i in range(4):
            new_pos = find_new_possible(possible, i)
            if str(new_pos) not in done:
                if len(new_pos) < min_leng_pos:
                    done = set()
                    queue.clear()
                    min_leng_pos = len(new_pos)
                done.add(str(new_pos))
                queue.append((new_pos, moves + [i]))


maps = ["maps/map1.txt", "maps/map2.txt", "maps/map3.txt", "maps/map4.txt", "maps/map5.txt", "maps/map6.txt",\
        "maps/map7.txt", "maps/map8.txt", "maps/map9.txt", "maps/map10.txt", "maps/map11.txt"]

x_dir = [1, -1, 0, 0]
y_dir = [0, 0, 1, -1]

start_all = time.time()
# for i in range(len(maps)):
start = time.time()

walls = set()
goals = set()
possible_pos = set()
# load(i)
load(0)

moves = []
not_good_dir = -1
c = 0

options = ['0', '1', '2', '3']
all_seq = list(itertools.permutations(options))

min_leng = len(possible_pos) + 1
best_mov_seq = []
best_pos = []
ind = -1

for i in range(len(all_seq)):
    seq = all_seq[i]
    act_pos = possible_pos.copy()
    act_seq = []
    for s in seq:
        act_seq += s*12
    mov = []
    for m in act_seq:
        act_pos = find_new_possible(act_pos, eval(m))
        mov.append(eval(m))

    if len(act_pos) < min_leng:
        min_leng = len(act_pos)
        ind = i
        best_mov_seq = mov
        best_pos = act_pos

bfs(best_pos, best_mov_seq)

