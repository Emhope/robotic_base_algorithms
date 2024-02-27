import numpy as np
import cv2


def create_ceil_graph2d(img, step):
    arr = img[(step // 2)::step, (step // 2)::step]
    graph = {}
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            if arr[y, x] == 0:
                neighbors = []
                for _x, _y in [(x, y) for x in range(-1, 2) for y in range(-1, 2)]:
                        if (_x != 0 or _y != 0) and 0 <= x + _x < arr.shape[1] and 0 <= y + _y < arr.shape[0]:
                            if arr[y + _y, x + _x] == 0:
                                neighbors.append((x + _x, y + _y))
                graph[(x, y)] = neighbors
    return graph

