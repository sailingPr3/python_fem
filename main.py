from fem import beam_rigidity, truss_rigidity, K_albero
import numpy as np

E = np.array([80,80,80,80,80,210,210],dtype = float) * 1000 # 1 - 7
J1 = np.array([0,0,0,0,729.2],dtype=float) # 5
J2 = np.array([69,69,69,69,0],dtype=float)*10000 # 1 - 4
J = J1 + J2
A = np.array([50.3,50.3]) # 6,7
l = np.array([1000,2000,3000,1000,750,0,3000],dtype=float) # 1-5,7
l[5] = np.sqrt(np.square(l[2]) + np.square(l[4]))

# Our rotation angles
theta = -np.arccos(l[2]/l[5]) - np.radians(180)
alpha = np.radians(270)

ls_mat = []
for i in range(5):
    ls_mat.append(
        beam_rigidity(E[i],J[i],l[i]) if i!=4 else beam_rigidity(E[i],J[i],l[i],alpha)
        )
ls_mat.append(truss_rigidity(E[5],A[0],l[5],theta))
ls_mat.append(truss_rigidity(E[6],A[1],l[6]))
K = K_albero(ls_mat)
np.savetxt("K_albero.txt",K,fmt="%.4e")

print K
