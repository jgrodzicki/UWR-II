from tqdm import trange
import matplotlib.pyplot as plt
import numpy as np


class CGA:
    
    def __init__(self, d, F, theta=None, max_iters=1000):
        self.d = d
        self.F = F
        self.theta = theta
        if self.theta is None:
            self.theta = 1/self.N
        self.max_iters = max_iters
        
    
    def run(self, with_tqdm=True):
        self.max_evals = np.zeros(self.max_iters)
        best_eval, self.best_ind = None, None
        
        p = np.full(self.d, 0.5)
        xs = self._random_xs(p)
        evals = self.F(xs)
        if evals[0] > evals[1]:
            best_eval, self.best_ind = evals[0], xs[0]
        else:
            best_eval, self.best_ind = evals[1], xs[1]
        
        if with_tqdm:
            range_ = trange(self.max_iters, desc='CGA', position=0, leave=True)
        else:
            range_ = range(self.max_iters)
            
        for it in range_:
            if evals[0] < evals[1]:
                xs[0], xs[1] = xs[1], xs[0]
                if evals[1] > best_eval:
                    best_eval, self.best_ind = evals[1], xs[1]
            elif evals[0] > best_eval:
                best_eval, self.best_ind = evals[0], xs[0]
                    
            
            p += np.where(xs[0] - xs[1] == 1, self.theta, 0)
            p -= np.where(xs[0] - xs[1] == -1, self.theta, 0)
            
            self.max_evals[it] = np.max(evals)
            
            xs = self._random_xs(p)
            evals = self.F(xs)
    
    
    def _random_xs(self, p):
        return np.array([np.where(np.random.random(self.d) < p, 1, 0) for _ in range(2)])