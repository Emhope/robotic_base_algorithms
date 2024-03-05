import time
import cv2
import numpy as np


def _timer(func):

    def wrapp(*args, **kwargs):
        s = time.perf_counter()
        res = func(*args, **kwargs)
        print(f'{time.perf_counter() - s} s.')
        return res    
    return wrapp


def _save_res(func, test_name='test.png'):

    def wrapp(*args, **kwargs):
        res = func(*args, **kwargs)
        cv2.imwrite(test_name, res)
        return res
    
    return wrapp


def _hashe_solver(obj):
    if isinstance(obj, np.ndarray):
        return obj.tobytes()
    return obj


def memoize(func):
    cache = {}
    def wrapp(*args, **kwargs):
        h_args = tuple(_hashe_solver(i) for i in args)
        h_kwargs = tuple((_hashe_solver(k), _hashe_solver(v)) for k, v in kwargs.items())
        key = (h_args, h_kwargs)
        if key not in cache:
            res = func(*args, **kwargs)
            cache[key] = res
        return cache[key]
    return wrapp
