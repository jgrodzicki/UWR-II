from typing import List, NamedTuple, Optional, Tuple, Union
import numpy as np  # type: ignore
import sys
import time
# import matplotlib.pyplot as plt

LandingSpot = NamedTuple('LandingSpot', (('start', int), ('end', int), ('height', int)))
Position = NamedTuple('Position', (('x', int), ('y', int)))
# Move = NamedTuple('Move', (('rotation', int), ('power', int)))


MINUS_FOR_CRASH = 1e6
MINUS_FOR_BEING_IN_AIR = 0


def log(msg):
    print(msg, file=sys.stderr)


class Game:
    def __init__(self) -> None:
        self.surface: Union[List[int], np.ndarray] = []
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

            for y in np.linspace(points[i-1][1], points[i][1]+1, points[i][0] - points[i-1][0]):
                y = round(int(y))
                self.surface.append(y)
        self.surface = np.array(self.surface)

    def is_alive(self) -> bool:
        return (0 <= self.x < 7000 and
                0 <= self.y < 3000 and
                0 <= self.fuel_left)

    def on_ground(self, x: float, y: float) -> bool:
        return y <= self.surface[round(int(x))]

    def landed_successfully(self) -> bool:
        assert self.landing_spot is not None

        return (
            self.on_ground(self.x, self.y) and
            self.landing_spot.start <= self.x <= self.landing_spot.end and
            self.rotation == 0 and
            abs(self.v_speed) <= 40 and
            abs(self.h_speed) <= 20
        )

    def hit_surface(self, prev_x: float, prev_y: float) -> bool:
        # if self.x == prev_x:
        #     return False
        # if np.all(self.surface[int(min(prev_x, self.x)):int(max(prev_x, self.x))] > min(prev_y, self.y)):
        #     return False
        # xs = [x for x in range(int(prev_x), int(self.x), -1 if prev_x > self.x else 1)]
        # for x, y in zip(xs, np.linspace(prev_y, self.y, len(xs))):
        #     if self.surface[int(x)] >= y:
        #         return True
        # return False
        return False

    def get_input(self) -> None:
        self.x, self.y, self.h_speed, self.v_speed, self.fuel_left, self.rotation, self.power = list(map(int, input().split()))

    def update(self) -> None:
        prev_x, prev_y = self.x, self.y
        self.x += self.h_speed
        self.y += self.v_speed

        self.v_speed += self.G

        self.fuel_left -= self.power

        # update speeds
        rotation_radians = self.rotation * np.pi / 180
        self.v_speed += np.cos(rotation_radians) * self.power
        self.h_speed += -np.sin(rotation_radians) * self.power

        if not self.is_alive() or self.on_ground(x=self.x, y=self.y) or self.hit_surface(prev_x=prev_x, prev_y=prev_y):
            self.is_in_air = False

    def make_move(self, rotation: int, power: int) -> None:
        self.rotation = max(min(90, self.rotation+rotation), -90)
        self.power = max(min(4, self.power+power), 0)

    def evaluate_population(self, population: np.ndarray) -> np.ndarray:
        """
        Evaluate by checking if landed on the spot
        """
        evals = []

        og_state = self.x, self.y, self.h_speed, self.v_speed, self.fuel_left, self.rotation, self.power, self.is_in_air
        for individual in population:
            self.x, self.y, self.h_speed, self.v_speed, self.fuel_left, self.rotation, self.power, self.is_in_air = og_state

            eval = 0

            while len(individual) and self.is_in_air:
                rotation, power = individual[:2]
                individual = individual[2:]

                self.make_move(rotation, power)
                self.update()

            if (not self.landing_spot.start + 50 < self.x < self.landing_spot.end - 50 or
                abs(not self.landing_spot.height - self.y) < 50
            ):
                eval -= (abs((self.landing_spot.start+self.landing_spot.end)/2 - self.x) + abs(self.landing_spot.height - self.y)) * 2
            if abs(self.v_speed) > 30:  # for safety margin
                eval -= (abs(self.v_speed) - 0)**2
            if abs(self.h_speed) > 15:
                eval -= (abs(self.h_speed) - 0)**2
            # if abs(self.rotation) != 0:
            #     eval -= abs(self.rotation)

            if not self.is_alive() or not self.landed_successfully():
                eval -= MINUS_FOR_CRASH
            if self.is_alive():
                eval -= MINUS_FOR_BEING_IN_AIR
            evals.append(eval)

        self.x, self.y, self.h_speed, self.v_speed, self.fuel_left, self.rotation, self.power, self.is_in_air = og_state

        return np.array(evals)

    def do_moves(self, individual: np.ndarray) -> None:
        while len(individual) and self.is_in_air:
            rotation, power = individual[:2]
            individual = individual[2:]

            self.make_move(rotation, power)
            self.update()

    # def plot_population(self, population: np.ndarray) -> None:
    #     og_state = self.x, self.y, self.h_speed, self.v_speed, self.fuel_left, self.rotation, self.power, self.is_in_air
    #
    #     plt.xlim(0, 7000)
    #     plt.ylim(0, 3000)
    #     plt.plot(self.surface, c='black')
    #     plt.plot([self.landing_spot.start, self.landing_spot.end], [self.landing_spot.height]*2, c='g', linewidth=4)
    #
    #     plt.scatter(self.x, self.y, s=20, c='r')
    #
    #     from tqdm import tqdm
    #     for individual in tqdm(population):
    #         self.x, self.y, self.h_speed, self.v_speed, self.fuel_left, self.rotation, self.power, self.is_in_air = og_state
    #
    #         while self.is_in_air:
    #             rotation, power = individual[:2]
    #             individual = individual[2:]
    #             self.make_move(rotation, power)
    #             self.update()
    #             plt.scatter(self.x, self.y, s=5, c='b', alpha=0.3)
    #     plt.show()


