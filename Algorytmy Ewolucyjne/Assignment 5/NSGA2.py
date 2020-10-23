import time
import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt
from collections import defaultdict


def PMX(ind1, ind2, separator_no=2):
    new_ind1, new_ind2 = ind1.copy(), ind2.copy()
    idxs = sorted(np.random.choice(len(ind1), separator_no, replace=False))
    
    group = np.random.choice(separator_no-1)
    start, end = idxs[group], idxs[group+1]
    
    tmp = ind1[start:end].copy()
    ind1[start:end] = ind2[start:end]
    ind2[start:end] = tmp
    
    for i in range(len(ind1)):
        if start <= i < end:
            continue
            
        while ind1[i] in ind1[start:end]:
            # get elem from the other ind
            idx_of_elem = np.nonzero(ind1[start:end] == ind1[i])[0][0]
            ind1[i] = ind2[start+idx_of_elem]
        
        while ind2[i] in ind2[start:end]:
            # get elem from the other ind
            idx_of_elem = np.nonzero(ind2[start:end] == ind2[i])[0][0]
            ind2[i] = ind1[start+idx_of_elem]

    return ind1, ind2

def tsp_F(p, dist):
    s = 0.0
    for i in range(len(p)):
        s += dist[p[i-1], p[i]]
    return s

def reverse_sequence_mutation(p, *args):
    a = np.random.choice(len(p), 2, False)
    i, j = a.min(), a.max()
    q = p.copy()
    q[i:j+1] = q[i:j+1][::-1]
    return q


class NSGA2:
    
    def __init__(self, N, d, domain, crossover_func=PMX, F=tsp_F, mutation_func=reverse_sequence_mutation, replace_method='mu+lambda', number_of_offspring=None, crossover_prob = 0.95, mutation_prob = 0.25, max_iters = 250, no_groups=2):
        
        self.N = N
        self.d = d
        self.domain = domain
        
        self.crossover_func = crossover_func
        self.F = F
        self.mutation_func = mutation_func
        
        if number_of_offspring is None:
            number_of_offspring = N
        self.number_of_offspring = number_of_offspring
        
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.max_iters = max_iters
        assert replace_method in ['mu+lambda', 'lambda'], 'wrong replace_method: ["mu+lambda", "lambda"]'
        self.replace_method = replace_method
        self.no_groups = no_groups
        
        
    def run(self, verbose=False, with_tqdm=True):
        time0 = time.time()
        self.mean_costs = np.zeros(self.max_iters)
        self.min_costs = np.zeros(self.max_iters)
        self.max_costs = np.zeros(self.max_iters)

        self.best_objective_value = np.Inf
        self.best_chromosome = np.zeros((1, self.d))

        current_population = self._generate_random_population()
        obj_vals = np.array(list(map(lambda ind: self.F(ind), current_population)))
        fronts = self.pareto_fronts(obj_vals)
        
        if with_tqdm:
            range_ = trange(self.max_iters, position=0, leave=True)
        else:
            range_ = range(self.max_iters)
    
        for its in range_:
            parent_idxs = self._select_parent_idxs(fronts)
            print(current_population)
            
            children_pop = self._gen_children_pop(current_population, parent_idxs)
            print('childern', children_pop)
            self._mutate(children_pop)

            children_obj_vals = self._eval_children(children_pop)
            children_fronts = self.pareto_fronts(children_obj_vals)
            
            current_population, obj_vals = self._replace_pop(current_population, fronts, children_pop, children_fronts)
            
            fronts = self.pareto_fronts(obj_vals)

            
            if verbose:
                print('%3d %14.8f %12.8f %12.8f %12.8f %12.8f' % (its, time.time() - time0, obj_vals.min(), obj_vals.mean(), obj_vals.max(), obj_vals.std()))
        return current_population
    
    
    def pareto_fronts(self, obj_vals):
        dominant_count = np.zeros(self.N).astype(int)
        dominates = defaultdict(set)
        fronts = np.full(self.N, None)
        
        for i, vals1 in enumerate(obj_vals):
            for j, vals2 in enumerate(obj_vals):
                if j < i:
                    continue

                if np.all(vals1 <= vals2) and np.any(vals1 < vals2):
                    dominant_count[j] += 1
                    dominates[i].add(j)
                elif np.all(vals1 >= vals2) and np.any(vals1 > vals2):
                    dominant_count[i] += 1
                    dominates[j].add(i)
        
        cur_pareto = 0
        fronts[np.nonzero(dominant_count == 0)[0]] = cur_pareto
        from_pareto = np.nonzero(fronts == 0)[0]
        
        while len(from_pareto):
            dominant_count[from_pareto] = -1
            cur_pareto += 1
            for i in from_pareto:
                if len(dominates[i]) == 0:
                    continue
                dominant_count[np.array(list(dominates[i]))] -= 1
                fronts[np.nonzero(dominant_count == 0)[0]] = cur_pareto
            from_pareto = np.nonzero(fronts == cur_pareto)[0]
        
        return fronts
    
    
#     def crowding_dists(self, )
    
    
    def plot_costs(self, title=''):
        plt.title(title)
        plt.plot(self.max_costs, label='max')
        plt.plot(self.min_costs, label='min')
        plt.plot(self.mean_costs, label='mean')
        plt.show()
        
    
    def _generate_random_population(self):
        return np.random.uniform(self.domain[0], self.domain[1], size=(self.N, self.d))
    
    
    def _gen_children_pop(self, current_population, parent_idxs):
        children_pop = np.zeros((self.number_of_offspring, self.d), dtype=np.int64)
        for i in range(int(self.number_of_offspring/2)):
            if np.random.random() < self.crossover_prob:
                children_pop[2*i, :], children_pop[2*i+1, :] = self.crossover_func(current_population[parent_idxs[2*i], :].copy(), current_population[parent_idxs[2*i+1], :].copy())
            else:
                children_pop[2*i, :], children_pop[2*i+1, :] = current_population[parent_idxs[2*i], :].copy(), current_population[parent_idxs[2*i+1]].copy()

        if np.mod(self.number_of_offspring, 2) == 1:
            children_pop[-1, :] = current_population[parent_idxs[-1], :]

        print('ch', children_pop)
        return children_pop
    
    
    def _select_parent_idxs(self, front):
        idxs = np.argsort(front)
        return idxs[:self.number_of_offspring]
    
    
    def _mutate(self, children_pop):
        for i in range(self.number_of_offspring):
            if np.random.random() < self.mutation_prob:
                children_pop[i, :] = self.mutation_func(children_pop[i, :], self.no_groups)
            
    
    def _eval_children(self, children_pop):
        return np.array(list(map(lambda ind: self.F(ind), children_pop)))
    
    
    def _replace_pop(self, current_population, obj_vals, children_pop, children_obj_vals):
        if self.replace_method == 'mu+lambda':
            obj_vals = np.hstack([obj_vals, children_obj_vals])
            current_population = np.vstack([current_population, children_pop])

            idxs = np.argsort(obj_vals)
            print(f'idxs: {idxs}')
            current_population = current_population[idxs[:self.N], :]
            obj_vals = obj_vals[idxs[:self.N]]
        elif self.replace_method == 'lambda':
            current_population = children_pop
            obj_vals = children_obj_vals
        
        return current_population, obj_vals