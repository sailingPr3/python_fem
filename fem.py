import numpy as np
import copy
from numpy import cos, sin

def truss_rigidity(E, A, l, theta = 0):
	"""Produce matrice di rigidezza per un'asta (truss).
		E = modulo di Young
		A = area della sezione
		l = lunghezza dell'asta
		theta = rotazione
		"""
	cost = E * A / l
	mat = cost * np.matrix(
					[[1,-1],[-1,1]],
					dtype=float)
	# matrice di rotazione
	T = np.matrix([
		[cos(theta),sin(theta),0,0],
		[0,0,cos(theta),sin(theta)]], dtype=float)
	if theta:
		mat = (T.transpose() * mat * T)
	return mat

def switch(nm_mat, ls_perm):
	tmp = copy.deepcopy(nm_mat)
	for i in range(len(ls_perm)):
		if i != ls_perm[i]:
			tmp[i,:] = nm_mat[ls_perm[i],:]
	switched = copy.deepcopy(tmp)
	for i in range(len(ls_perm)):
		if i != ls_perm[i]:
			switched[:,i] = tmp[:,ls_perm[i]]
	return switched

def beam_rigidity(E,J,l,theta = 0):
	M = 12. * E * J / (l * 3)
	T = 6. * E * J / (l * 2)
	S = 2. * E * J / (l)
	mat = np.matrix(
		[
		[M, T, -M, T],
		[T, 2*S, -T, S],
		[-M, -T, M, -T],
		[T,S,-T, 2*S]])
	lx = cos(theta)
	mx = sin(theta)
	ly = cos(np.pi/2 + theta)
	my = sin(np.pi/2 + theta)
	T = np.matrix([
		[lx,mx,0,0],
		[ly,my,0,0],
		[0,0,lx,mx],
		[0,0,ly,my]])
	if theta:
		mat = T.transpose() * mat * T
	return mat

def K_albero(ls_mat):
	if len(ls_mat) != 7:
		print("Expected 7 matrices")
		return 0

	K = np.zeros((15,15),dtype=float)
	# First matrix
	K[0:4,0:4] = ls_mat[0]
	
	# Second
	K[2:6,2:6] += ls_mat[1]
	
	# Third
	K[4:8,4:8] += ls_mat[2]
	
	# Fourth
	K[6:9,6:9] += ls_mat[3][0:3,0:3]
	K[[6,7,8,10],10] += ls_mat[3][:,3]
	K[10,[6,7,8,10]] += ls_mat[3][3,:]
	
	# Fifth
	K[4:6,4:6] += ls_mat[4][0:2,0:2]
	K[12:14,12:14] += ls_mat[4][2:4,2:4]
	K[4:6,12:14] += ls_mat[4][0:2,2:4]
	K[12:14,4:6] += ls_mat[4][2:4,0:2]
	
	# Sixth
	K[8:13,8:13] += switch(ls_mat[5],[1,0])

	# Seventh
	K[[12,14],12] += ls_mat[6][:,0]
	K[[12,14],14] += ls_mat[6][:,1]

	return K