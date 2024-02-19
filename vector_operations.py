import numpy as np

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