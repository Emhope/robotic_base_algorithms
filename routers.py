import voronoi
import numpy as np
import config
from copy import deepcopy
from graph_class import Graph


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
    g.add_endpoint(goal)

    path = ...
    ...

    return g, path


@add_router('А*')
def a_star(graph, start, goal):
    g = deepcopy(graph)
    g.add_endpoint(start)
    g.add_endpoint(goal)

    path = ...
    ...

    return g, path
