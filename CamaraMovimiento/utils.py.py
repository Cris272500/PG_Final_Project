import numpy as np

def create_projection_matrix(fov, aspect_ratio, near, far):
    return np.array([
        [1/(aspect_ratio*np.tan(fov/2)), 0, 0, 0],
        [0, 1/np.tan(fov/2), 0, 0],
        [0, 0, -(far+near)/(far-near), -2*far*near/(far-near)],
        [0, 0, -1, 0]
    ], dtype='f4')
