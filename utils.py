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
