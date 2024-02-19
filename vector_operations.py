import numpy as np
from numpy import linalg as la

# counter-clockwise rotation matrices about the axes
def R_x(vector, angle):
    x_comp = vector[0] 
    y_comp = vector[1] * np.cos(angle) - vector[2] * np.sin(angle)
    z_comp = vector[1] * np.sin(angle) + vector[2] * np.cos(angle)

    return np.array([x_comp, y_comp, z_comp])

def R_y(vector, angle):
    x_comp = vector[0] * np.cos(angle) + vector[2] * np.sin(angle)
    y_comp = vector[1]
    z_comp = -vector[0] * np.sin(angle) + vector[2] * np.cos(angle)

    return np.array([x_comp, y_comp, z_comp])

def R_z(vector, angle):
    x_comp = vector[0] * np.cos(angle) - vector[1] * np.sin(angle)
    y_comp = vector[0] * np.sin(angle) + vector[1] * np.cos(angle)
    z_comp = vector[2]

    return np.array([x_comp, y_comp, z_comp])

def R_v(axis, vector, angle):
	axis = axis / np.linalg.norm(axis)
	# Rodrigues' rotation formula
	cos_theta = np.cos(angle)
	sin_theta = np.sin(angle)
	cross_product = np.cross(axis, vector)
	dot_product = np.dot(axis, vector)

	rotated_vector = (vector * cos_theta) + (cross_product * sin_theta) + (axis * dot_product * (1 - cos_theta))

	return rotated_vector

def pairwise_batch_cosine_sim_cal(x, y):
	dotprod_mat = np.dot(x,  y.T)
	costheta = dotprod_mat / (la.norm(x, axis=1)[:, np.newaxis] * la.norm(y, axis=1))
	print(costheta)
	return costheta