import sys
import math
import numpy as np  # type: ignore
from typing import List


def log(msg):
    print(msg, file=sys.stderr, flush=True)


class Distance:
    def __init__(self):
        self.N = self.NE = self.E = self.SE = self.S = self.SW = self.W = self.NW = 0
    
    def set_all(self, value: int) -> None:
        self.N = self.NE = self.E = self.SE = self.S = self.SW = self.W = self.NW = value
    
    def __repr__(self):
        return f'{self.N} {self.NE} {self.E} {self.SE} {self.S} {self.SW} {self.W} {self.NW}'


class Distances:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._distances = [[Distance() for _ in range(width)] for _ in range(height)]
    
    def find_distances(self, passable: np.ndarray) -> None:
        for y in range(self._height):
            for x in range(self._width):
                if passable[y][x]:
                    if y > 0:
                        self._distances[y][x].N = self._distances[y-1][x].N - 1
                    if x > 0:
                        self._distances[y][x].W = self._distances[y][x-1].W - 1
                    if x > 0 and y > 0:
                        if passable[y-1][x] and passable[y][x-1]:
                            self._distances[y][x].NW = self._distances[y-1][x-1].NW - 1
            
            for x in reversed(range(self._width-1)):
                if passable[y][x]:
                    self._distances[y][x].E = self._distances[y][x+1].E - 1
                    if y > 0:
                        if passable[y-1][x] and passable[y][x+1]:
                            self._distances[y][x].NE = self._distances[y-1][x+1].NE - 1
        
        for y in reversed(range(self._height-1)):
            for x in range(self._width):
                if passable[y][x]:
                    self._distances[y][x].S = self._distances[y+1][x].S - 1
                    
                    if x > 0:
                        if passable[y+1][x] and passable[y][x-1]:
                            self._distances[y][x].SW = self._distances[y+1][x-1].SW - 1
            
            for x in reversed(range(self._width-1)):
                if passable[y][x] and passable[y+1][x] and passable[y][x+1]:
                    self._distances[y][x].SE = self._distances[y+1][x+1].SE - 1
    
    def print_distances(self, passable: np.ndarray) -> None:
        for x in range(self._width):
            for y in range(self._height):
                if passable[y][x]:
                    print(x, y, self._distances[y][x])
            

# Compute the proper wall / jump point distances, according to the preprocessing phase of the JPS+ algorithm.

# width: Width of the map
# height: Height of the map
width, height = [int(i) for i in input().split()]
passable = np.full((height, width), True)
for i in range(height):
    inp = input()  # A single row of the map consisting of passable terrain ('.') and walls ('#')
    passable[i, np.where(np.array(list(inp)) == '#')] = False

distances = Distances(width=width, height=height)
distances.find_distances(passable=passable)
distances.print_distances(passable=passable)
