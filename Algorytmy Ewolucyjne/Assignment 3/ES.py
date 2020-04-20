from tqdm import trange
import numpy as np

class ES:
    def __init__(self, domain, dims, population_size, offspring_size, parent_choice_method, replacement_method, tau, tau0, cost_func, max_iters):
        self.domain = domain
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
            self.parent_selection = self._roulette
        
        assert replacement_method in ['mulambda', 'lambda'], 'replacement method has to be either "mulambda" or "lambda'
        if replacement_method == 'mulambda':
            self.replace = self._mulambda
        elif replacement_method == 'lambda':
            self.replace = self._lambda
        
    
    def run(self, verbose=False, with_tqdm=True):
        if with_tqdm:
            range_ = trange(self.max_iters, position=0, leave=True)
        else:
            range_ = range(self.max_iters)
        
        self._generate_population()
        costs = self.cost_func(self.population)
        best = self.population[costs.argmin()]
        best_cost = costs.min()
        
        try:
            for iter_ in range_:
                parents = self.parent_selection(self.population, costs)
                children = self.mutate(parents)
                children_costs = self.cost_func(children)
                self.population, costs = self.replace(self.population, costs, children, children_costs)

                if costs.min() < best_cost:
                    best_cost = costs.min()
                    best = self.population[costs.argmin()]

                if verbose and iter_%50 == 0:
    #                 print(f'iter: {iter_}, min: {round(costs.min(), 2)}\tmax: {costs.max()}\tmean: {costs.mean()}')
                    print('iter: %d, min: %.4f,\tmean: %.4f,\tmax: %.4f' % (iter_, costs.min(), costs.mean(), costs.max()))
        except KeyboardInterrupt:
            pass
        
        return best, best_cost
    
    
    def _generate_population(self):
        pop = []
        for _ in range(self.population_size):
            x = np.random.uniform(self.domain[0], self.domain[1], size=self.dims)
            sigmas = np.random.uniform(0.5, 1.5, size=self.dims)
            pop.append(np.vstack((x, sigmas)))
        self.population = np.array(pop)
    
    
    def mutate(self, pop):
        x, sigmas = pop[:, 0], pop[:, 1]
        mutated = []
        
        for i in range(len(pop)):
            eps0 = np.random.random() * self.tau0
            eps = np.random.random(self.dims) * self.tau
            
            new_sigma = sigmas[i] * np.exp(eps0 + eps)
            new_x = x[i] + np.random.random(self.dims) * new_sigma
            
            its = 0
            while np.any((new_x < self.domain[0], new_x > self.domain[1])) and its < 5:
                its += 1
                new_x = x[i] + np.random.random(self.dims) * new_sigma
            
            if np.any((new_x < self.domain[0], new_x > self.domain[1])):
                new_x = np.random.uniform(self.domain[0], self.domain[1], size=self.dims)
                new_sigma = np.ones(self.dims)
            
            mutated.append(np.vstack((new_x, new_sigma)))
            
        return np.array(mutated)
        
    
    def _roulette_method(self, pop, costs):
        idxs = np.random.choice(len(pop), p=costs/sum(costs), size=self.offspring_size, replace=True)
        return pop[idxs, :, :]
    
    def _random(self, pop, costs):
        idxs = np.random.choice(len(pop), size=self.offspring_size, replace=False)
        return pop[idxs, :, :]
    
    
    def _mulambda(self, pop, pop_costs, children, children_costs):
        full_pop = np.vstack((pop, children))
        full_costs = np.append(pop_costs, children_costs)
        idxs = np.argsort(full_costs)[:self.population_size]
        return full_pop[idxs], full_costs[idxs]
    
    
    def _lambda(self, pop, pop_costs, children, children_costs):
        return children, children_costs