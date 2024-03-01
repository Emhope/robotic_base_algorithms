import numpy as np
from graph_class import Graph


def create_ceil_graph_2d(map, step):
    ceils = map[step:-step:step, step:-step:step]
    g = Graph()

    for y in range(ceils.shape[0]):
        for x in range(ceils.shape[1]):
            v = np.array([y, x]) * np.array([1, step, step]) + np.array([0, step, step])
            if map[*v]: # if map[v[0], v[1], v[2]]
                continue
            for _y in range(-1, 2):
                for _x in range(-1, 2):
                    n = v + np.array([_y, _x]) * np.array([1, step, step])
                    if not (0 <= n[0] <= map.shape[0]-1):
                        continue
                    if _y == _x == 0 or map[*n]: # map[n[0], n[1], n[2]]
                        continue
                    g.add_edge(tuple(v), tuple(n))
    return g



def create_ceil_graph_3d(map, step):
    ceils = map[:, step:-step:step, step:-step:step]
    g = Graph()
    for w in range(ceils.shape[0]):
        for y in range(ceils.shape[1]):
            for x in range(ceils.shape[2]):
                v = np.array([w, y, x]) * np.array([1, step, step]) + np.array([0, step, step])
                if map[*v]: # if map[v[0], v[1], v[2]]
                    continue
                for _w in range(-1, 2):
                    for _y in range(-1, 2):
                        for _x in range(-1, 2):
                            n = v + np.array([_w, _y, _x]) * np.array([1, step, step])
                            if not (0 <= n[0] <= map.shape[0]-1):
                                continue
                            if _w == _y == _x == 0 or map[*n]: # map[n[0], n[1], n[2]]
                                continue
                            g.add_edge(tuple(v), tuple(n))
    return g
    