from collections import deque
import sys
import math
import numpy as np  # type: ignore
import time
from typing import List, Tuple, Set, Deque, Dict

# Remove connected regions of the same color to obtain the best score.


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


class Agent:
    def __init__(self) -> None:
        self._map = np.zeros((15, 15))
        pass
    
    def move(self) -> None:
        pass
    
    def load_map(self) -> None:
        for i in range(15):
            self._map[i] = np.array(list(map(int, input().split())))
    
    def find_move_seq(self, max_time: float) -> List[Tuple[int, int]]:
        st_time = time.time()
        q: Deque = deque()
        q.append((0, self._map.copy(), []))
        best_score, best_move_seq = -1, []
        cnt = 0
        while q and time.time() - st_time < max_time:
            cur_score, cur_map, cur_move_seq = q.popleft()
            cnt += 1
            if np.all(cur_map == -1):
                break
            groups = self._find_groups(cur_map)
            for x, y in groups.keys():
                score = self._get_score(x, y, groups)
                new_score = cur_score + score
                new_map = self._simulate_move(cur_map.copy(), x, y, groups)
                new_move_seq = cur_move_seq + [(x, y)]
                if new_score > best_score:
                    best_score, best_move_seq = new_score, new_move_seq
                
                q.append((new_score, new_map, new_move_seq))
        log(f'analyzed {cnt}')
        return best_move_seq
    
    def _get_score(self, x: int, y: int, group_coords: Dict[Tuple[int, int], Set]):
        number_of_tiles_removes = len(group_coords[(x, y)])
        score = (number_of_tiles_removes-2)**2
        return score
    
    def _find_groups(self, map: np.ndarray) -> Dict[Tuple[int, int], Set]:
        """
        Finds groups, returning a dict where a point from the group is a key and value is a set of point from this
        group.
        """
        group_coords = dict()
        
        visited = set()
        for y in range(15):
            for x in range(15):
                if (x, y) in visited or map[y, x] == -1:
                    continue
                visited.add((x, y))
                q: Deque = deque()
                q.append((x, y))
                number_visited = 1
                color = map[y, x]
                from_group = {(x, y)}
                while q:
                    cur_x, cur_y = q.popleft()
                    for xd, yd in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_x, new_y = cur_x+xd, cur_y+yd
                        if (
                            0 <= new_x < 15 and
                            0 <= new_y < 15 and
                            (new_x, new_y) not in visited and
                            map[new_y, new_x] == color
                        ):
                            number_visited += 1
                            q.append((new_x, new_y))
                            visited.add((new_x, new_y))
                            from_group.add((new_x, new_y))
                if number_visited >= 2:
                    group_coords[(x, y)] = from_group
        return group_coords
    
    @staticmethod
    def _simulate_move(map: np.ndarray, x: int, y: int, group_coords: Dict[Tuple[int, int], Set]) -> np.ndarray:
        """
        Moves tiles down and left after removing given group.
        """
        # indices_to_remove = tuple(np.array(list(group_coords[(x, y)])).T)[::-1]
        # map[indices_to_remove] = -1
        x_indices_to_remove, y_indices_to_remove = [], []
        for x, y in group_coords[(x, y)]:
            x_indices_to_remove.append(x)
            y_indices_to_remove.append(y)
        map[y_indices_to_remove, x_indices_to_remove] = -1
        moved_map = Agent.move_down_left(map=map)
        return moved_map
    
    @staticmethod
    def move_down_left(map: np.ndarray) -> np.ndarray:
        new_map = np.full_like(map, -1)
    
        # Drop down.
        for i, col in enumerate(map.T):
            nonempty_idxs = np.flatnonzero(col != -1)
            if len(nonempty_idxs) == 0:
                new_map[:, i] = -1
                continue
            nonempty_elems = col[nonempty_idxs]
            new_map[-len(nonempty_elems):, i] = nonempty_elems
    
        # Empty columns.
        col_sum = new_map.sum(axis=0)
        nonempty_cols = (col_sum != -map.shape[1])
        number_nonempty_cols = np.count_nonzero(nonempty_cols)
        new_map[:, :number_nonempty_cols] = new_map[:, np.flatnonzero(nonempty_cols)]
        new_map[:, number_nonempty_cols:] = -1
    
        return new_map


def test_move_down_left():
    map_1 = np.array([
        [0, 0, 0],
        [-1, -1, -1],
        [0, 0, 0]
    ])
    expected_1 = np.array([
        [-1, -1, -1],
        [0, 0, 0],
        [0, 0, 0]
    ])
    assert np.all(Agent.move_down_left(map_1) == expected_1)
    
    map_2 = np.array([
        [0, -1, 0],
        [0, -1, 0],
        [0, -1, 0]
    ])
    expected_2 = np.array([
        [0, 0, -1],
        [0, 0, -1],
        [0, 0, -1]
    ])
    assert np.all(Agent.move_down_left(map_2) == expected_2)
    
    map_3 = np.array([
        [0, -1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ])
    expected_3 = map_3
    assert np.all(Agent.move_down_left(map_3) == expected_3)
    
    
if __name__ == '__main__':
    # test_move_down_left()

    agent = Agent()
    is_first_move = True
    move_seq: List[Tuple[int, int]] = []
    expected_map = None

    while True:
        agent.load_map()
        if expected_map is not None:
            if not np.all(agent._map == expected_map):
                log(f'real:\n{agent._map}')
                log(f'simulated:\n{expected_map}')
                assert False
        if is_first_move or len(move_seq) == 0:
            move_seq = agent.find_move_seq(max_time=19 if is_first_move else 0.05)
            is_first_move = False
        # log(str(agent._map))
        # log(str(move_seq))
        # log(str(agent._find_groups(agent._map)))
        x, y = move_seq[0]
        move_seq = move_seq[1:]
        print(f'{x} {14-y}')
        expected_map = agent._simulate_move(agent._map.copy(), x, y, agent._find_groups(agent._map))
