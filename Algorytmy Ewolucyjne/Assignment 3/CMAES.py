import numpy as np


class SMAES:
    def __init__(self, population_size, chromosome_length, eval_func, crossover_func,
                 replacement_method, no_children, no_parents, beta, tau0, tau, max_iters):
    # beta - parameter of mutation, we add to lambdas eps ~N(0, beta)
    # tau - parameter of mutation,  we mult sigmas by exp(~N(0, tau) + ~N(0, tau0))
    # ind -> (x, age, lambdas, sigmas) sizes:(ch_len, 1, ch_len*(ch_len)-1, ch_len)
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.eval_func = eval_func
        self.crossover_func = crossover_func
        self.no_children = no_children
        self.no_parents = no_parents
        self.beta = beta
        self.tau0 = tau0
        self.tau = tau
        self.max_iters = max_iters
        
        
        if replacement_method == 'mulambda':
            self.replacement_func = self._mulambda
        elif replacement_method == 'lambda':
            self.replacement_func = self._lambda
        elif replacement_method == 'tournament':
            self.replacement_func = self._tournament
        else:
            raise NameError('Replacement method has to be: "mulambda", "lambda" or "tournament"')
    
    
    def run(self):
        self.population = self.create_random_population()
        pop_evals = self.eval_func(self.population)
        
        for iter_ in range(max_iters):
            children = self.reproduction()
            children_evals = self.eval_func(children)
            self.population = self.replacement_func(self.population, pop_evals, children, children_evals)
            pop_eval = self.eval_func(self.population)
    
    
    def reproduction(self):
        children = []
        
        for i in range(self.no_children):
            parents = self._parent_selection(self.population, self.eval_pop)
            child = self.crossover_func(parents)
            child = self.mutation_func(child)
            
            children.append(child)
        return children

    
    def mutate(self, ind):
        mut_ind = ind
        mut_ind[2] += np.random.random(self.chromosome_length)*self.beta  #alphas
        mut_ind[3] *= np.exp(np.random.random(self.chromosome_length)*self.tau0 + np.random.random(self.chromosome_length)*self.tau)
        
        z = np.random.random(self.chromosome_length)*mut_ind[2]
        z = z.reshape(-1, 1)
        
        T = np.ones((self.chromosome_length, self.chromosome_length))
        
        for p in range(self.chromosome_length):
            for q in range(p+1, self.chromosome_length):
                j = 0.5 * (2*self.chromosome_length - p) * (p+1) - 2 * self.chromosome_length + q
                tpq = self._create_tpq(p, q, mut_ind[1][j])
                T = T.dot(tpq)
                
        mut_ind[0] += (T.dot(z)).T
        mut_ind[1] += 1  #age+1
        
        return mut_ind
    
    
    def create_random_population(self):
        population = [None for _ in range(self.population_size)]
        for i in range(len(population)):
            p = [None for _ in range(4)]
            p[0] = np.zeros(self.chromosome_length)
            p[1] = 0
            p[2] = np.ones(self.chromosome_length * (self.chromosome_length-1)/2)
            p[3] = np.ones(self.chromosome_length)
            
            population[i] = p
        return population
         
    
    def _parent_selection(self, parent_pop, parent_evals):
        return np.random.choice(parent_pop, p=parent_evals/parent_evals.sum(), size=self.no_parents)
    
    
    def _random_selection(self, parents):
        return np.random.choice(parents)
    
    
    def _global_intermediary_recombination(self, parents):
        return np.dstack(parents).mean(axis=2)
    
    
    def _local_intermediary_recombination(self, parents):
        u = np.random.random()
        p1, p2 = np.random.choice(parents, size=2)
        
        child = p2[:]
        for i in range(self.chromosome_length):
            if np.random.random() < u:
                child[i] = p1[i][:]
        return child
    
    
    def _uniform_crossover(self, parents):
        child = parents[0][:]
        for attr in range(len(child)):
            for i in range(len(child[attr])):  #x
                par_idx = np.random.randint(len(parents))
                child[attr][i] = parents[par_idx][attr][i]
        return child
    
    
    def _create_tpq(self, p, q, alpha):
        t = np.diag(np.ones(self.chromosome_length))
        t[p][p] = np.cos(alpha)
        t[p][q] = -np.sin(alpha)
        t[q][p] = np.sin(alpha)
        t[q][q] = -np.cos(alpha)
        return t
    
    
    def _mulambda(self, parents, parent_evals, children, children_evals):
        pop = np.vstack((parents, children))
        evals = np.append(parent_evals, children_evals)
        idxs = np.argsort(evals)[:-self.population_size-1:-1]
        return pop[idxs], evals[idxs]
    
    
    def _lambda(self, parents, parent_evals, children, children_evals):
        return children, children_evals
    
    
    def _tournament(self, parents, parent_evals, children, children_evals):
        pop = np.vstack((parents, children))
        evals = np.append(parent_evals, children_evals)
        new_pop = np.random.choice(pop, size=self.population_size, p=evals/evals.sum())
        return new_pop