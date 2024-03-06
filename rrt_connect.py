import numpy as np
import time
import cv2
import matplotlib.pyplot as plt

FREQ = 0.01

class RRTconnect:
    def __init__(self, img_path, step, threshold, max_iters=10000):
        self.map = self.get_map(img_path)
        self.step = step
        self.threshold = threshold
        self.max_iters = max_iters

    def get_map(self, path):
        img = cv2.imread(path, cv2.COLOR_BGR2GRAY)
        img = np.int32(img / 255)
        img = img.swapaxes(0, 1)
        return img
        
    # def get_map(self, path):
    #     map = np.zeros((10, 15))
    #     map[1:6, 3:6] = 1
    #     map = map.swapaxes(0, 1)
    #     return map
    
    def random_point(self):
        r_x = np.random.randint(0, self.map.shape[0])
        r_y = np.random.randint(0, self.map.shape[0])
        return np.array([r_x, r_y])

    def is_obstacle(self, point):
        if point[0] < self.map.shape[0] and point[1] < self.map.shape[1] \
            and self.map[point[0], point[1]] == 0:
            return False
        else:
            return True
        
    def intersection(self, p1, p2):
        line_map = np.zeros((self.map.shape[0], self.map.shape[1]))
        line_map = cv2.line(line_map, [p1[1], p1[0]], [p2[1], p2[0]], 1)
        if np.max(line_map * self.map) == 1:
            return True
        return False
                
    def distance(self, p1, p2):
        return np.linalg.norm(p1 - p2)
    
    def nearest(self, rand_p, tree):
        min_d = float('inf') 
        for i in range(len(tree)):
            p = np.array([tree[i][0], tree[i][1]])
            td = self.distance(p, rand_p)
            if td < min_d:
                min_d = td
                row = i
        near_p = np.array([tree[row][0], tree[row][1]])
        return near_p, row

    def extend_tree(self, p1, p2, step):
        if self.distance(p1, p2) < self.threshold:
            return p2
        else:
            theta = np.arctan2((p2[1] - p1[1]), (p2[0] - p1[0]))
            p_new = np.array([int(p1[0] + step * np.cos(theta)), int(p1[1] + step * np.sin(theta))])
            return p_new
    
    def get_path(self, start, goal):
        if self.is_obstacle(start) or self.is_obstacle(goal):
            print('Start or goal is obstacle')
            return
        tree1 = []
        tree1.append([start[0], start[1], -1])
        tree2 = []
        tree2.append([goal[0], goal[1], -1])
        flag = False
        self.iters = 0

        while self.iters < self.max_iters:
            rand_p = self.random_point()
            near_p1, num1 = self.nearest(rand_p, tree1) 
            new_p1 = self.extend_tree(near_p1, rand_p, self.step) 

            if self.is_obstacle(new_p1) or self.intersection(new_p1, near_p1):
                # self.plot_node(new_p1)
                self.iters += 1
                if len(tree2) < len(tree1):
                    tree1, tree2 = tree2, tree1
                continue
            else:
                tree1.append([new_p1[0], new_p1[1], num1])
                self.plot_tree(tree1, tree2)
                near_p2, num2 = self.nearest(new_p1, tree2) 
                new_p2 = self.extend_tree(near_p2, new_p1, self.step)

                if self.is_obstacle(new_p2) or self.intersection(new_p2, near_p2):
                    # self.plot_node(new_p2)
                    self.iters += 1
                    if len(tree2) < len(tree1):
                        tree1, tree2 = tree2, tree1
                    continue
                else:
                    tree2.append([new_p2[0], new_p2[1], num2])
                    self.plot_tree(tree1, tree2)
                    new_new_p2 = self.extend_tree(new_p2, new_p1, self.step) 

                    if self.is_obstacle(new_new_p2) or self.intersection(new_new_p2, new_p2):
                        # self.plot_node(new_new_p2)
                        self.iters += 1
                        if len(tree2) < len(tree1):
                            tree1, tree2 = tree2, tree1
                        continue
                    else:
                        tree2.append([new_new_p2[0], new_new_p2[1], len(tree2)-1])
                        self.plot_tree(tree1, tree2)
                        new_p2 = new_new_p2

                        while self.distance(new_p2, new_p1) > self.threshold:
                            new_new_p2 = self.extend_tree(new_p2, new_p1, self.step) 
                            if self.is_obstacle(new_new_p2) or self.intersection(new_new_p2, new_p2):
                                # self.plot_node(new_new_p2)
                                self.iters += 1
                                break
                            else:
                                tree2.append([new_new_p2[0], new_new_p2[1], len(tree2)-1])
                                self.plot_tree(tree1, tree2)
                                new_p2 = new_new_p2
                        else:
                            tree2.append([new_p1[0], new_p1[1], len(tree2)-1])
                            self.plot_tree(tree1, tree2)
                            flag = True
                            break

                if len(tree2) < len(tree1):
                    tree1, tree2 = tree2, tree1

        if flag:
            path1 = []
            i = -1
            ni = tree1[-1][2]
            while ni != -1:
                path1.append([tree1[i][0], tree1[i][1]])
                i = ni
                ni = tree1[i][2]
            path1.append([tree1[0][0], tree1[0][1]])

            path2 = []
            i = -1
            ni = tree2[-1][2]
            while ni != -1:
                path2.append([tree2[i][0], tree2[i][1]])
                i = ni
                ni = tree2[i][2]
            path2.append([tree2[0][0], tree2[0][1]])

            return np.array(path1), np.array(path2), np.array(tree1), np.array(tree2)

        else:
            print('Reached max iterations')

    def plot_map(self):
        plt.clf()
        plt.imshow(self.map.swapaxes(0, 1), cmap='gray', extent=[0, self.map.shape[0], self.map.shape[1], 0], origin='upper')
        plt.pause(FREQ)

    def plot_tree(self, tree1, tree2):
        plt.clf()
        plt.imshow(self.map.swapaxes(0, 1), cmap='gray', extent=[0, self.map.shape[0], self.map.shape[1], 0], origin='upper')
        for node in tree1:
            if node[2] != -1:
                plt.scatter(node[0], node[1], color='red', s=1)
                plt.plot([node[0], tree1[node[2]][0]], [node[1], tree1[node[2]][1]], 'red', linewidth=1)
        for node in tree2:
            if node[2] != -1:
                plt.scatter(node[0], node[1], color='blue', s=1)
                plt.plot([node[0], tree2[node[2]][0]], [node[1], tree2[node[2]][1]], 'blue', linewidth=1)
        plt.pause(FREQ)

    def plot_node(self, node):
        plt.clf()
        plt.imshow(self.map.swapaxes(0, 1), cmap='gray', extent=[0, self.map.shape[0], self.map.shape[1], 0], origin='upper')
        plt.scatter(node[0], node[1], color='red', s=1)
        plt.pause(FREQ)

    def plot_path(self, path1, path2):
        plt.clf()
        plt.imshow(self.map.swapaxes(0, 1), cmap='gray', extent=[0, self.map.shape[0], self.map.shape[1], 0], origin='upper')
        plt.plot(path1[:, 0], path1[:, 1], 'red', linewidth=1)
        plt.plot(path2[:, 0], path2[:, 1], 'blue', linewidth=1)
        plt.show()

if __name__ == '__main__':
    rrt = RRTconnect(img_path='tmp/test.png', 
                     step=100, 
                     threshold=100,
                     max_iters=1000)
    
    start = [100, 100]
    goal = [500, 500]

    path1, path2, tree1, tree2 = rrt.get_path(start, goal)
    rrt.plot_map()
    rrt.plot_path(path1, path2)
    print(f'iterations: {rrt.iters}')
