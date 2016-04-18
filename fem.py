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
	M = 12. * E * J / (l ** 3)
	T = 6. * E * J / (l ** 2)
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

	K = np.matrix(np.zeros((16,16)),dtype=float)
	# First matrix
	K[0:4,0:4] = ls_mat[0]

	# Second
	K[2:6,2:6] += ls_mat[1]

	# Third
	K[4:6,4:6] += ls_mat[2][0:2,0:2]
	K[4:6,7:9] += ls_mat[2][0:2,2:4]
	K[7:9,4:6] += ls_mat[2][2:4,0:2]
	K[7:9,7:9] += ls_mat[2][2:4,2:4]

	# Fourth
	K[7:9,7:9] += ls_mat[3][0:2,0:2]
	K[7:9,10:12] += ls_mat[3][0:2,2:4]
	K[10:12,7:9] += ls_mat[3][2:4,0:2]
	K[10:12,10:12] += ls_mat[3][2:4,2:4]

	# Fifth
	mat_5 = switch(ls_mat[4],[1,0])
	K[5:7,5:7] += mat_5[0:2,0:2]
	K[5:7,[12,14]] += mat_5[0:2,2:4]
	K[[12,14],5:7] += mat_5[2:4,0:2]
	K[[12,12,14,14],[12,14,12,14]] += mat_5[2:4,2:4].reshape((1,4))

	# Sixth
	K[9:11,9:11] += ls_mat[5][0:2,0:2]
	K[9:11,12:14] += ls_mat[5][0:2,2:4]
	K[12:14,9:11] += ls_mat[5][2:4,0:2]
	K[12:14,12:14] += ls_mat[5][2:4,2:4]

	# Seventh
	K[[12,12,15,15],[12,15,12,15]] += ls_mat[6].reshape((1,4))

	return K
