import numpy as np


def convolution(img, kernel):
    f = np.fft.fft2(img) * np.fft.fft2(kernel, s=img.shape)
    res = np.real(np.fft.ifft2(f))
    res[res > 255] = 255
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


def _perp_intersection_point(p1, p2, p3):
    k = ((p2[1]-p1[1]) * (p3[0]-p1[0]) - (p2[0]-p1[0]) * (p3[1]-p1[1])) / ((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)
    return (p3[0] - k * (p2[1]-p1[1]), p3[1] + k * (p2[0]-p1[0]))



def perp_intersection(p1, p2, p3):
    '''
    p1, p2 - start and end points of line
    p3 - point
    returns distance and point of intersection
    '''
    p4 = _perp_intersection_point(p1, p2, p3)
    
    eq1 = p4[0] >= min(p1[0], p2[0]) and p4[0] <= max(p1[0], p2[0])
    eq2 = p4[1] >= min(p1[1], p2[1]) and p4[1] <= max(p1[1], p2[1])
    if eq1 and eq2:
        return get_dist(p3, p4), p4
    else:
        return -1, None

