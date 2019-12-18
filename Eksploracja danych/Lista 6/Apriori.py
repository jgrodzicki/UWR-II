#setup
import numpy as np
from collections import defaultdict, deque
import itertools

from tqdm import tqdm, trange
import pandas as pd


class Apriori:
    def __init__(self, df, delimiter=' ', supp_count=100, min_confidence=0.7, min_lift=1, min_leverage=0):
        self.df = df.copy()
        self.delimiter = delimiter
        self.supp_count = supp_count
        self.min_confidence = min_confidence
        self.min_lift = min_lift
        self.min_leverage = min_leverage
        
        self.find_single_group_counts()
        
        self.df[self.df.columns[0]] = self.df[self.df.columns[0]].str.strip().apply(lambda row: set(row.split(self.delimiter)))
        
        
    def find_single_group_counts(self):
        res = defaultdict(int)
        for i in trange(len(self.df), desc='Find single group counts', position=0, leave=True):
            row = self.df.iloc[i][0].strip().split(self.delimiter)
            for v in row:
                res[v] += 1 
        self.single_group_counts = pd.Series(res)
        

    def get_common_single_groups(self):
        return self.single_group_counts.where(lambda x: x >= self.supp_count).dropna()

    
    def find_common_groups(self):
        def gen_Ck(k):
            Lk = self.common_groups[k-1]

            Ck = []  # candicates

            for i in range(len(Lk)):
                group_i = Lk[i]
                for j in range(i+1, len(Lk)):
                    group_j = Lk[j]

                    group_ij = group_i.union(group_j)
                    if len(group_ij) == k and group_ij not in Ck:
                        Ck.append(group_ij)

            return np.array(Ck)
        
        single_groups = self.get_common_single_groups()
        self.common_groups = [None, list(map(lambda x: {x}, single_groups.index))]
        self.group_length = {tuple({k}): v for k, v in np.c_[single_groups.index, single_groups.values]}
        
        for length in tqdm(range(2, len(self.common_groups[1])), desc='Extending common groups', position=0, leave=True):
            Ck = gen_Ck(length)
            
            idx_count = pd.Series(Ck).apply(lambda c:
                                    np.count_nonzero([c.issubset(row)
                                                      for row in self.df[self.df.columns[0]]])) \
                                    .where(lambda x: x >= self.supp_count).dropna()
            

            if idx_count.size == 0:
                break
            
            D = Ck[idx_count.index]
            self.common_groups.append(D)
            
            for i, v in enumerate(idx_count.values):
                self.group_length[tuple(sorted(D[i]))] = v
                
    
    def find_rules(self):
        if self.min_confidence > 1:
            self.rules = []
            return
    
        S_all = []
        
        q = deque()
        subsets = []
        for group in self.common_groups[1:]:
            for X in group:
                conf = 1
                lift = self.lift(X, set())
                leve = self.leverage(X, set())

                if lift >= self.min_lift and leve >= self.min_leverage:
                    S_all.append(((X, set()), {'confidence': conf, 'lift': lift, 'leverage': leve}))
                    
                q.append((X, set()))
                subsets.append((X, set()))

        pbar = tqdm(desc='Find rules', position=0, leave=True)
        while q:
            pbar.update(1)
            A, B = q.popleft()
            for x in A:
                new_A = A - {x}
                new_Bs = [B.union({x}), {x}, set()]
                
                for new_B in new_Bs:
                    if (new_A, new_B) not in subsets:
                        conf = self.confidence(new_A, new_B)
                        lift = self.lift(new_A, new_B)
                        leve = self.leverage(new_A, new_B)

                        if conf >= self.min_confidence:
                            q.append((new_A, new_B))
                            
                            if lift >= self.min_lift and leve >= self.min_leverage:
                                S_all.append(((new_A, new_B), {'confidence': conf, 'lift': lift, 'leverage': leve}))
                        
                        subsets.append((new_A, new_B))

        pbar.close()

#         S_all = list(filter(lambda x: self.lift(x[0], x[1]) >= self.min_lift, tqdm(S_all, desc='min lift', position=0, leave=True)))
#         S_all = list(filter(lambda x: self.leverage(x[0], x[1]) >= self.min_leverage, tqdm(S_all, desc='min leverage', position=0, leave=True)))
        self.rules = S_all
        
        
    def support(self, X):
        if len(X) == 0:
            return 1
        return self.group_length[tuple(sorted(X))] / len(self.df)
    
    def confidence(self, A, B):
        if not A:  # A = {}
            return self.support(B)
        if not B:  # B = {}
            return 1
        return self.support(A.union(B)) / self.support(A)
    
    def lift(self, A, C):
        return self.confidence(A, C) / self.support(C)

    def leverage(self, A, C):
        return self.support(A.union(C)) - self.support(A)*self.support(C)