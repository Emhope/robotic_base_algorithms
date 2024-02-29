import voronoi
import numpy as np
import config
from copy import deepcopy
from graph_class import Graph
import heapq


routers = dict()

def add_router(name):
    def adder(f):
        routers[name] = f
        return f
    return adder

@add_router('Алгоритм Дейкстры')
def dijkstra(graph: Graph, start, goal):
    g = deepcopy(graph)
    g.add_endpoint(start)

    # path = ...

    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        curr_dist, curr_node = heapq.heappop(priority_queue)
        if curr_node == goal:
            path = []
            while curr_node is not None:
                path.append(curr_node)
                curr_node = predecessors[curr_node]
            path.reverse()
            return path, distances[goal]
        for neighbor, weight in graph[curr_node].items():
            dist = curr_dist + weight
            if dist < distances[neighbor]:
                distances[neighbor] = dist
                predecessors[neighbor] = curr_node
                heapq.heappush(priority_queue, (dist, neighbor))
    return None, float('infinity')
    # return g, path

def _euclid_dist(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

@add_router('А*')
def a_star(graph, start, goal):
    g = deepcopy(graph)
    g.add_endpoint(start)
    g.add_endpoint(goal)

    # path = ...
    
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        curr_dist, curr_node = heapq.heappop(priority_queue)
        if curr_node == goal:
            path = []
            while curr_node is not None:
                path.append(curr_node)
                curr_node = predecessors[curr_node]
            path.reverse()
            return path, distances[goal]
        for neighbor, weight in graph[curr_node].items():
            dist = curr_dist + weight
            heuristic = _euclid_dist(neighbor, goal)
            total_dist = dist + heuristic
            if total_dist < distances[neighbor]:
                distances[neighbor] = total_dist
                predecessors[neighbor] = curr_node
                heapq.heappush(priority_queue, (total_dist, neighbor))
    return None, float('infinity')

    # return g, path
