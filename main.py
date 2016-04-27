from fem import beam_rigidity, truss_rigidity, K_albero
import numpy as np

E = np.array([80,80,80,80,80,210,210],dtype = float) * 1000 # 1 - 7
J1 = np.array([0,0,0,0,1042],dtype=float) # 5
J2 = np.array([3.15,3.15,3.15,3.15,0],dtype=float)*100000 # 1 - 4
J = J1 + J2
A = np.array([1534,1534,1534,1534,500,7.1,7.1]) # 6,7
l = np.array([1000,2000,3000,1000,750,0,3000],dtype=float) # 1-5,7
l[5] = np.sqrt(np.square(l[2]) + np.square(l[4]+l[3]))

F=np.zeros(19)
f=np.zeros(19)

F[4]=-100
F[10]=1000

# Our rotation angles
theta = -np.arccos(l[2]/l[5]) - np.radians(180)
alpha = np.radians(270)

ls_mat = []
for i in range(5):
    ls_mat.append(
        beam_rigidity(E[i],J[i],A[i],l[i]) if i!=4 else beam_rigidity(E[i],J[i],l[i],alpha)
        )
ls_mat.append(truss_rigidity(E[5],A[5],l[5],theta))
ls_mat.append(truss_rigidity(E[6],A[6],l[6]))

K = K_albero(ls_mat)
K_r=np.linalg.inv(K[2:19,2:19])

f[2:19]=K_r.dot(F[2:19])
F=K.dot(f).transpose()

np.savetxt("F.txt",F,fmt="%.4e")
np.savetxt("Kr_albero.txt",K_r,fmt="%.4e")
np.savetxt("f_albero.txt",f,fmt="%.4e")
np.savetxt("K_albero.txt",K,fmt="%.4e")

print f
print F
