import numpy as np
from graph_class import Graph


def create_ceil_graph_2d(map, step):
    ceils = map[step:-step:step, step:-step:step]
    g = Graph()

    for y in range(ceils.shape[0]):
        for x in range(ceils.shape[1]):
            v = np.array([y, x]) * np.array([step, step]) + np.array([step, step])
            if map[v[0], v[1]]: # if map[v[0], v[1], v[2]]
                continue
            for _y in range(-1, 2):
                for _x in range(-1, 2):
                    n = v + np.array([_y, _x]) * np.array([step, step])                    
                    if _y == _x == 0 or map[n[0], n[1]]: # map[n[0], n[1], n[2]]
                        continue
                    g.add_edge(tuple(v[::-1]), tuple(n[::-1]))
    return g


def create_ceil_graph_2d2(img, step):
    graph = {}
    start = step // 2
    img = np.copy(img)
    img = img.astype(int)
    img[img != 0] = -1
    for y in range(start, img.shape[0], step):
        for x in range(start, img.shape[1], step):
            if img[y, x] == 0:
                neighbors = {}
                for _y in [-step, 0, step]:
                    for _x in [-step, 0, step]:
                        if _y == 0 and _x == 0:
                            continue
                        if 0 <= y + _y < img.shape[0] and 0 <= x + _x < img.shape[1] \
                            and img[y + _y, x + _x] == 0:
                            neighbors[(x + _x, y + _y)] = step * np.sqrt(_x**2 + _y**2)
                graph[(x, y)] = neighbors
    return graph


def create_ceil_graph_3d(map, step):
    ceils = map[:, step:-step:step, step:-step:step]
    g = Graph()
    for w in range(ceils.shape[0]):
        for y in range(ceils.shape[1]):
            for x in range(ceils.shape[2]):
                v = np.array([w, y, x]) * np.array([1, step, step]) + np.array([0, step, step])
                if map[v[0], v[1], v[2]]:
                    continue
                for _w in range(-1, 2):
                    for _y in range(-1, 2):
                        for _x in range(-1, 2):
                            n = v + np.array([_w, _y, _x]) * np.array([1, step, step])
                            if not (0 <= n[0] <= map.shape[0]-1):
                                continue
                            if _w == _y == _x == 0 or map[n[0], n[1], n[2]]:
                                continue
                            g.add_edge(tuple(v), tuple(n))
    return g
    