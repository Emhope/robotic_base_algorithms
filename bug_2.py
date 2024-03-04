import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import cv2
import copy
import math
from skimage.draw import line
from config_space import create_config_space
import matplotlib.animation as animation
import config 
import time


def find_m_line(start, end):
    '''find m-line from start position to goal'''
    rr, cc = line(*start, *end)
    return (rr, cc)

def find_angle(x_start, y_start, x_end, y_end):
    ''''find angle between m-line and horizont'''
    dy = -y_end + y_start
    dx = x_end - x_start
    angle = math.atan2(dy, dx)
    return math.degrees(angle)

def check_obst(curr_pos, curr_angle, bin_map, angle, safe_dist=0.3):
    safe_dist /= config.step
    angle_point = math.radians(curr_angle + angle)
    y, x = -math.sin(angle_point) * safe_dist + curr_pos[0], math.cos(angle_point) * safe_dist + curr_pos[1]    
    rr, cc = line(*(int(curr_pos[0]), int(curr_pos[1])), *(round(y), round(x)))

    return np.any(bin_map[rr, cc] == 255)


def check_angle(angle):
    if angle > 180:
        return  (angle - 180) % 180
    elif abs(angle) > 180 and angle < 0:
        return (360 + angle) % 180
    elif angle < 0 and abs(angle) < 180:
        return (180 + angle) % 180
    else:
        return angle
    

def bug2(bin_map, start_point, end_point):
    start_point, end_point = tuple(reversed(start_point)), tuple(reversed(end_point))
    state = 'follow mline'
    safe_dist = 0.3
    safe_dist_right = 0.4
    mline = np.array(find_m_line(start_point, end_point))
    path = [[start_point[0]], [start_point[1]]]
    forw_flag = False
    flag_back = False
    counter_right = 0
    counter_left = 0
    counter = 0
    res = copy.copy(bin_map)
    res = ~res
    res_arr = []

    while state != 'goal_reached':
        counter += 1

        if state == 'follow mline':                       
            i = 0
            safe_dist_right = 0.4

            if flag_back:
                mline = mline[:, index:]
                
            angle_to_goal = find_angle(mline[1][0], mline[0][0], mline[1][-1], mline[0][-1])
            curr_pos = [path[0][-1], path[1][-1]]

            if (curr_pos[0], curr_pos[1]) == end_point:
                state = 'goal_reached'
                break
            
            curr_angle = angle_to_goal
            flag = True

            while flag:
                counter += 1
                i += 1

                if (mline[0][i], mline[1][i]) == end_point:
                    state = 'goal_reached'
                    curr_pos = [mline[0][i], mline[1][i]]        
                    path[0].extend([curr_pos[0]])
                    path[1].extend([curr_pos[1]])
                    break

                if not check_obst(curr_pos, curr_angle, bin_map, 0, safe_dist):
                    if check_obst(curr_pos, curr_angle, bin_map, -90, 0.2):
                        # if distance to obstacle is < safe_dist, then turn left
                        state = 'turn counterclock-wise'
                        mline = mline[:, i+1:]
                        break
                    else:
                        curr_pos = [mline[0][i], mline[1][i]]        
                        path[0].extend([curr_pos[0]])
                        path[1].extend([curr_pos[1]])

                else:
                    flag = False

                res[path[0][-1], path[1][-1]] = 30
                res_arr.append(copy.copy(res))

            else:
                state = 'turn counterclock-wise'   
                mline = mline[:, i+1:]
            

        elif state == 'turn counterclock-wise':
            curr_angle += config.angle_step

            if abs(curr_angle) > 360:
                safe_dist_right = 0.5
                curr_angle %= 360
                counter_left += 1
           
            if check_obst(curr_pos, curr_angle, bin_map, -90, safe_dist_right) and not check_obst(curr_pos, curr_angle, bin_map, 0, safe_dist): # or flag_turn
                state = 'follow obstacle'
            
        
        elif state == 'turn clock-wise':
            curr_angle -= config.angle_step

            if abs(curr_angle) > 360:
                safe_dist_right = 0.5
                curr_angle %= 360
                counter_right += 1

            if (check_obst(curr_pos, curr_angle, bin_map, -90, safe_dist_right) or forw_flag) and not check_obst(curr_pos, curr_angle, bin_map, 0, 0.3):
                state = 'follow obstacle'
                forw_flag = False
            if check_obst(curr_pos, curr_angle, bin_map, 0, safe_dist):
                state = 'turn counterclock-wise'
            

        elif state == 'follow obstacle': 
            # safe_dist_right = 0.4
            y, x = -math.sin(math.radians(curr_angle)) + curr_pos[0], math.cos(math.radians(curr_angle)) + curr_pos[1] # *safe_dist
            rr, cc = line(*(curr_pos[0], curr_pos[1]), *(round(y), round(x)))   
 
            path[0].extend(rr)
            path[1].extend(cc)
            curr_pos = [path[0][-1], path[1][-1]]

            if check_obst(curr_pos, curr_angle, bin_map, -90, 0.2):
                # if distance to obstacle is < safe_dist, then turn left
                state = 'turn counterclock-wise'

            if not check_obst(curr_pos, curr_angle, bin_map, -90, safe_dist_right):
                state = 'turn clock-wise'

            if check_obst(curr_pos, curr_angle, bin_map, 0, safe_dist):
                state = 'turn counterclock-wise'
                                    
        mask_x = curr_pos[0] == mline[0]
        mask_y = curr_pos[1] == mline[1]
        mask = mask_x & mask_y

        if (curr_pos[0], curr_pos[1]) == end_point:
            state = 'goal_reached'

           
        if np.any(mask):  
            state = 'follow mline'
            index = list(mask).index(True)
            flag_back = True

        if counter_right > 2 or counter_right > 2:
            return path, res_arr

        res[path[0][-1], path[1][-1]] = 30
        res_arr.append(copy.copy(res))
            
    return path, res_arr


def render_bug2(bin_map, start_point, end_point, fig, ax, canvas, fps=120):
    path, res_arr = bug2(bin_map, start_point, end_point)
    start_dot, = ax.plot(*start_point, 'go')
    end_dot, = ax.plot(*end_point, 'ro')
    def animate(i):
        img.set_array(res_arr[i*fps//10])
        canvas.draw()
        return img, start_dot, end_dot

    img = ax.imshow(res_arr[0], animated=True, cmap='gray')
    ani = animation.FuncAnimation(fig, animate, frames=len(res_arr)//(fps//10), interval=100, repeat=True, blit=True)

