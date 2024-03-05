import numpy as np
import utils
from matplotlib import pyplot as plt


class Graph(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k in self:
            self[k] = list(set(self[k]))

    def get_edges(self):    
        edges = []
        for n in self:
            for neighbor in self[n]:
                edge = tuple(sorted([n, neighbor[0]]))
                edges.append(edge)
        return list(set(edges))
    
    def remove_edge(self, vert1, vert2):
        if vert1 in self:
            for n in self[vert1]:
                if vert2 == n[0]:
                    self[vert1].remove(n)
                    if not self[vert1]:
                        self.remove_vertex(vert1)
                    break
        
        if vert2 in self:
            for n in self[vert2]:
                if vert1 == n[0]:
                    self[vert2].remove(n)
                    if not self[vert2]:
                        self.remove_vertex(vert2)
                    break
            
    
    def add_edge(self, vert1, vert2):
        self[vert1] = list(set((self.get(vert1, list()) + [(vert2, utils.get_dist(vert1, vert2))])))
        self[vert2] = list(set((self.get(vert2, list()) + [(vert1, utils.get_dist(vert1, vert2))])))


    def add_vert(self, vert):
        self.setdefault(vert, list())
 
    
    def draw_graph(self, edge_color='black', vert_color='blue', ax=None):
        if ax is None:
            fig, ax = plt.subplots()
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 1000)
        for vert in self:
            for n in self[vert]:
                ax.plot([vert[0], n[0][0]], [vert[1], n[0][1]], markersize=10, color=edge_color)
            ax.scatter(*vert, 100, color=vert_color)


    def remove_vertex(self, vertex):
        if vertex not in self:
            return
        rm_vertices = []
        for n in self[vertex]:
            rm_vertices.append(n[0])
        for v in rm_vertices:
            self.remove_edge(v, vertex)
        if vertex in self:
            self.pop(vertex)


    def remove_endpoint(self, endpoint):
        if len(self[endpoint]) != 1:
            raise ValueError(f'{endpoint} is not endpoint')
        neighbor = self[endpoint][0][0]
        self.remove_vertex(endpoint)
        self.add_edge(self[neighbor][0][0], self[neighbor][1][0])
        self.remove_vertex(neighbor)
    
    
    def add_endpoint(self, new_p):
        '''
        adding goal or end point to graph
        '''
        lines = self.get_edges()
        min_dist, point, line = np.inf, None, None
        for l in lines:
            d, p = utils.perp_intersection(l[0], l[1], new_p)
            if 0 < d < min_dist:
                min_dist = d
                point = p
                line = l
        
        if point is not None:
            self.remove_edge(*line)
            self.add_edge(line[0], point)
            self.add_edge(line[1], point)
            self.add_edge(new_p, point)
        