class RandomAgent:
    def __init__(self) -> None:
        pass

    def _select_action(self) -> Tuple[int, int]:
        rotation = np.random.randint(-3, 4) * 5
        power = np.random.randint(-1, 2)
        return rotation, power


class ES:
    def __init__(self, population_size: int, chromosome_length: int, mutation_prob=0.1) -> None:
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.mutation_prob = mutation_prob
        self.population = None

    def _random_population(self) -> np.ndarray:
        rotations = np.random.randint(-3, 4, self.population_size * self.chromosome_length) * 5
        powers = np.random.randint(0, 2, self.population_size * self.chromosome_length)
        return np.c_[rotations, powers].reshape(self.population_size, -1)

    def mutate(self, population: np.ndarray) -> np.ndarray:
        y_idxs, x_idxs = np.where(np.random.random((population.shape[0], self.chromosome_length)) <= self.mutation_prob)
        population[y_idxs, 2 * x_idxs] = np.random.randint(-3, 4, len(y_idxs)) * 5
        population[y_idxs, 2 * x_idxs + 1] = np.random.randint(-1, 2, len(y_idxs))

        return population

    def parent_selection(self, population: np.ndarray, evals: np.ndarray) -> np.ndarray:
        norm_evals = evals - np.min(evals)
        if np.sum(norm_evals) == 0:
            norm_evals += 1/len(norm_evals)
        else:
            norm_evals = norm_evals / np.sum(norm_evals)

        idxs = np.random.choice(self.population_size, size=self.population_size//2, p=norm_evals)
        return population[idxs].copy()

    def population_selection(
        self,
        population: np.ndarray,
        evals: np.ndarray,
        children: np.ndarray,
        children_evals: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        all_population = np.vstack((population, children))
        all_evals = np.append(evals, children_evals)
        idxs = np.argsort(all_evals)[-self.population_size:]
        return all_population[idxs], all_evals[idxs]

    def run(self, game: Game, time_limit=0.08):
        start_time = time.time()

        if self.population is None:
            self.population = self._random_population()
            self.evals = game.evaluate_population(self.population)
        else:
            self.population = self.population[:, 2:]
            to_append = []

            og_state = game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power, game.is_in_air

            for i, individual in enumerate(self.population):
                game.do_moves(individual)
                after_ind_state = game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power, game.is_in_air

                best_eval, best_rot, best_pow = -np.inf, None, None

                for rot in [-15, -10, -5, 0, 5, 10, 15]:
                    for pow in [-1, 0, 1]:
                        game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power, game.is_in_air = after_ind_state
                        eval = game.evaluate_population(np.array([[rot, pow]]))[0]
                        if eval > best_eval:
                            best_eval, best_rot, best_pow = eval, rot, pow

                # self.population[i] = np.append(self.population[i], [best_rot, best_pow])
                to_append.append([best_rot, best_pow])
                self.evals[i] = best_eval

                game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power, game.is_in_air = og_state

            self.population = np.hstack((self.population, to_append))
            assert self.population.shape == (self.population_size, 2*self.chromosome_length)

        cnt = 0
        while time.time() - start_time < time_limit:
            cnt += 1
            parents = self.parent_selection(self.population, self.evals)
            children = self.mutate(parents)
            children_evals = game.evaluate_population(children)
            self.population, self.evals = self.population_selection(self.population, self.evals, children, children_evals)

        log(f'Done iters: {cnt}')
        log(f'Best eval: {np.max(self.evals)}')
        return self.population[np.argmax(self.evals)], np.max(self.evals)


# class RHEA(ES):
#     def __init__(self, population_size: int, chromosome_length: int, mutation_prob: float=0.1) -> None:
#         super(RHEA, self).__init__(population_size, chromosome_length, mutation_prob)
#         self.



if __name__ == '__main__':
    '''Code for running in Codingame'''
    game = Game()
    game.load_map()
    st = time.time()
    es = ES(population_size=20, chromosome_length=80, mutation_prob=0.05)

    game.get_input()
    best_ind, best_ind_eval = es.run(game, time_limit=0.98)

    rotation, power = best_ind[:2]
    best_ind = best_ind[2:]

    rotation = max(min(90, game.rotation + rotation), -90)
    power = max(min(4, game.power + power), 0)

    print(rotation, power)

    while game.is_in_air and len(best_ind):
        # state = game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power
        if best_ind_eval > -MINUS_FOR_BEING_IN_AIR:
            input()
        else:
            game.get_input()

        game_rotation, game_power = game.rotation, game.power

        if best_ind_eval < -MINUS_FOR_BEING_IN_AIR:
            best_ind, best_ind_eval = es.run(game)
        else:
            log(f'optimal: {best_ind[:10]}')
            # game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power = state

        rotation, power = best_ind[:2]
        best_ind = best_ind[2:]
        raw_rotation = rotation

        # log(f'raw rotation: {rotation}')
        #

        if best_ind_eval > -MINUS_FOR_BEING_IN_AIR:
            game.make_move(rotation, power)
            game.update()
            log(f'raw rotation: {raw_rotation}')
            log(f'{" ".join(map(lambda f: str(round(int(f))), [game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power]))}')

        # og_state = game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power, game.is_in_air
        # game.make_move(rotation, power)
        # if not game.is_in_air:
        #     rotation = 0
        #
        # game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power, game.is_in_air = og_state

        rotation = max(min(90, game_rotation + rotation), -90)
        power = max(min(4, game_power + power), 0)

        print(rotation, power)


    '''Profile times'''
    # game = Game()
    # points = [[0, 100], [1000, 500], [1500, 1500], [3020, 1000], [4000, 150], [5500, 150], [6999, 800]]
    # for i in range(1, len(points)):
    #     if points[i-1][1] == points[i][1]:
    #         game.landing_spot = LandingSpot(start=points[i-1][0], end=points[i][0], height=points[i][1])
    #
    #     for y in np.linspace(points[i-1][1], points[i][1], points[i][0] - points[i-1][0]):
    #         y = int(y)
    #         game.surface.append(y)
    #
    # rhea = RHEA(population_size=100, chromosome_length=100)
    # game.plot_population(rhea.population)

    # start = time.time()

    # cnt = 0
    # iters = []
    # t0 = t1 = t2 = t3 = t4 = 0

    # while time.time() - start < 1:
    #     st = time.time()
    #     rhea = RHEA(population_size=100, chromosome_length=0 + 100)
    #     t0 += time.time() - st
    #
    #     cnt += 1
    #     game.x = 5000
    #     game.y = 2700
    #     game.h_speed = game.v_speed = game.rotation = game.power = 0
    #     game.fuel_left = 550
    #     game.is_in_air = True
    #
    #     it = 0
    #     while game.is_in_air:
    #         st = time.time()
    #         rotation, power = rhea.select_move()
    #         t1 += time.time() - st
    #         st = time.time()
    #         game.make_move(rotation, power)
    #         t2 += time.time() - st
    #         st = time.time()
    #         game.update()
    #         t3 += time.time() - st
    #         it += 1
    #
    #     iters.append(it)
    #
    # print(cnt)
    # print(np.min(iters), np.mean(iters), np.max(iters))
    # print(t0, t1, t2, t3, t4)


    '''Step by step plot for 1 individual'''
    # game.x = 5000
    # game.y = 2500
    #
    # import matplotlib.pyplot as plt
    # import matplotlib.animation as animation
    #
    # rhea = RHEA(population_size=100, chromosome_length=100)
    #
    # fig, ax = plt.subplots()
    # ax.set_xlim(0, 7000)
    # ax.set_ylim(0, 3000)
    # lander = ax.scatter(game.x, game.y, c='r')
    # path = [[game.x], [game.y]]
    # lander_path,  = ax.plot(path, linestyle='--', c='r')
    # surface = ax.plot(game.surface)
    # landing = ax.plot([game.landing_spot.start, game.landing_spot.end], [game.landing_spot.height]*2, c='g', linewidth=4)
    #
    # while game.is_in_air:
    #     rotation, power = rhea.select_move()
    #     game.make_move(rotation, power)
    #     game.update()
    #     # print('\t'.join(list(map(lambda x: str(int(x)), [game.x, game.y, game.h_speed, game.v_speed, game.fuel_left, game.rotation, game.power]))))
    #
    #     lander.set_offsets(np.c_[game.x, game.y])
    #
    #     path[0].append(game.x)
    #     path[1].append(game.y)
    #     lander_path.set_data(path)
    #     plt.pause(0.05)
    #
    # plt.show()