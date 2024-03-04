import numpy as np
from scipy.signal import convolve2d, fftconvolve
import PIL
import io

def convolution(img, kernel, dtype=None):
    res = convolve2d(img, kernel, mode='same')
    if dtype is None:
        res[res > 255] = 255
        return res.astype(np.uint8)
    return res.astype(dtype)
    

def fast_convolution(img, kernel):
    res = fftconvolve(img, kernel, mode='same')
    res[res>255] = 255
    return res.astype(np.uint8)


def minkowski(map, shape):
    k = np.ones((shape, shape)) * 255
    s = convolution(map, k)
    s[s>0] = 255
    return s


def get_dist(p1, p2):
    return np.linalg.norm(
        np.array(p1) - np.array(p2)
    )


def buffer_plot_and_get(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return PIL.Image.open(buf)


def _perp_intersection_point(p1, p2, p3):
    k = ((p2[1]-p1[1]) * (p3[0]-p1[0]) - (p2[0]-p1[0]) * (p3[1]-p1[1])) / ((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
    return (p3[0] - k * (p2[1]-p1[1]), p3[1] + k * (p2[0]-p1[0]))


def _on_line_seg(a1, a2, p):
    eq1 = p[0] >= min(a1[0], a2[0]) and p[0] <= max(a1[0], a2[0])
    eq2 = p[1] >= min(a1[1], a2[1]) and p[1] <= max(a1[1], a2[1])
    return eq1 and eq2


def perp_intersection(p1, p2, p3):
    '''
    p1, p2 - start and end points of line
    p3 - point
    returns distance and point of intersection
    '''
    p4 = _perp_intersection_point(p1, p2, p3)

    if _on_line_seg(p1, p2, p4):
        return get_dist(p3, p4), p4
    else:
        return -1, None

