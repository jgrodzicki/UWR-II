import collections
import time
from os import system


def is_guy_move_good(x, y):
    if 0 <= x < cols and 0 <= y < rows:
        if (x, y) not in walls:
            return True
    return False


def is_chest_move_good(x, y, chests):
    if 0 <= x < cols and 0 <= y < rows:
        if (x, y) not in chests and (x, y) not in walls:
            return True
    return False


def is_finished(chests):
    for ch in chests:
        if ch not in goals:
            return False
    return True


# def draw(pos, chests):
#     for i in range(rows):
#         for j in range(cols):
#             if (j, i) in chests and (j, i) in goals:
#                 print('*', end=" ")
#             elif (j, i) in pos and (j, i) in goals:
#                 print('+', end=" ")
#             elif (j, i) == pos:
#                 print('K', end=" ")
#             elif (j, i) in chests:
#                 print('C', end=" ")
#             elif (j, i) in walls:
#                 print('W', end=" ")
#             elif (j, i) in goals:
#                 print('G', end=" ")
#             else:
#                 print(".", end=" ")
#         print()


def finish(dir, state):
    count = 0
    ans = ""
    prev_pos = state[0]
    state = dir[str(state)]

    while state != "-1":
        s = ''
        if state[0][0] > prev_pos[0]:
            s = 'L'
        elif state[0][0] < prev_pos[0]:
            s = 'R'
        elif state[0][1] > prev_pos[1]:
            s = 'U'
        else:
            s = 'D'

        prev_pos = state[0]

        ans = s + ans
        count += 1

        state = dir[str(state)]


    print(ans)
    print(count)
    o = open("zad_output.txt", "w")
    o.write(ans)
    o.close()


def find_bfs(pos, chests):
    queue = collections.deque([[pos, chests]])
    done = {str((pos, chests))}

    dir = {str([pos, chests]): "-1"}

    while True:
        try:
            cur = queue.popleft()
            pos = cur[0]
            chests = cur[1]
        except:
            print("error")
            print(len(done))
            return

        for i in range(4):
            if i == 0:
                x_d = -1
                y_d = 0
            elif i == 1:
                x_d = 1
                y_d = 0
            elif i == 2:
                x_d = 0
                y_d = -1
            else:
                x_d = 0
                y_d = 1

            x = pos[0] + x_d
            y = pos[1] + y_d

            if is_guy_move_good(x, y):
                if (x, y) in chests:
                    if is_chest_move_good(x+x_d, y+y_d, chests):
                        cc = list(chests)
                        cc.remove((x, y))
                        cc.append((x+x_d, y+y_d))

                        if str(((x, y), cc)) not in done:
                            done.add(str(((x, y), cc)))
                            dir[str([(x, y), cc])] = [pos, chests]

                            if is_finished(cc):
                                finish(dir, [(x, y), cc])
                                return
                            queue.append([(x, y), cc])
                else:
                    if str(((x, y), chests)) not in done:
                        done.add(str(((x, y), chests)))
                        dir[str([(x, y), chests])] = [pos, chests]
                        queue.append([(x, y), chests])


def load():
    global rows, cols, goals, walls, chests, pos

    input = open(maps[0], "r").read().split("\n")
    # input = open("zad_input.txt", "r").read().split("\n")
    rows = len(input)
    cols = len(input[0])

    for i in range(rows-1):
        line = input[i]
        for j in range(cols):
            if line[j] == 'W':
                walls.append((j, i))
            elif line[j] == 'K':
                pos = (j, i)
            elif line[j] == 'B':
                chests.append((j, i))
            elif line[j] == 'G':
                goals.append((j, i))
            elif line[j] == '*':
                chests.append((j, i))
                goals.append((j, i))
            elif line[j] == '+':
                pos = (j, i)
                goals.append((j, i))


maps = ["maps/map1.txt", "maps/map2.txt", "maps/map3.txt", "maps/map4.txt", "maps/map5.txt",
        "maps/map6.txt", "maps/map7.txt", "maps/map8.txt", "maps/map9.txt", "maps/map10.txt"]

cols, rows = 0, 0
walls = []
goals = []
chests = []
pos = ()

start = time.time()
load()
# draw(pos, chests)

find_bfs(pos, chests)
print(time.time() - start)
