import numpy as np
import copy
import fem

"""
Analisi fem di una trave incastrata con forze applicate
nel nodo centrale e nel nodo opposto all'incastro
"""

# cd /Users/mastraa/Desktop/Programmazione/Sorgenti/python_fem

E=210e3
l=1e3
I=69e5

M=12*E*I/l**3
T=6*E*I/l**2
S=2*E*I/l

print M, 2*S