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
    

'''
start_point=(500, 250), end_point=(450, 700) # ok
start_point=(500, 250), end_point=(250, 760) # close to obst
start_point=(250, 300), end_point=(550, 800) # close on mline
start_point=(550, 800), end_point=(240, 450) # inf loop
start_point=(600, 900), end_point=(500, 290)
check if point is out of map
safe_dist = 0.3
safe_dist_right = 0.45
'''
def bug222(bin_map, start_point, end_point):
    # bin_map = cv2.imread('./raw_data/test_map.png', cv2.IMREAD_GRAYSCALE)
    # config_space = create_config_space(copy.copy(bin_map))
    start_point, end_point = tuple(reversed(start_point)), tuple(reversed(end_point))
    state = 'follow mline'
    safe_dist = 0.3
    safe_dist_right = 0.4
    mline = np.array(find_m_line(start_point, end_point))
    path = [[start_point[0]], [start_point[1]]]
    angles = []
    forw_flag = False
    flag_turn = False
    flag_back = False
    counter_right = 0
    counter_left = 0
    # for i in range(1250):
    res = copy.copy(bin_map)
    res_arr = []

    while state != 'goal_reached':

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
            # bin_map = config_space[int(angle_to_goal // config.angle_step),: ,:]
            flag = True
            while flag:

                i += 1
                if (mline[0][i], mline[1][i]) == end_point: # change
                    state = 'goal_reached'
                    curr_pos = [mline[0][i], mline[1][i]]        
                    path[0].extend([curr_pos[0]])
                    path[1].extend([curr_pos[1]])
                    angles.append(curr_angle)
                    break

                if not check_obst(curr_pos, curr_angle, bin_map, 0, safe_dist):
                    if check_obst(curr_pos, curr_angle, bin_map, -90, 0.2):
                        # if distance to obstacle is < safe_dist, then turn left
                        state = 'turn counterclock-wise'
                        last_mline_point = [curr_pos[0], curr_pos[1]]
                        mline = mline[:, i+1:]
                        break
                    else:
                        curr_pos = [mline[0][i], mline[1][i]]        
                        path[0].extend([curr_pos[0]])
                        path[1].extend([curr_pos[1]])
                        angles.append(curr_angle)
                else:
                    flag = False

                res[path[0][-1], path[1][-1]] = 200
                res_arr.append(copy.copy(res))

            else:
                state = 'turn counterclock-wise'   
                last_mline_point = [curr_pos[0], curr_pos[1]]
                mline = mline[:, i+1:]
            

        elif state == 'turn counterclock-wise':
            curr_angle += config.angle_step

            if abs(curr_angle) > 360:
                safe_dist_right = 0.5
                curr_angle %= 360
                counter_left += 1

            angles.append(curr_angle)
            curr_angle_conf = check_angle(curr_angle)
            # bin_map = config_space[int(curr_angle_conf // config.angle_step),: ,:]
           
            if check_obst(curr_pos, curr_angle, bin_map, -90, safe_dist_right) and not check_obst(curr_pos, curr_angle, bin_map, 0, safe_dist): # or flag_turn
                state = 'follow obstacle'
            
        
        elif state == 'turn clock-wise':
            curr_angle -= config.angle_step

            if abs(curr_angle) > 360:
                safe_dist_right = 0.5
                curr_angle %= 360
                counter_right += 1
                # state = 'follow obstacle'
            
            angles.append(curr_angle)
            curr_angle_conf = check_angle(curr_angle)
            # bin_map = config_space[int(curr_angle_conf // config.angle_step),: ,:]
            if (check_obst(curr_pos, curr_angle, bin_map, -90, safe_dist_right) or forw_flag) and not check_obst(curr_pos, curr_angle, bin_map, 0, 0.3):
                state = 'follow obstacle'
                forw_flag = False
            if check_obst(curr_pos, curr_angle, bin_map, 0, safe_dist):
                state = 'turn counterclock-wise'
                flag_turn = True
            


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

            if not check_obst(curr_pos, curr_angle, bin_map, -90, 0.3):
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
            return path, bin_map, mline, res_arr

        res[path[0][-1], path[1][-1]] = 200
        res_arr.append(copy.copy(res))
            
    return path, bin_map, mline, res_arr


def render_bug2(bin_map, start_point, end_point, fig, ax, canvas, fps=120):
    p222, bin_map, mline, res_arr = bug222(bin_map, start_point, end_point)
    def animate(i):
        img.set_array(res_arr[i*fps//10])
        canvas.draw()
        return img,

    img = ax.imshow(res_arr[0], animated=True, cmap='gray')
    ani = animation.FuncAnimation(fig, animate, frames=len(res_arr)//(fps//10), interval=100, repeat=True, blit=True)
