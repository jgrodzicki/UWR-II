import sys
import math
import numpy as np  # type: ignore
from typing import List
from collections import deque


def log(msg):
    print(msg, file=sys.stderr, flush=True)


class Distance:
    def __init__(self):
        self.N = self.NE = self.E = self.SE = self.S = self.SW = self.W = self.NW = 0
        self._was_set = {dir: False for dir in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']}
    
    def set_all(self, value: int) -> None:
        self.N = self.NE = self.E = self.SE = self.S = self.SW = self.W = self.NW = value
    
    def __repr__(self):
        return f'{self.N} {self.NE} {self.E} {self.SE} {self.S} {self.SW} {self.W} {self.NW}'
    
    def set(self, var: str, value: int) -> None:
        if self._was_set[var]:
            return
        self.__dict__[var] = value
        self._was_set[var] = True
        
    def get(self, var: str) -> int:
        return self.__dict__[var]


class Distances:
    def __init__(self, width: int, height: int, passable: np.ndarray) -> None:
        self._width = width
        self._height = height
        self._passable = passable
        self._distances = [[Distance() for _ in range(width)] for _ in range(height)]
    
    def find_distances(self) -> None:
        
        # Primary and straight jump points.
        prim_str_jump_points = set()
        for y, x in np.c_[np.nonzero(~self._passable)]:
            if x - 1 >= 0:
                self._distances[y][x - 1].set('E', 0)
                self._distances[y][x - 1].set('NE', 0)
                self._distances[y][x - 1].set('SE', 0)
                prim_str_jump_points.add((x-1, y))
                for y1 in range(y, -1, -1):
                    if not self._passable[y1, x - 1]:
                        break
                    self._distances[y1][x - 1].set('S', y - y1 + 1)
                    prim_str_jump_points.add((x-1, y1))
                for y1 in range(y, self._height):
                    if not self._passable[y1, x - 1]:
                        break
                    self._distances[y1][x - 1].set('N', y1 - y + 1)
                    prim_str_jump_points.add((x-1, y1))
            if x + 1 < self._width:
                self._distances[y][x + 1].set('W', 0)
                self._distances[y][x + 1].set('NW', 0)
                self._distances[y][x + 1].set('SW', 0)
                prim_str_jump_points.add((x+1, y))
                for y1 in range(y, -1, -1):
                    if not self._passable[y1, x + 1]:
                        break
                    self._distances[y1][x + 1].set('S', y - y1 + 1)
                    prim_str_jump_points.add((x+1, y1))
                for y1 in range(y, self._height):
                    if not self._passable[y1, x + 1]:
                        break
                    self._distances[y1][x + 1].set('N', y1 - y + 1)
                    prim_str_jump_points.add((x+1, y1))
            if y - 1 >= 0:
                self._distances[y - 1][x].set('S', 0)
                self._distances[y - 1][x].set('SE', 0)
                self._distances[y - 1][x].set('SW', 0)
                prim_str_jump_points.add((x, y-1))
                for x1 in range(x, -1, -1):
                    if not self._passable[y - 1, x1]:
                        break
                    self._distances[y - 1][x1].set('E', x - x1 + 1)
                    prim_str_jump_points.add((x1, y-1))
                for x1 in range(x, self._width):
                    if not self._passable[y - 1, x1]:
                        break
                    self._distances[y - 1][x1].set('W', x1 - x + 1)
                    prim_str_jump_points.add((x1, y-1))
            if y + 1 < self._width:
                self._distances[y + 1][x].set('N', 0)
                self._distances[y + 1][x].set('NE', 0)
                self._distances[y + 1][x].set('NW', 0)
                prim_str_jump_points.add((x, y+1))
                for x1 in range(x, -1, -1):
                    if not self._passable[y + 1, x1]:
                        break
                    self._distances[y + 1][x1].set('E', x - x1 + 1)
                    prim_str_jump_points.add((x1, y+1))
                for x1 in range(x, self._width):
                    if not self._passable[y + 1, x1]:
                        break
                    self._distances[y + 1][x1].set('W', x1 - x + 1)
                    prim_str_jump_points.add((x1, y+1))
            
        # Diagonal jump points.
        diag_dists = dict()
        for x, y in prim_str_jump_points:
            log(f'{x} {y} ')
            for xd, yd, dir in [(-1, -1, 'SE'), (-1, 1, 'NE'), (1, -1, 'SW'), (1, 1, 'NW')]:
                dist = 0
                new_x, new_y = x, y
                while True:
                    dist += 1
                    new_x, new_y = new_x+xd, new_y+yd
                    if (0 <= new_x < self._width and
                        0 <= new_y < self._height and
                        (self._distances[y][x].get(dir[0]) != 0 or self._distances[y][x].get(dir[1]) != 0) and
                        self._distances[new_y][new_x].get(dir) == 0
                    ):
                        state = (new_x, new_y, dir)
                        if state not in diag_dists:
                            diag_dists[state] = dist
                        else:
                            diag_dists[state] = min(diag_dists[state], dist)
                    else:
                        break
        for (x, y, dir), dist in diag_dists.items():
            self._distances[y][x].set(dir, dist)
        
        for y, x in np.c_[np.nonzero(~self._passable)]:
            self._distances[y][x].set_all(1)  # So distances for around the walls are 0

        for y in range(1, self._height):
            for x in range(1, self._width):
                if self._passable[y, x]:
                    self._distances[y][x].set('N', self._distances[y - 1][x].N - 1)
                    self._distances[y][x].set('NW', self._distances[y - 1][x - 1].NW - 1)
                    self._distances[y][x].set('W', self._distances[y][x - 1].W - 1)
    
            for x in range(self._width - 2, -1, -1):
                if self._passable[y, x]:
                    self._distances[y][x].set('N', self._distances[y - 1][x].N - 1)
                    self._distances[y][x].set('NE', self._distances[y - 1][x + 1].NE - 1)
                    self._distances[y][x].set('E', self._distances[y][x + 1].E - 1)

        for y in range(self._height-2, -1, -1):
            for x in range(1, self._width):
                if self._passable[y, x]:
                    self._distances[y][x].set('S', self._distances[y + 1][x].S - 1)
                    self._distances[y][x].set('SW', self._distances[y + 1][x - 1].SW - 1)
                    self._distances[y][x].set('W', self._distances[y][x - 1].W - 1)
    
            for x in range(self._width - 2, -1, -1):
                if self._passable[y, x]:
                    self._distances[y][x].set('S', self._distances[y + 1][x].S - 1)
                    self._distances[y][x].set('SE', self._distances[y + 1][x + 1].SE - 1)
                    self._distances[y][x].set('E', self._distances[y][x + 1].E - 1)


    def print_distances(self) -> None:
        for x in range(self._width):
            for y in range(self._height):
                if self._passable[y][x]:
                    print(x, y, self._distances[y][x])
            

# Compute the proper wall / jump point distances, according to the preprocessing phase of the JPS+ algorithm.

# width: Width of the map
# height: Height of the map
width, height = [int(i) for i in input().split()]
passable = np.full((height, width), True)
for i in range(height):
    inp = input()  # A single row of the map consisting of passable terrain ('.') and walls ('#')
    passable[i, np.where(np.array(list(inp)) == '#')] = False

distances = Distances(width=width, height=height, passable=passable)
distances.find_distances()
distances.print_distances()
