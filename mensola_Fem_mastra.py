import numpy as np
import copy

"""
Analisi fem di una trave incastrata con forze applicate
nel nodo centrale e nel nodo opposto all'incastro
"""

# cd /Users/mastraa/Desktop/Programmazione/Sorgenti/python_fem

E=206e3
l=1e3
I=5e6

M=12*E*I/l**3
T=6*E*I/l**2
S=2*E*I/l

K_el=np.array([[M,T,-M,T],[T,2*S,-T,S],[-M,-T,M,-T],[T,S,-T,2*S]])

K=np.zeros((6,6),dtype=float)

K[0:4,0:4]=K_el
K[2:6,2:6]=K[2:6,2:6]+K_el

F=np.array([np.nan,np.nan,-1e3,0,-1e3,0])

f=np.zeros(6)

f[2:]=np.dot(np.linalg.inv(K[2:,2:]),F[2:])
F=np.dot(K,f)


#print E, I, l
print f
print F

x = y = np.arange(0.0,5.0,1.0)
z=y=np.array([[1.0,2.0,8.7],[2.3,4.5,4.4]])
#np.savetxt('test.out', x, delimiter=',')   # X is an array
#np.savetxt('test.out', (x,y,z))   # x,y,z equal sized 1D arrays
np.savetxt('test.txt', (z,y), fmt='%1.4e')   # use exponential notation