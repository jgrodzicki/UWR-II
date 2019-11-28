import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Game_of_live:
    def __init__(self, n):
        self.n = n
        self.board = np.random.randint(2, size=(n, n))
        
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

    def update(self, _):
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
        
        mat.set_data(self.board)
        return [mat]


if __name__ == "__main__":
    g = Game_of_live(10)
    fig, ax = plt.subplots()
    mat = ax.matshow(g.board)
    ani = animation.FuncAnimation(fig, g.update, interval=100)
    plt.show()
