import numpy as np
from graph_class import Graph
import skimage
import utils


def _on_map(v, map_shape):
    return (0 <= v[0] < map_shape[1]) and (0 <= v[1] < map_shape[0])


def _perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def _seg_intersect(a1, a2, b1, b2):
    # line segment a given by endpoints a1, a2
    # line segment b given by endpoints b1, b2
    a1 = np.array(a1)
    a2 = np.array(a2)
    b1 = np.array(b1)
    b2 = np.array(b2)

    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = _perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    return (num / denom.astype(float))*db + b1


def _create_frame_lines(frame_shape, border_width=1):
    up_left = np.array([0, 0])
    up_right = np.array([frame_shape[1]-border_width, 0])
    down_left = np.array([0, frame_shape[0]-border_width])
    down_right = np.array([frame_shape[1]-border_width, frame_shape[0]-border_width])
    lines = [
        [up_left, up_right],
        [up_right, down_right],
        [down_right, down_left],
        [down_left, up_left],
    ]
    return lines


def _frame_intersect(p1, p2, frame_shape):
    flines = _create_frame_lines(frame_shape)
    for l1, l2 in flines:
        p = _seg_intersect(p1, p2, l1, l2)
        if utils._on_line_seg(p1, p2, p) and _on_map(p, frame_shape):
            return p.astype(int)


def _rm_away_verts(g: Graph, map_shape):
    for v in list(g.keys()):
        if not _on_map(v, map_shape):
            g.remove_vertex(v)


def _divide_edges_on_border(g: Graph, map: np.ndarray):
    for v1, v2 in g.get_edges():
        v1_on_map = _on_map(v1, map.shape)
        v2_on_map = _on_map(v2, map.shape)
        if not ((v1_on_map and (not v2_on_map)) or (v2_on_map and (not v1_on_map))):
            continue
        
        g.remove_edge(v1, v2)
        fpoint = tuple(_frame_intersect(v1, v2, map.shape))
        if v1_on_map:
            g.add_edge(v1, fpoint)
        else:
            g.add_edge(v2, fpoint)
        _rm_away_verts(g, map.shape)


def _obs_intersection(p1, p2, map):
    line = skimage.draw.line(*p1, *p2)
    mline = map[line[::-1]]
    p1_intersect, p2_intersect = None, None
    
    for n, i in enumerate(mline):
        if i:
            p1_intersect = (line[0][n], line[1][n])
            break
    for n, i in enumerate(mline[::-1]):
        if i:
            p2_intersect = (line[0][-n-1], line[1][-n-1])
            break
        
    return p1_intersect, p2_intersect

    

def _divide_edges_on_obs(g: Graph, map: np.ndarray):
    for v1, v2 in g.get_edges():
        v1_intersect, v2_intersect = _obs_intersection(v1, v2, map)
        if v1_intersect is None and v2_intersect is None:
            continue
        if v1 != v1_intersect:
            g.add_edge(v1, v1_intersect)
        if v2 != v2_intersect:
            g.add_edge(v2, v2_intersect)
        g.remove_edge(v1, v2)


def _find_cycles(g: Graph):
    cycles = []
    for v in g:
        v_neighbors = set(n for n, w in g[v])
        v_neighbors |= {v}
        
        intersex = []
        for c in cycles:
            if v_neighbors & c:
                intersex.append(c)
        
        inter_sum = v_neighbors
        for i in intersex:
            inter_sum |= (i)
            cycles.remove(i)
        cycles.append(inter_sum)
    
    return cycles


def _rm_side_cycles(g: Graph):
    main_cycle = max(_find_cycles(g), key=len)
    for v in list(g.keys()):
        if v not in main_cycle:
            g.remove_vertex(v)


def verificate(g: Graph, map):
    _divide_edges_on_border(g, map)
    _divide_edges_on_obs(g, map)
    _rm_side_cycles(g)
    