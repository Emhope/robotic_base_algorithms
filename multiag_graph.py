import networkx as nx
from matplotlib import pyplot as plt
import map_tools
import config
import numpy as np
import cv2
import utils
import json
from progress.bar import IncrementalBar


def expand_map(dmap, robot_d):
    robot_d = int(robot_d/config.step)
    r_circle = np.zeros((robot_d+1, robot_d+1))
    cv2.circle(r_circle, (robot_d//2, robot_d//2), robot_d//2, 255, thickness=-1)
    res = utils.fast_convolution(dmap, r_circle)
    res[res>0] = 255
    return res


def discretize_map(my_map, step):
    return my_map[::step, ::step]


def create_graph_2robots(dmap, dstep):
    
    nodes = []
    bar = IncrementalBar('creating nodes  ', max = dmap.shape[0]*dmap.shape[1])
    for y1 in range(dmap.shape[0]):
        for x1 in range(dmap.shape[1]):
            bar.next()
            if dmap[y1, x1]:
                continue
            for y2 in range(dmap.shape[0]):
                for x2 in range(dmap.shape[1]):
                    if dmap[y2, x2] or (y1 == y2 and x1 == x2):
                        continue
                    node = (x1*dstep, y1*dstep, x2*dstep, y2*dstep)
                    nodes.append(node)
                    
    print()

    deltas = []
    for x1 in range(-1, 2):
        for y1 in range(-1, 2):
            for x2 in range(-1, 2):
                for y2 in range(-1, 2):
                    if (x1 == 0 or y1 == 0) and (x2 == 0 or y2 == 0):
                        deltas.append((x1*dstep, y1*dstep, x2*dstep, y2*dstep))

    bar = IncrementalBar('connecting nodes', max = len(nodes)*len(deltas))
    
    graph = nx.Graph()
    for n in nodes:
        str_n = ' '.join(map(str, n))
        for d in deltas:
            bar.next()
            new_n = tuple(i + j for i, j in zip(n, d))
            # swap places check
            if n[:2] == new_n[2:] and n[2:] == new_n[:2]:
                continue

            if new_n not in nodes:
                continue

            w = sum(map(abs, d))
            graph.add_edge(str_n, ' '.join(map(str, new_n)), weight=w)
    
    print()
    return graph


map_num = input(  '             номер карты (2 - 17): ')
dstep = int(input('шаг дискретизации (70 ~ 1.5 часа): '))

my_map = map_tools.create_map(f'./raw_data/examp{map_num}.txt')
my_map = expand_map(my_map, 0.2)
my_map = discretize_map(my_map, dstep)


plt.imshow(my_map)
plt.show()

g = create_graph_2robots(my_map, dstep)

with open(f'multiag_graph{map_num}d{dstep}.json', 'w') as file:
    json.dump(nx.to_dict_of_dicts(g), file)
