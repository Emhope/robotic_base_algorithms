import utils
import numpy as np
import skimage
from graph_class import Graph


def _find_verts_on_layer(map):
    '''
    func for find vertices on 2d map
    '''
    res = utils.convolution(map.astype(bool), np.ones((5, 5))) * map.astype(bool)
    points = np.indices(res.shape)
    verts = points[:, res==12].astype(int)
    return verts


def find_verts(map3d):
    '''
    func for find vertices on 3d map
    '''
    verts = np.array([[], [], []], dtype=int)
    for i, l in enumerate(map3d):
        v = _find_verts_on_layer(l)
        v = np.concatenate(
            (
                np.ones((1, v.shape[1]), dtype=v.dtype)*i,
                v
            ), axis=0
        )
        verts = np.concatenate((verts, v), axis=1)
    return verts


def _check_vis(vert1, vert2, map3d, thresh=10):
    line = skimage.draw.line_nd(vert1, vert2)
    map_line = map3d[line]
    return map_line[map_line!=0].shape[0] < thresh
    


def create_graph(map3d):
    verts = find_verts(map3d)
    visual_graph = Graph()
    for v in verts.transpose():
        v = tuple(v)
        visual_graph.add_vert(v)
        for n in verts.transpose():
            n = tuple(n)
            if n == v:
                continue
            if _check_vis(v, n, map3d):
                visual_graph.add_edge(v, n)
    return visual_graph   

    