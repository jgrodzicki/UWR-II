import heapq
import collections


def find_to_goal():
    global to_goal
    queue = collections.deque()
    for g in goals:
        queue.append(g)
        to_goal[g] = 0

    while queue:
        pos = queue.popleft()
        no = to_goal[pos]

        for i in range(4):
            new_pos = (pos[0] + x_dir[i], pos[1] + y_dir[i])
            if new_pos not in walls and new_pos not in to_goal:
                to_goal[new_pos] = no + 1
                queue.append(new_pos)


def heuristic(pos, no_moves):
    m = [to_goal[p] for p in pos]

    res = max(m)
    return res + no_moves


def move(pos, dir):
    res = set()
    for p in pos:
        if (p[0] + x_dir[dir], p[1] + y_dir[dir]) in walls:
            res.add(p)
        else:
            res.add((p[0] + x_dir[dir], p[1] + y_dir[dir]))

    return res


def is_done(pos):
    for p in pos:
        if p not in goals:
            return False
    return True


def load(map):
    global possible_pos, walls, goals, rows, cols

    if map == -1:
        input = open("zad_input.txt", "r").read().split("\n")
    else:
        input = open(maps[map], "r").read().split("\n")

    rows = len(input) - 1
    cols = len(input[0])

    for i in range(rows):
        for j in range(cols):
            if input[i][j] == '#':
                walls.add((j, i))
            elif input[i][j] == 'S':
                possible_pos.add((j, i))
            elif input[i][j] == 'G':
                goals.add((j, i))
            elif input[i][j] == 'B':
                possible_pos.add((j, i))
                goals.add((j, i))


def draw(pos):
    for i in range(rows):
        s = ""
        for j in range(cols):
            if (j, i) in pos:
                s += "S"
            elif (j, i) in walls:
                s += "#"
            elif (j, i) in goals:
                s += "G"
            else:
                s += " "
        print(s)


def a_star(pos):
    q = []
    heapq.heappush(q, (heuristic(pos, 0), pos, ''))
    visited = set()
    visited.add(tuple(pos))

    while True:
        cur = heapq.heappop(q)
        pos = cur[1]
        moves = cur[2]

        if is_done(pos):
            print(len(moves))
            print(moves)
            out = open("zad_output.txt", "w")
            out.write(moves)
            out.close()
            return

        for i in range(4):
            new = move(pos, i)
            if tuple(new) not in visited:
                heapq.heappush(q, (heuristic(new, len(moves)), new, moves + char_moves[i]))
                visited.add(tuple(new))


maps = ["maps/map1.txt", "maps/map2.txt", "maps/map3.txt", "maps/map4.txt", "maps/map5.txt", "maps/map8.txt"]

char_moves = ['R', 'L', 'D', 'U']
x_dir = [1, -1, 0, 0]
y_dir = [0, 0, 1, -1]
possible_pos = set()
walls = set()
goals = set()
rows = cols = 0

load(-1)
to_goal = {}
find_to_goal()
a_star(possible_pos)
