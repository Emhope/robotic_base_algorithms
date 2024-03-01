import time
import cv2


def _timer(func):

    def wrapp(*args, **kwargs):
        s = time.perf_counter()
        res = func(*args, **kwargs)
        print(f'{time.perf_counter() - s} s.')
        return res    
    return wrapp


def _save_res(func, test_name): # = 'test.png'

    def wrapp(*args, **kwargs):
        res = func(*args, **kwargs)
        cv2.imwrite(test_name, res)
        return res
    
    return wrapp
