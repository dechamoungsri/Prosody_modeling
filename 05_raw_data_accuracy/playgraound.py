from sklearn.metrics import f1_score

import itertools
def findsubsets(S,m):
    return set(itertools.combinations(S, m))

# real = [0,0,0,1]
# pred = [1,1,1,0]

# f1 = f1_score(real, pred, average=None) 

# print f1

s = [0,1,1,1,2,3,3,4,4]

ss = findsubsets(set(s), 3)

for a in ss:
    print a, set(s)-set(a)

