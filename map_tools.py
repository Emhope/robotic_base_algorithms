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


def _union_frames_bad_ver(coordinates, lidar):
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

def _union_frames(coordinates, lidar, step=0.01):

    step = 0.01
    points_all = [np.array([]), np.array([])]
    for i in range(coordinates.shape[0]):
        points_session = _calculate_session(coordinates[i], lidar[i])
        points_all[0] = np.concatenate((points_all[0], points_session[0]))
        points_all[1] = np.concatenate((points_all[1], points_session[1]))

    points_all = np.round(np.array(points_all)/step).astype(int)
    points_all[0] -= np.min(points_all[0])
    points_all[1] -= np.min(points_all[1])

    x_shape = -np.min(points_all[0]) + np.max(points_all[0])
    y_shape = -np.min(points_all[1]) + np.max(points_all[1])

    map = np.zeros((y_shape+1, x_shape+1), dtype=np.uint8)
    for i in range(points_all.shape[1]):
        map[points_all[1][i], points_all[0][i]] = 255
    map = cv2.blur(map, (11, 11))
    thresh = 100
    map[map > thresh] = 255
    map[map <= thresh] = 0
    return map


def create_map(fname):
    coordinates, lidar = _parse_lidar(fname)
    img = _union_frames(coordinates, lidar)
    return img
