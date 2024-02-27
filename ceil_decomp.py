import numpy as np


def create_ceil_graph(img, step):
    arr = img[(step // 2)::step, (step // 2)::step]
    graph = {}
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            if arr[y, x] == 0:
                neighbors = []
                for _x, _y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        if (_x != 0 or _y != 0) and 0 <= x + _x < arr.shape[1] and 0 <= y + _y < arr.shape[0]:
                            if arr[y + _y, x + _x] == 0:
                                neighbors.append((x + _x, y + _y))
                graph[(x, y)] = neighbors
    return graph


def create_ceil_graph_3d(img, step):
    arr = img[(step // 2)::step, (step // 2)::step]
    graph = {}
    for y in range(arr.shape[0]):
        for x in range(arr.shape[1]):
            for w in range(arr.shape[2]):
                if arr[y, x, w] == 0:
                    neighbors = []
                    for _y in [-1, 0, 1]:
                        for _x in [-1, 0, 1]:
                            for _w in [-1, 0, 1]:
                                if _y == 0 and _x == 0 and _w == 0:
                                    continue
                                if 0 <= y + _y < arr.shape[0] and 0 <= x + _x < arr.shape[1] \
                                    and 0 <= w + _w < arr.shape[2] and arr[y + _y, x + _x, w + _w] == 0:
                                        neighbors.append(((x + _x, y + _y, w + _w), np.sqrt(_x**2 + _y**2 + _w**2))) # ребра = эвклидово расстояние
                    graph[(x, y, w)] = neighbors
    return graph