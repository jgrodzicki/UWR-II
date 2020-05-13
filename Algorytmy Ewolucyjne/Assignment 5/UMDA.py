import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt

class UMDA:
    
    def __init__(self, d, N, no_sample, F, max_iters=1000):
        self.d = d
        self.N = N
        self.no_sample = no_sample
        self.F = F
        self.max_iters = max_iters
        
    
    def run(self, verbose=False, with_tqdm=True):
        if with_tqdm:
            range_ = trange(self.max_iters, desc='UMDA', position=0, leave=True)
        else:
            range_ = range(self.max_iters)
            
        self.best_ind = np.zeros(self.d)
        self.best_eval = 0
        self.max_evals = np.zeros(self.max_iters)
        self.mean_evals = np.zeros(self.max_iters)
        self.min_evals = np.zeros(self.max_iters)
            
        p = np.full(self.d, 0.5)
        pop = self._random_population(p)
        evals = self.F(pop)
        self.best_ind = pop[np.argmax(evals)]
        
        for it in range_:
            sample_pop = self._sample_pop(pop, evals)
            p = self._model_estimation(sample_pop)
            pop = self._random_population(p)
            evals = self.F(pop)
            
            self.max_evals[it] = np.max(evals)
            self.mean_evals[it] = np.mean(evals)
            self.min_evals[it] = np.min(evals)
            
            if self.max_evals[it] > self.best_eval:
                self.best_eval = self.max_evals[it]
                self.best_ind = pop[np.argmax(evals)]
    
    
    def plot_evals(self):
        plt.figure()
        plt.title('UMDA')
        plt.plot(range(self.max_iters), self.max_evals, c='g', linewidth=0.5, label='Max')
        plt.plot(range(self.max_iters), self.mean_evals, c='b', linewidth=0.5, label='Mean')
        plt.plot(range(self.max_iters), self.min_evals, c='r', linewidth=0.5, label='Min')
        plt.legend()
        plt.show()
        
        
    def _sample_pop(self, pop, evals):
        idxs = np.argsort(evals)[-self.no_sample:]
        return pop[idxs]
        
        
    def _model_estimation(self, sample_pop):
        return sample_pop.mean(axis=0)
    
    
    def _random_population(self, p):
        return np.array([np.where(np.random.random(self.d) < p, 1, 0) for _ in range(self.N)])
    
    
    