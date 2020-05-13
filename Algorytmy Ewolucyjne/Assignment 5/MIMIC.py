from tqdm import trange
import matplotlib.pyplot as plt
import numpy as np

class MIMIC:
    
    def __init__(self, N, d, domain, epsilon, cost_func, max_iters=1000):
        self.N = N
        self.d = d
        self.domain = domain
        self.epsilon = epsilon
        self.cost_func = cost_func
        max_iters = min(max_iters, int(0.5/self.epsilon))
        self.max_iters = max_iters
    
    
    def run(self, verbose=False, with_tqdm=True):
        self.max_cost, self.mean_cost, self.min_cost = np.zeros(self.max_iters), np.zeros(self.max_iters), np.zeros(self.max_iters)
        theta = 0.5
        
        possible_v = np.array([np.full(self.d, v) for v in np.arange(self.domain[0], self.domain[1]+1e-10)])
        
        if with_tqdm:
            range_ = trange(self.max_iters, desc='MIMIC', position=0, leave=True)
        else:
            range_ = range(self.max_iters)
        
        pop = self._random_population(possible_v)
        costs = self.cost_func(pop)
        self.best_ind = pop[np.argmin(costs)]
        best_cost = costs.min()
        
        for it in range_:
            sample_pop, sample_ev = self._sample(pop, costs, theta)
            pop = self._random_population(sample_pop)
            costs = self.cost_func(pop)
            theta -= self.epsilon
            
            self.max_cost[it] = costs.max()
            self.mean_cost[it] = costs.mean()
            self.min_cost[it] = costs.min()
            
            if self.min_cost[it] < best_cost:
                self.best_ind, best_cost = pop[np.argmin(costs)], self.min_cost[it]
                
            if verbose and it%50 == 0:
                print(f'{it} / {self.max_iters},\tmin: {self.min_cost[it]}\tmean: {self.mean_cost[it]}\tmax: {self.max_cost[it]}')
            
    
    def plot_costs(self, extra_title):
        plt.figure()
        plt.title(f'MIMIC cost function {extra_title}')
        plt.plot(self.max_cost, c='r', label='max')
        plt.plot(self.mean_cost, c='b', label='mean')
        plt.plot(self.min_cost, c='g', label='min')
        plt.legend()
        plt.show()
        
    
    def _sample(self, pop, costs, theta):
        idxs = np.argsort(costs)[:int(theta*self.N)]
        return pop[idxs], costs[idxs]
    
    
    def _random_population(self, possible_v):
        pop = np.zeros((self.N, self.d))
        for c in range(self.d):
            pop[:, c] = np.random.choice(possible_v[:, c], size=self.N)
        return pop
    