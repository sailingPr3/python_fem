from fem import beam_rigidity, truss_rigidity, K_albero
import numpy as np
import copy

#%%

foo = beam_rigidity(210000,1.0762e6,2000)
bar = copy.deepcopy(foo)

#%%

res = np.matrix(np.zeros((6,6)),dtype=float)
res[0:4,0:4] = foo
res[2:6,2:6] += bar

#%%

r = res[2:6,2:6]

#%%

Fr = np.array([127,0.3,127,0],dtype=float)

#%%

fr = (r**(-1)).dot(Fr)

#%%
f = np.zeros((6),dtype=float)
f[2:] = fr
