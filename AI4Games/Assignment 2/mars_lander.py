from typing import List, NamedTuple, Optional, Tuple
import numpy as np  # type: ignore
import sys
import time

LandingSpot = NamedTuple('LandingSpot', (('start', int), ('end', int), ('height', int)))
Position = NamedTuple('Position', (('x', int), ('y', int)))
Move = NamedTuple('Move', (('rotation', int), ('power', int)))

def log(msg):
    print(msg, file=sys.stderr)

class Game:
    def __init__(self) ->  None:
        self.surface: List[int] = []
        self.landing_spot: Optional[LandingSpot] = None 
        self.x: float = 2500
        self.y: float = 2700
        self.fuel_left: int = 550
        self.h_speed: float = 0
        self.v_speed: float = 0
        self.rotation: int = 0
        self.power: int = 0
        self.is_in_air: bool = True
        
        self.G: float = -3.711
    
    
    def load_map(self) -> None:
        N = int(input())
        points = []
        for _ in range(N):
            x, y = list(map(int, input().split()))
            points.append((x, y))
            
        for i in range(1, len(points)):
            if points[i-1][1] == points[i][1]:
                self.landing_spot = LandingSpot(start=points[i-1][0], end=points[i][0], height=points[i][1])
            
            for y in np.linspace(points[i-1][1], points[i][1], points[i][0] - points[i-1][0]):
                y = int(y)
                self.surface.append(y)
    
    def is_alive(self) -> bool:
        return (0 <= self.x < 7000 and
                0 <= self.y < 3000 and
                -500 < self.h_speed < 500 and
                -500 < self.v_speed < 500 and
                0 <= self.fuel_left <= 2000 and
                -90 <= self.rotation <= 90 and
                0 <= self.power <= 4)
    
    def on_ground(self, x: float, y: float) -> bool:
        return y <= self.surface[int(x)]
    
    def on_landing_spot(self, position: Position) -> bool:
        assert self.landing_spot is not None
        
        return (self.on_ground(position.x, position.y) and 
                self.landing_spot.start <= position.x <= self.landing_spot.end and
                self.rotation == 0 and
                abs(self.v_speed) <= 40 and
                abs(self.h_speed) <= 20
        )
    
    def get_input(self) -> None:
        inp = input().split()
        log(len(inp))
        self.x, self.y, self.h_speed, self.v_speed, self.fuel, self.rotate, self.power = list(map(int, inp))
    
    def update(self) -> None:
        self.v_speed += self.G / 2
        self.x += self.h_speed
        self.y += self.v_speed
        
        self.fuel_left -= self.power
        
        # update speeds
        self.v_speed += abs(np.cos(self.rotation)) * self.power
        self.h_speed += -np.sin(self.rotation) * self.power
        
        if not self.is_alive():
            self.is_in_air = False
            return
        
        if self.on_ground(x=self.x, y=self.y):
            self.is_in_air = False
    
    def make_move(self, move) -> None:
        self.rotation = move.rotation
        self.power = move.power
    

class RandomAgent:
    def __init__(self) -> None:
        pass
    
    def _select_action(self, rotation, power) -> Move:
        rotation = np.random.randint(max(-90, rotation-15), min(90, rotation+15)+1)
        power = np.random.randint(max(0, power-1), min(4, power+1)+1)
        return Move(rotation=rotation, power=power)



if __name__=='__main__':
    game = Game()
    game.load_map()
    start = time.time()
    
    agent = RandomAgent()
    
    cnt = 0
    iters = []
    while time.time() - start < 0.1:
        cnt += 1
        game.x = 2500
        game.y = 2700
        game.h_speed = game.v_speed = game.rotation = game.power = 0
        game.fuel_left = 550
        game.is_in_air = True
        
        it = 0
        while game.is_in_air:
            move = agent._select_action(game.rotation, game.power)
            game.make_move(move)
            game.update()
            it += 1
        iters.append(it)
    print(cnt)
    print(np.min(iters), np.mean(iters), np.max(iters))
        
        
    # game.x = 3000
    # game.y = 2500
    
    # agent = RandomAgent()
    
    # import matplotlib.pyplot as plt
    # import matplotlib.animation as animation

    # fig, ax = plt.subplots()
    # ax.set_xlim(0, 7000)
    # ax.set_ylim(0, 3000)
    # lander = ax.scatter(game.x, game.y, c='r')
    # path = [[game.x], [game.y]]
    # lander_path,  = ax.plot(path, linestyle='--', c='r')
    # surface = ax.plot(game.surface)
    # landing = ax.plot([game.landing_spot.start, game.landing_spot.end], [game.landing_spot.height]*2, c='g', linewidth=4)
    
    # while game.is_in_air:
    #     move = agent._select_action()
    #     game.make_move(move)
    #     game.update()
    #     print('\t'.join(list(map(lambda x: str(int(x)), [game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power]))))
        
    #     lander.set_offsets(np.c_[game.x, game.y])
        
    #     path[0].append(game.x)
    #     path[1].append(game.y)
    #     lander_path.set_data(path)
    #     plt.pause(0.05)
        
    # plt.show()