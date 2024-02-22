import numpy as np
import cv2


def create_ceil_graph(img, step):
    arr = img[(step // 2)::step, (step // 2)::step]
    graph = {}
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            if arr[y, x] == 0:
                neighbors = []
                for _x, _y in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        if (_x != 0 or _y != 0) and 0 <= x + _x < arr.shape[1] and 0 <= y + _y < arr.shape[0]:
                            if arr[y + _y, x + _x] == 0:
                                neighbors.append((x + _x, y + _y))
                graph[(x, y)] = neighbors
    return graph
