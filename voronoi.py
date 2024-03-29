import numpy as np 
import cv2 
from matplotlib import pyplot as plt
import scipy
import matplotlib.animation as animation
import utils
from graph_class import Graph
import config
import skimage
import voronoi_verification


def obs_centers(map) -> np.ndarray:
    res = []
    r, classes = scipy.ndimage.label(map)
    i_space = np.indices(map.shape)
    for i in range(1, classes+1):
        mask = r==i
        points = i_space[:, mask]
        obs_center = (np.sum(points, axis=1) / points.shape[1]).astype(int)
        if mask[obs_center[0], obs_center[1]] and points.shape[1] >= config.voronoi_obs_thresh:
            res.append(obs_center)
    return np.array(res)


def voronoi(m):
    map = np.copy(m)
    obs = obs_centers(map)
    obs = np.concatenate((obs, np.array([[m.shape[1]*2, m.shape[0]*2], [m.shape[1]*2, -m.shape[0]*2], [-m.shape[1]*2, 0]])))
    v = scipy.spatial.Voronoi(obs[:, ::-1])
    return v


def voronoi_to_graph(v):
    res = dict()
    for edge in v.ridge_vertices:
        v1 = tuple(v.vertices[edge[0]].astype(int))
        v2 = tuple(v.vertices[edge[1]].astype(int))
        if -1 in edge:
            continue
        weight = np.linalg.norm(v.vertices[edge[0]] - v.vertices[edge[1]])
        res[v1] = res.get(v1, list()) + [(v2, weight)]
        res[v2] = res.get(v2, list()) + [(v1, weight)] 
    return Graph(res)


def verify(g: Graph, map: np.ndarray, thresh: int) -> Graph:
    verified = False

    while not verified:
        for e in g.get_edges():
            v1, v2 = e
            line = skimage.draw.line(v1[0], v1[1], v2[0], v2[1])
            map_line = map[line]
            if map_line[map_line!=0].shape[0] < thresh:
                continue
            

def create_voronoi_graph(map) -> Graph:
    v = voronoi(map)
    g = voronoi_to_graph(v)
    voronoi_verification.verificate(g, map)
    return g
