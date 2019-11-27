import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from os import system
import time


class Game_of_live:
    def __init__(self, n):
        self.n = n
        self.board = np.random.randint(2, size=(n, n))

    def draw(self):
        system('clear')
        for r in self.board:
            print(r)
        
    def count_alive_neighs(self, x, y):
        min_x, max_x = max(0, x-1), min(self.n-1, x+1)
        min_y, max_y = max(0, y-1), min(self.n-1, y+1)
        res = 0

        for x1 in range(min_x, max_x+1):
            for y1 in range(min_y, max_y+1):
                if x1 == x and y1 == y:
                    continue
                res += self.board[y1][x1]
        return res
    
    def next_board(self):
        new_board = self.board*0
        for y, row in enumerate(self.board):
            for x, e in enumerate(row):
                alive_neighs = self.count_alive_neighs(x, y)
                if e:
                    if 2 <= alive_neighs <= 3:
                        new_board[y][x] = 1
                    else:
                        new_board[y][x] = 0
                else:
                    if alive_neighs == 3:
                        new_board[y][x] = 1
                    else:
                        new_board[y][x] = 0
        self.board = new_board
        return new_board
    
    def run(self):
        while True:
            self.next_board()
            self.draw()
            time.sleep(1)

                

g = Game_of_live(10)
g.run()

