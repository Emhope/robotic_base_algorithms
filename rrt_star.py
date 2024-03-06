import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import scipy
import matplotlib.animation as animation
import utils
import config_space
import map_tools
import voronoi
from pprint import pprint
import graph_class
from scipy.signal import convolve2d
import skimage
import config
import vis_graph
import time
import ceil_decomp
import pickle
import matplotlib.animation as animation
import copy
import random
import io
import PIL



def find_nearest(graph, point):
    temp_dist = []
    vertices = list(graph.keys())
    
    for i in range(len(vertices)):
        dist = np.linalg.norm(np.array(point) - np.array(vertices[i]))
        temp_dist.append(dist)
        
    return vertices[temp_dist.index(min(temp_dist))]


def find_neighborhood(graph, point, r, map):
    n = []
    for v in graph:
        if v != point:
            if check_goal(r, point, v) and check_vis(v ,point, map):
                n.append(v)
    return n


def check_vis(vert1, vert2, bin_map, thresh=0):
    l = skimage.draw.line(*vert1, *vert2)
    map_line = bin_map[l[::-1]]
    return map_line[map_line!=0].shape[0] <= thresh


def set_random_point(bin_map):
    point = (random.randint(0, bin_map.shape[0] - 1), random.randint(0, bin_map.shape[1] - 1))
    return point


def check_goal(region, vert, goal):
    return np.linalg.norm(np.array(vert) - np.array(goal)) <= region


def on_map(v, map_shape):
    return (0 <= v[0] < map_shape[1]) and (0 <= v[1] < map_shape[0])


def get_cost(g: graph_class.Graph, start, end):
    path = [end]
    cost = 0
    while path[-1] != start:
        try:
            parent = g.get_parent(path[-1])
        except:
            return np.inf
        if parent in path:
            return np.inf
        path.append(parent)
        cost += np.linalg.norm(np.array(path[-1])-np.array(path[-2]))
    return cost


def rrt_star(start, end, bin_map, region, max_distance, neigborhood_rad, ax=None):
    surf = np.copy(bin_map)
    region /= config.step
    max_distance /= config.step
    neigborhood_rad /= config.step
    graph = graph_class.Graph()
    goal =  False
    graph.add_vert(start, heritage=True)
    its = 1
    while True:
        if its == 0:
            its = int(input('сколько еще итераций? '))
            if its <= 0:
                yield graph, rand_point
                break
        rand_point = set_random_point(bin_map)
        nearest_vert = find_nearest(graph, rand_point)
        dist_to_point = np.linalg.norm(nearest_vert - np.array(rand_point)) # distance between nearest and current random point\
        if dist_to_point > max_distance:
            x_new = int(max_distance * rand_point[0] // dist_to_point)
            y_new = int(max_distance * rand_point[1] // dist_to_point)
            rand_point = (x_new, y_new)

        
        if not on_map(rand_point, bin_map.shape):
            continue

        if (not check_vis(rand_point, nearest_vert, bin_map)) or (rand_point in graph) or rand_point == end:
            continue

        if check_goal(region, rand_point, end) and check_vis(rand_point, end, bin_map) and not goal:
            goal = True
            graph.add_edge(nearest_vert, rand_point, heritage=True)
            yield graph, rand_point

            graph.add_edge(rand_point, end, heritage=True)
            yield graph, end
        
        graph.add_edge(nearest_vert, rand_point, heritage=True)
        cv2.line(surf, rand_point, nearest_vert, 150, 4)
        cv2.circle(surf, start, 20, 100, -1)
        cv2.circle(surf, end, 20, 200, -1)
        ax.clear()
        ax.imshow(surf)

        neigborhood = find_neighborhood(graph, rand_point, neigborhood_rad, bin_map)
        for n in neigborhood:
            if n == nearest_vert or (not check_vis(n, rand_point, bin_map)) or n == start or n == end:
                continue
            old_cost = get_cost(graph, end=n, start=start)
            old_parent = graph.get_parent(n)
            graph.remove_edge(n, old_parent, hold=True)
            graph.add_edge(rand_point, n, heritage=True)
            new_cost = get_cost(graph, end=n, start=start)
            if new_cost >= old_cost:
                graph.remove_edge(n, rand_point, hold=True)
                graph.add_edge(old_parent, n, heritage=True)
            else:
                ax.clear()
                surf = np.copy(bin_map)
                s = time.perf_counter()
                for e in graph.get_edges():
                    cv2.line(surf, e[0], e[1], 150, 4)
                cv2.circle(surf, start, 20, 100, -1)
                cv2.circle(surf, end, 20, 200, -1)
                ax.imshow(surf)
        
        if goal:
            path = [end]
            while path[-1] != start:
                parent = g.get_parent(path[-1])
                path.append(parent)
            path = np.array(path).transpose()
            ax.plot(path[0, :], path[1, :], color='red')
        yield graph, rand_point
        its -= 1

        if ax is not None:
            ax.plot()


m_num = input('номер карты (2 - 17): ')
map = map_tools.create_map(f'raw_data/examp{m_num}.txt')
r = np.ones((10, 10))
map = utils.fast_convolution(map, r)
start = tuple(int(i) for i in input('старт: <x y> ').split())
goal = tuple(int(i) for i in input('конец: <x y> ').split())

fig, ax = plt.subplots()

graph_gen = rrt_star(start, goal, map, region=1, max_distance=2, neigborhood_rad=2, ax=ax)

ax.imshow(map)

for g, new_v in graph_gen:
    plt.show(block=False)
    plt.pause(0.01)
