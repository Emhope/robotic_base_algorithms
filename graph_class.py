import numpy as np
import utils
from matplotlib import pyplot as plt


class Graph(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k in self:
            self[k] = list(set(self[k]))
        self.tree = dict()


    def get_edges(self):    
        edges = []
        for n in self:
            for neighbor in self[n]:
                edge = tuple(sorted([n, neighbor[0]]))
                edges.append(edge)
        return list(set(edges))
    

    def remove_edge(self, vert1, vert2, hold=False):
        if vert1 in self:
            for n in self[vert1]:
                if vert2 == n[0]:
                    self[vert1].remove(n)
                    if (not self[vert1]) and (not hold):
                        self.remove_vertex(vert1)
                    break
        
        if vert2 in self:
            for n in self[vert2]:
                if vert1 == n[0]:
                    self[vert2].remove(n)
                    if not (not self[vert2]) and (not hold):
                        self.remove_vertex(vert2)
                    break
            
    
    def add_edge(self, vert1, vert2, heritage=False, ax=None, edge_color='red', vert_color='blue'):
        '''vert1 - parent for vert2 if herigate True'''
        self[vert1] = list(set((self.get(vert1, list()) + [(vert2, utils.get_dist(vert1, vert2))])))
        self[vert2] = list(set((self.get(vert2, list()) + [(vert1, utils.get_dist(vert1, vert2))])))

        if heritage:
            self.tree[vert2] = vert1

        if ax is not None:
            ax.plot([vert1[0], vert2[0]], [vert1[1], vert2[1]], color=edge_color)


    def add_vert(self, vert, heritage=False):
        self.setdefault(vert, list())
        if heritage:
            self.tree[vert] = vert
 
    
    def draw_graph(self, ax=None, show_verts=True):
        if ax is None:
            fig, ax = plt.subplots()
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 1000)
        for vert in self:
            for n in self[vert]:
                ax.plot([vert[0], n[0][0]], [vert[1], n[0][1]], 'red', 10)
            if len(self[vert]) == 1 and show_verts:
                ax.scatter(*vert, 100, 'yellow')
            elif show_verts:
                ax.scatter(*vert, 100, 'b')


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
    

    def get_weight(self, vert1, vert2):
        for v in self[vert1]:
            if v[0] == vert2:
                return v[1]


    def get_parent(self, vert):
        # min_ind = np.inf
        # keys = list(self.keys())
        # neighbors = [v for v, w in self[vert]]
        # for i in keys:
        #      if i in neighbors:
        #          ind = keys.index(i)
        #          if ind < min_ind:
        #              min_ind = ind
        # return keys[min_ind]
        return self.tree[vert]
    