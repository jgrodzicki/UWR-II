import heapq
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


def load(map):
    global rows, cols, goals, walls, chests, pos

    # input = open(maps[map], "r").read().split("\n")
    input = open("zad_input.txt", "r").read().split("\n")
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


def good_move(player_x, player_y, chests, dir):
    if not (0 <= player_x < cols) or not (0 <= player_y < rows) or (player_x, player_y) in walls:
        return False
    
    if (player_x, player_y) in chests:
        if not is_chest_move_good(player_x + x_dir[dir], player_y + y_dir[dir], chests):
            return False
    else:
        if not is_guy_move_good(player_x, player_y):
            return False

    return True


def heuristic(state):
    pos = state[0]
    chests = state[1]
    no_moves = len(state[2])
    min_dist = 1e9
    player_x, player_y = pos[0], pos[1]

    for c in chests:
        act_dist = abs(player_x - c[0]) + abs(player_y - c[1])
        for g in goals:
            min_dist = min(min_dist, act_dist + abs(c[0] - g[0]) + abs(c[1] - g[1]))

    return min_dist + no_moves


def is_win(chests):
    for c in chests:
        if c not in goals:
            return False

    return True


def hash_state(state):
    pos = state[0]
    chests = tuple(state[1])
    return (pos, chests)


def move_chest(x, y, dir, chests):
    for i in range(len(chests)):
        c_x = chests[i][0]
        c_y = chests[i][1]

        if c_x == x and c_y == y:
            chests[i] = (c_x + x_dir[dir], c_y + y_dir[dir])


def a_star(pos, chests, moves):
    og_state = (pos, chests)

    q = []  # priority queue
    done = set()
    moves = []
    state = (pos, chests, moves)
    heapq.heappush(q, (heuristic(state), state))
    done.add(hash_state(state))

    while len(q) > 0:
        act_state = heapq.heappop(q)[1]

        if is_win(act_state[1]):
            # reconstruct(og_state, act_state[2])
            # print(len(moves))
            # # draw(act_state[0], act_state[1])
            # out = open("zad_output.txt", "w").close()
            for m in act_state[2]:
                out = open("zad_output.txt", "a")
                out.write(str(m))
            out.close()
            # print(str(moves))
            break

        pos = act_state[0]
        for i in range(4):
            new_x = pos[0] + x_dir[i]
            new_y = pos[1] + y_dir[i]

            # chests = act_state[1].copy()
            # moves = act_state[2].copy()
            chests = act_state[1][:]
            moves = act_state[2][:]

            if good_move(new_x, new_y, chests, i):
                if (new_x, new_y) in chests:
                    move_chest(new_x, new_y, i, chests)

                moves.append(char_dir[i])
                new_state = ((new_x, new_y), chests, moves)
                if hash_state(new_state) not in done:
                    # print(f'new_x: {new_x}\tnew_y: {new_y}')
                    done.add(hash_state(new_state))
                    heapq.heappush(q, (heuristic(new_state), new_state))

    # print(q)


def reconstruct(start_state, moves):
    # print(len(moves))
    player_x = start_state[0][0]
    player_y = start_state[0][1]
    chests = start_state[1]

    draw((player_x, player_y), chests)
    print()

    for m in moves:
        move_x, move_y = 0, 0
        if m == 'R':
            move_x = 1
        elif m == 'L':
            move_x = -1
        elif m == 'U':
            move_y = -1
        else:
            move_y = 1
        print(m)

        player_x += move_x
        player_y += move_y

        if (player_x, player_y) in chests:
            for i in range(len(chests)):
                if chests[i] == (player_x, player_y):
                    chests[i] = (chests[i][0] + move_x, chests[i][1] + move_y)
                    break

        time.sleep(0.3)
        _ = system('clear')
        draw((player_x, player_y), chests)
        print()
    print(len(moves))


maps = ["maps/map1.txt", "maps/map2.txt", "maps/map3.txt", "maps/map4.txt", "maps/map5.txt",\
        "maps/map6.txt", "maps/map7.txt", "maps/map8.txt", "maps/map9.txt", "maps/map10.txt"]

char_dir = ['R', 'L', 'D', 'U']

x_dir = [1, -1, 0, 0]
y_dir = [0, 0, 1, -1]

cols, rows = 0, 0
walls = []
goals = []
chests = []
pos = ()

load(0)
a_star(pos, chests, [])

# for i in range(len(maps)):
#     cols, rows = 0, 0
#     walls = []
#     goals = []
#     chests = []
#     pos = ()
#     load(i)
#     a_star(pos, chests, [])
