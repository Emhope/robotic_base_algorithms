import numpy as np

def create_ceil_graph_2d(img, step):
    graph = {}
    start = step // 2
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


def create_ceil_graph_3d(img, step):
    graph = {}
    start = step // 2
    for y in range(start, img.shape[0], step):
        for x in range(start, img.shape[1], step):
            for w in range(img.shape[2]):
                if img[y, x, w] == 0:
                    neighbors = {}
                    for _y in [-step, 0, step]:
                        for _x in [-step, 0, step]:
                            for _w in [-step, 0, step]:
                                if _y == 0 and _x == 0 and _w == 0:
                                    continue
                                if 0 <= y + _y < img.shape[0] and 0 <= x + _x < img.shape[1] \
                                    and 0 <= w + _w < img.shape[2] and img[y + _y, x + _x, w + _w] == 0:
                                        neighbors[(x + _x, y + _y, w + _w)] = step * np.sqrt(_x**2 + _y**2 + _w**2)
                    graph[(x, y, w)] = neighbors
    return graph