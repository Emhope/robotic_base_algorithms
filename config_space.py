import numpy as np 
import cv2 
from matplotlib import pyplot as plt
from PIL import Image
import scipy
import matplotlib.animation as animation
import utils
from config import step, h, w


def _create_robot_rotates():
    robot_shape = np.array((int(h/step), int(w/step)))
    robot = np.ones(robot_shape)
    robot = np.pad(robot, int(abs(h-w)/step)+5)
    robot_rotates = [scipy.ndimage.rotate(robot, angle, reshape=False, order=0) for angle in range(0, 180, 10)]
    return robot_rotates


def create_config_space(map):
    robot_rotates = _create_robot_rotates()
    configuration_space = np.zeros((len(robot_rotates),) + map.shape)

    for i, r in enumerate(robot_rotates):
        rot_map = utils.convolution(map, r)
        rot_map[rot_map>0] = 255
        configuration_space[i] = np.copy(rot_map)
    
    return configuration_space