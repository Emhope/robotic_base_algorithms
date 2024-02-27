import numpy as np 
import cv2 
from matplotlib import pyplot as plt
from PIL import Image
import scipy
import matplotlib.animation as animation
import utils
from graph_class import Graph


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
    #map = utils.minkowski(map, 20)
    obs = obs_centers(map)
    obs = np.concatenate((obs, np.array([[m.shape[1]*2, m.shape[0]*2], [m.shape[1]*2, -m.shape[0]*2], [-m.shape[1]*2, 0]])))
    v = scipy.spatial.Voronoi(obs[:, ::-1])
    return v
 

def add_endpoint(g: Graph, new_p):
    '''
    adding goal or end point (p) to graph
    '''
    lines = g.get_edges()
    min_dist, point, line = np.inf, None, None
    for l in lines:
        d, p = utils.perp_intersection(l[0], l[1], new_p)
        if 0 < d < min_dist:
            min_dist = d
            point = p
            line = l
    
    if point is not None:
        g.remove_edge(*line)
        g.add_edge(line[0], point)
        g.add_edge(line[1], point)
        g.add_edge(new_p, point)


def voronoi_to_graph(v, map_shape):
    res = dict()
    for edge in v.ridge_vertices:
        v1 = tuple(v.vertices[edge[0]].astype(int))
        v2 = tuple(v.vertices[edge[1]].astype(int))
        if -1 in edge:
            continue
        #if (0 <= v1[0] <= map_shape[1] and 0 <= v1[1] <= map_shape[0]) or (0 <= v2[0] <= map_shape[1] and 0 <= v2[1] <= map_shape[0]):
        weight = np.linalg.norm(v.vertices[edge[0]] - v.vertices[edge[1]])
        res[v1] = res.get(v1, list()) + [(v2, weight)]
        res[v2] = res.get(v2, list()) + [(v1, weight)] 
    return Graph(res)


