from tqdm import trange
import numpy as np
import matplotlib.pyplot as plt

class ES:
    def __init__(self, domain, dims, cost_func, tau, tau0, population_size=1000, offspring_size=500, parent_choice_method='roulette', replacement_method='mulambda', max_iters=1000):
        if type(domain) is tuple:
            self.domain = np.array([domain] * dims)
        else:
            self.domain = np.array(domain)
        self.dims = dims
        self.population_size = population_size
        self.offspring_size = offspring_size
        self.tau = tau
        self.tau0 = tau0
        self.cost_func = cost_func
        self.max_iters = max_iters
        
        assert offspring_size <= population_size, 'offspring size cannot be larger than population size'
        
        assert parent_choice_method in ['random', 'roulette'], 'parent choice method has to be either "random" or "roulette"'
        if parent_choice_method == 'random':
            self.parent_selection = self._random
        elif parent_choice_method == 'roulette':
            self.parent_selection = self._roulette_method
        
        assert replacement_method in ['mulambda', 'lambda'], 'replacement method has to be either "mulambda" or "lambda'
        if replacement_method == 'mulambda':
            self.replace = self._mulambda
        elif replacement_method == 'lambda':
            self.replace = self._lambda
        
    
    def run(self, verbose=False, with_tqdm=True, log_interv=50):
        if with_tqdm:
            range_ = trange(self.max_iters, position=0, leave=True)
        else:
            range_ = range(self.max_iters)
            
        self.iter_min, self.iter_mean, self.iter_max = [], [], []
        
        self._generate_population()
        costs = self.cost_func(self.population)
        self.best_ind, best_cost = self.population[np.argmin(costs)], costs.min()
        
        try:
            for iter_ in range_:
                parents = self.parent_selection(self.population, costs)[:, :]
                children = self.mutate(parents)
                children_costs = self.cost_func(children)
                self.population, costs = self.replace(self.population, costs, children, children_costs)
                
                self.iter_min.append(costs.min())
                self.iter_mean.append(costs.mean())
                self.iter_max.append(costs.max())
                
                if costs.min() < best_cost:
                    best_cost = costs.min()
                    self.best_ind = self.population[np.argmin(costs)]

                if verbose and iter_%log_interv == 0:
                    print(f'iter: {iter_},\tmin: {costs.min():.5},\tmean: {costs.mean():.5},\tmax: {costs.max():.5}')
        except KeyboardInterrupt:
            pass
        
        self.iter_min = np.array(self.iter_min)
        self.iter_mean = np.array(self.iter_mean)
        self.iter_max = np.array(self.iter_max)
        
    
    def history(self, glob_min=None, with_plot=False, with_text=True, title=None):
        if with_plot:
            plt.figure(figsize=(10, 6))
            idx = self.iter_min < 1e9
            plt.plot(np.arange(len(self.iter_min))[idx], self.iter_min[idx])
            if glob_min is not None:
                plt.plot(np.full(len(self.iter_min), glob_min), c='r')
            if title is not None:
                plt.title(title)
            plt.show()
        
        if with_text:
            print(f'\nBest cost function: {round(self.iter_min.min(), 5)} at iter: {np.argmin(self.iter_min)}')
    
    
    def _generate_population(self):
        pop = []
        for _ in range(self.population_size):
            pop.append(self._random_ind())
        self.population = np.array(pop)
    
    
    def mutate(self, pop):
        xs, sigmas = pop[:, 0], pop[:, 1]
        mutated = []
        
        for i in range(len(pop)):
            eps0 = np.random.normal(0, self.tau0)
            eps = np.random.normal(0, self.tau, size=self.dims)
            
            new_sigma = sigmas[i] * np.exp(eps0 + eps)
            new_x = xs[i] + np.random.normal(0, new_sigma, size=self.dims)
            
            its = 0
            while (np.any(new_x < self.domain[:,0]) or np.any(new_x > self.domain[:,1])) and its < 4:
                its += 1
                new_x = xs[i] + np.random.normal(0, new_sigma, size=self.dims)
            
            if (np.any(new_x < self.domain[:,0]) or np.any(new_x > self.domain[:,1])):
                new_x, new_sigma = self._random_ind()
            
            mutated.append(np.vstack((new_x, new_sigma)))
            
        return np.array(mutated)
    
    
    def _random_ind(self):
        x = np.random.uniform(self.domain[:,0], self.domain[:,1], size=self.dims)
        sigma = np.random.uniform(0.5, 2, size=self.dims)
        return np.vstack((x, sigma))
    
    
    def _roulette_method(self, pop, costs):
        if min(costs) == max(costs):
            idxs = np.random.choice(len(pop), size=self.offspring_size, replace=True)
        else:
            std_costs = (costs - min(costs)) / (costs - min(costs)).max()
            p_costs = (1 - std_costs)
            idxs = np.random.choice(len(pop), p=p_costs / sum(p_costs), size=self.offspring_size, replace=True)
        return pop[idxs].copy()
    
    
    def _random(self, pop, costs):
        idxs = np.random.choice(len(pop), size=self.offspring_size, replace=False)
        return pop[idxs].copy()
    
    
    def _mulambda(self, pop, pop_costs, children, children_costs):
        full_pop = np.vstack((pop, children))
        full_costs = np.append(pop_costs, children_costs)
        idxs = np.argsort(full_costs)[:self.population_size]
        return full_pop[idxs], full_costs[idxs]
    
    
    def _lambda(self, pop, pop_costs, children, children_costs):
        return children, children_costs