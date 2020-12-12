import heapq
import numpy as np
import sys
import time
from typing import Tuple, NamedTuple, List, Optional


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def measure_distance(pos_1: Tuple[int, int], pos_2: Tuple[int, int]) -> float:
    dx, dy = abs(pos_1[0] - pos_2[0]), abs(pos_1[1] - pos_2[1])
    return dx + dy + (np.sqrt(2) - 2) * min(dx, dy)


def heuresis_distance(pos_1: Tuple[int, int], pos_2: Tuple[int, int]) -> float:
    return measure_distance(pos_1, pos_2)


class Distance:
    def __init__(self, N: int, NE: int, E: int, SE: int, S: int, SW: int, W: int, NW: int):
        self.N, self.NE, self.E, self.SE, self.S, self.SW, self.W, self.NW = N, NE, E, SE, S, SW, W, NW


class Heap:
    def __init__(self) -> None:
        self._heap = []
    
    def push(self, heuristics_value: float, position: Tuple[int, int, str], cost_from_start: float):
        heapq.heappush(self._heap, (heuristics_value, position, cost_from_start))
    
    def pop_min(self) -> Tuple[int, Tuple[int, int, str], float]:
        return heapq.heappop(self._heap)
    
    def pop_push_min(self) -> Tuple[int, Tuple[int, int, str], float]:
        '''
        :return: The maximum node from the heap and pushes it back (the heap remains the same)
        '''
        value, position, cost = self.pop_min()
        self.push(value, position, cost)
        return value, position, cost
    
    def __len__(self) -> int:
        return len(self._heap)


class JPS:
    def __init__(
        self,
        height: int,
        width: int,
        start_column: int,
        start_row: int,
        goal_column: int,
        goal_row: int,
        tiles_data: List[List[int]],
    ) -> None:
        self._height = height
        self._width = width
        
        self._position = (start_column, start_row)
        self._distance_from_start = 0
        
        self._goal_position = (goal_column, goal_row)
        self._distances = dict()
        for column, row, n, ne, e, se, s, sw, w, nw in tiles_data:
            self._distances[(column, row)] = Distance(N=n, NE=ne, E=e, SE=se, S=s, SW=sw, W=w, NW=nw)
        
        self._heap = Heap()
        heuristic = measure_distance(self._position, self._goal_position)
        for dir in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']:
            if self._distances[self._position].__dict__[dir] != 0:
                self._heap.push(heuristic, (self._position[0], self._position[1], dir), 0)
        
        self._visited = {self._position}
        self._traversing = dict()  # Gives a previous state.
        # Flag set when found path to the goal position. If true, run function just prints the next states.
        self._found_path = False
        self._no_path = False

    
    def _run(self, time_limit: float) -> None:
        start_time = time.time()
        while time.time() - start_time < time_limit:
            if len(self._heap) == 0:
                self._no_path = True
                return
            
            heuristic_value, (x, y, dir), cost_from_start = self._heap.pop_min()
            position = (x, y)
            if position == self._goal_position:
                self._found_path = True
                self._heap.push(-np.inf, (x, y, dir), cost_from_start)
                log('FOUND ONE!!!')
                return
            if position == (3, 2):
                log(heuristic_value)
                log(cost_from_start)
            distance = self._distances[position].__dict__[dir]
            xd = yd = 0
            if 'N' in dir:
                yd = -1
            if 'S' in dir:
                yd = 1
            if 'E' in dir:
                xd = 1
            if 'W' in dir:
                xd = -1
            
            distance = abs(distance)  # Ignore the fact it can be to the wall.
            
            for i in range(1, distance+1):
                tmp_position = (position[0] + i*xd, position[1] + i*yd)
                if tmp_position == self._goal_position:
                    tmp_cost_from_start = cost_from_start + measure_distance(position, tmp_position)
                    self._heap.push(tmp_cost_from_start + measure_distance(position, self._goal_position), (self._goal_position[0], self._goal_position[1], '0'), tmp_cost_from_start)
                    self._traversing[(self._goal_position, tmp_cost_from_start)] = (position, cost_from_start)
                    
                # if tmp_position not in self._visited:
                #     tmp_cost_from_start = cost_from_start + measure_distance(position, tmp_position)
                #
                #     self._traversing[(tmp_position, tmp_cost_from_start)] = (position, cost_from_start)
                #
                #     log(f'{tmp_cost_from_start + measure_distance(tmp_position, self._goal_position)}\t{tmp_position}\t{tmp_cost_from_start}')
                #     for possible_dir in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']:
                #         if self._distances[tmp_position].__dict__[possible_dir] != 0:
                #             self._heap.push(tmp_cost_from_start + measure_distance(tmp_position, self._goal_position),
                #                             (tmp_position[0], tmp_position[1], possible_dir),
                #                             tmp_cost_from_start)
                #     self._visited.add(tmp_position)
                
            new_position = (position[0] + distance * xd, position[1] + distance * yd)
            if new_position in self._visited:
                pass

            new_cost_from_start = cost_from_start + measure_distance(position, new_position)
            new_heuristic_value = new_cost_from_start + measure_distance(new_position, self._goal_position)

            log(f'{new_cost_from_start + measure_distance(new_position, self._goal_position)}\t{new_position}\t{new_cost_from_start}')
            for possible_dir in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']:
                if self._distances[new_position].__dict__[possible_dir] != 0:
                    self._heap.push(new_heuristic_value, (new_position[0], new_position[1], possible_dir), new_cost_from_start)
            self._traversing[(new_position, new_cost_from_start)] = (position, cost_from_start)
            self._visited.add(new_position)
    
    
    def find_next_node(self, time_limit: float) -> Optional[Tuple[Tuple[int, int], int]]:
        if not self._no_path and not self._found_path:
            self._run(time_limit)
        
        if self._no_path:
            return None
        
        if self._found_path:
            value, (x, y, dir), cost = self._heap.pop_push_min()
            position = (x, y)
            log(f'found\tlast: {position} {cost}')
            prev_position, prev_cost = position, cost
            while position != self._position:
                prev_position, prev_cost = position, cost
                position, cost = self._traversing[(position, cost)]
            
            self._position = position
            self._distance_from_start = cost
            return prev_position, prev_cost


width, height = [int(i) for i in input().split()]
start_column, start_row, goal_column, goal_row = [int(i) for i in input().split()]
_open = int(input())  # number of open tiles on the map
tiles_data = []
for i in range(_open):
    tiles_data.append([int(j) for j in input().split()])

jps = JPS(
    height=height,
    width=width,
    start_column=start_column,
    start_row=start_row,
    goal_column=goal_column,
    goal_row=goal_row,
    tiles_data=tiles_data
)
# In order of nodes visited by the JPS+ algorithm, a line containing "nodeColumn nodeRow parentColumn parentRow givenCost".
jps.find_next_node(1)
print(f'{start_column} {start_row} -1 -1 0.00')

# game loop
while True:

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    next_node = jps.find_next_node(0.05)
    if next_node is None:
        print('NO PATH')
    else:
        position, distance_from_start = next_node
        print(f'{position[0]} {position[1]} {jps._position[0]} {jps._position[1]} {distance_from_start}')
    if jps._found_path:
        break
    # In order of nodes visited by the JPS+ algorithm, a line containing "nodeColumn nodeRow parentColumn parentRow givenCost".
    # print("3 4 0 2 3.14")
