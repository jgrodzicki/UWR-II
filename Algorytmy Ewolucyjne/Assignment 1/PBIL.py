import numpy as np
import pandas as pd

from tqdm import trange, tqdm
import matplotlib.pyplot as plt

from itertools import product


def _default_eval_func(population):
    return np.array([sum(individual) for individual in population])


class PBIL:
    
    def __init__(self, population_size, learning_rate, 
                 mutation_prob, disturbance_rate, allele_no, max_iter=1000, 
                 eval_func=_default_eval_func, with_tqdm=True, init_prob_val=0.5):
        self.population_size = population_size
        self.learning_rate = learning_rate
        self.mutation_prob = mutation_prob
        self.disturbance_rate = disturbance_rate
        self.prob_vect = np.full(allele_no, init_prob_val)
        self.allele_no = allele_no
        self.max_iter = max_iter
        self.eval_func = eval_func
        self.with_tqdm = with_tqdm
      
    def fit(self, new_max_iter=None):
        if new_max_iter is None:  # first fitting
            self.best_evals = np.zeros(self.max_iter)
            self.mean_evals = np.zeros(self.max_iter)
            self.worst_evals = np.zeros(self.max_iter)
        
            if self.with_tqdm:
                range_ = trange(self.max_iter, desc='epoch', position=0, leave=True)
            else:
                range_ = range(self.max_iter)
                
        else:  # continue fitting
            new_best_evals = np.zeros(new_max_iter)
            new_mean_evals = np.zeros(new_max_iter)
            new_worst_evals = np.zeros(new_max_iter)

            new_best_evals[:self.max_iter] = self.best_evals
            new_mean_evals[:self.max_iter] = self.mean_evals
            new_worst_evals[:self.max_iter] = self.worst_evals

            self.best_evals, self.mean_evals, self.worst_evals = new_best_evals, new_mean_evals, new_worst_evals
            
            if self.with_tqdm:
                range_ = trange(self.max_iter, new_max_iter, desc='epoch', position=0, leave=True)
            else:
                range_ = range(self.max_iter, new_max_iter)
            
            self.max_iter = new_max_iter
            
        population = self._random_population()
        evals = self.eval_func(population)
        self.best_individual = None
        self.best_individual_eval = -1
        
        for epoch in range_:
            best = population[evals.argmax()]
            
            if evals.max() > self.best_individual_eval:
                self.best_individual_eval = evals.max()
                self.best_individual = best

            self.best_evals[epoch] = evals.max()
            self.mean_evals[epoch] = evals.mean()
            self.worst_evals[epoch] = evals.min()
            
            # learn
            self.prob_vect = self.prob_vect * (1 - self.learning_rate) + \
                            best * self.learning_rate
            #mutate
            for idx in (np.random.rand(self.allele_no) < self.mutation_prob).nonzero():
                self.prob_vect[idx] = self.prob_vect[idx] * (1 - self.disturbance_rate) + self._binary_random(0.5) * self.disturbance_rate
            
            population = self._random_population()
            evals = self.eval_func(population)
    
    
    def plot_evals(self, with_params=False):
        plt.figure()
        if with_params:
            plt.title(f'Eval changes for learning_rate: {self.learning_rate}, \
mutation_prob: {self.mutation_prob}, disturbance_rate: {self.disturbance_rate}')
        else:
            plt.title('Eval changes')
        
        plt.plot(range(self.max_iter), self.best_evals, c='g', linewidth=0.5)
        plt.plot(range(self.max_iter), self.mean_evals, c='b', linewidth=0.5)
        plt.plot(range(self.max_iter), self.worst_evals, c='r', linewidth=0.5)
        plt.show()
    
    def _binary_random(self, p):
        if np.random.rand() < p:
            return 1
        else:
            return 0
    
    def _random_individual(self, p):
        return np.array([self._binary_random(pk) for pk in p])
    
    def _random_population(self):
        return np.array([self._random_individual(self.prob_vect) 
                         for _ in range(self.population_size)])