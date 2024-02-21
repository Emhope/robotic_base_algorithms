from matplotlib import pyplot as plt
import numpy as np
import cv2
import os
import time


def _parse_lidar(fname):
    '''
    Парсит сырую информацию
    возвращает 2 массива: массив лидара и массив координат (x, y, w)
    '''
    coordinates = []
    lidar = []

    with open(fname, 'r') as file:
        for row in file.readlines():
            coordinates.append([float(i) for i in row.split('; ')[0].split(', ')])
            lidar.append([float(i) for i in row.split('; ')[1].split(', ')])

    coordinates = np.array(coordinates)
    lidar = np.array(lidar)

    return (coordinates, lidar)


def _calculate_session(pos, lidar_data):
    '''
    Перевод одного прохода лидара в декартовы координаты
    возвразает массив иксов и игриков точек лидара, связанных с координатами робота
    '''
    lidar_data = lidar_data.copy()
    lidar_data[lidar_data == 5.6] = np.nan
    lidar_data[lidar_data < 0.3] = np.nan
    
    angles = np.linspace(pos[2] + 2*np.pi/3, pos[2] - 2*np.pi/3, len(lidar_data))

    x = np.array(lidar_data * np.cos(angles) + pos[0])
    x = x[~np.isnan(x)]
    y = np.array(lidar_data * np.sin(angles) + pos[1])
    y = y[~np.isnan(y)]
    
    return [x, y] 


def _union_frames(coordinates, lidar):
    res = None

    for i in range(coordinates.shape[0]):
        fig, ax = plt.subplots()
        fig.set_figheight(20)
        fig.set_figwidth(20)
        ax.axis('off')
        ax.set_xlim((0, 10))
        ax.set_ylim((-6, 4))
        ax.set_aspect (1)
        points_session = _calculate_session(coordinates[i], lidar[i])
        ax.scatter(points_session[0], points_session[1], 1, 'k')
        
        fig.savefig(f'tmp/tmp_frame.jpg', dpi=100, transparent=True)
        plt.close()
        
        data = cv2.imread('tmp/tmp_frame.jpg')
        data = cv2.Canny(cv2.blur(data, (9, 9)), 100, 200)
        
        cv2.imwrite('tmp/tmp_frame.jpg', data)
        data = data = cv2.imread('tmp/tmp_frame.jpg', cv2.IMREAD_GRAYSCALE)
        
        if res is None:
            res = np.copy(data)
        
        res = np.logical_or(data, res)


    os.remove('tmp/tmp_frame.jpg')

    res = cv2.blur(res.astype(np.uint8) * 255, (13, 13))
    thresh = 150
    res[res < thresh] = 0
    res[res >= thresh] = 255

    return res


def _timer(func):

    def wrapp(*args, **kwargs):
        s = time.perf_counter()
        res = func(*args, **kwargs)
        print(f'{time.perf_counter() - s} s.')
        return res    
    return wrapp


def _save_res(func, test_name='test.jpg'):

    def wrapp(*args, **kwargs):
        res = func(*args, **kwargs)
        cv2.imwrite(test_name, res)
        return res
    
    return wrapp

@_timer
@_save_res
def create_map(fname):
    coordinates, lidar = _parse_lidar(fname)
    img = _union_frames(coordinates, lidar)
    return img

create_map('raw_data/examp17.txt')