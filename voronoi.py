import numpy as np 
import cv2 
from matplotlib import pyplot as plt
from PIL import Image
import scipy
import matplotlib.animation as animation
import utils


def obs_centers(map):
    res = []
    r, classes = scipy.ndimage.label(map)
    i_space = np.indices(map.shape)
    for i in range(1, classes+1):
        mask = r==i
        points = i_space[:, mask]
        obs_center = (np.sum(points, axis=1) / points.shape[1]).astype(int)
        res.append(obs_center)
    
    return np.array(res)


def voronoi(m):
    map = np.copy(m)
    map = utils.minkowski(map, 20)
    obs = obs_centers(map)
    v = scipy.spatial.Voronoi(obs[:, ::-1])
