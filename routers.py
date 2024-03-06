import voronoi
import numpy as np
import config
from copy import deepcopy
from graph_class import Graph
import heapq
from utils import buffer_plot_and_get
import matplotlib.pyplot as plt
import matplotlib.animation as animation


routers = dict()

def add_router(name):
    def adder(f):
        routers[name] = f
        return f
    return adder

@add_router('Алгоритм Дейкстры')
def dijkstra(graph, start, goal):
    path = []
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    priority_queue = [(0, start)]

    images = []
    fig, ax = plt.subplots()

    iteration = 0
    while priority_queue:
        curr_dist, curr_node = heapq.heappop(priority_queue)
        print(curr_node)
        
        pq_nodes = [x[1] for x in priority_queue]
        for node in graph.keys():
            
            if len(node) == 2:
                color = 'white'
                if node == goal:
                    color = 'red'  # Целевая вершина
                elif node == curr_node:
                    color = 'yellow'  # Текущая вершина
                elif node in pq_nodes:
                    color = 'blue'  # Открытая вершина
                elif distances[node] != float('infinity'):
                    color = 'gray'  # Закрытая вершина

                ax.plot(node[0], node[1], marker='o', markersize=10, color=color)

                for neighbor, _ in graph[node]:
                    ax.plot([node[0], neighbor[0]], [node[1], neighbor[1]], color='gray')

            else:
                color = 'white'
                if node == goal:
                    color = 'red'  # Целевая вершина
                elif node == curr_node:
                    color = 'yellow'  # Текущая вершина
                elif node in pq_nodes:
                    color = 'blue'  # Открытая вершина
                elif distances[node] != float('infinity'):
                    color = 'gray'  # Закрытая вершина
                else:
                    continue
                ax.plot(node[2], node[1], marker='o', markersize=10, color=color)
                for neighbor, _ in graph[node]:
                    if distances[neighbor] == float('infinity'):
                        continue
                    ax.plot([node[2], neighbor[2]], [node[1], neighbor[1]], color='gray')

        ax.set_aspect('equal')
        ax.axis('off')
        img = buffer_plot_and_get(fig)
        images.append(img)
        ax.clear()

        if curr_node == goal:
            curr_node = goal
            while curr_node is not None:
                path.insert(0, curr_node)
                curr_node = predecessors[curr_node]
            return distances, path, images
        
        if curr_dist > distances[curr_node]:
            continue

        for neighbor, weight in graph[curr_node]:
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = curr_node
                heapq.heappush(priority_queue, (distance, neighbor))

        iteration += 1

    return distances, path, images


def render_dijkstra(graph, start_point, end_point, fig, ax, canvas, fps=60):
    _, _, images = dijkstra(graph, start_point, end_point)
    def animate(i):
        img.set_array(images[i])
        canvas.draw()
        return img,
    img = ax.imshow(images[0], animated=True, cmap='gray')
    ani = animation.FuncAnimation(fig, animate, frames=len(images), interval=100, repeat=True, blit=True)  



def _heuristic(node1, node2):
    if len(node1) == 2:
        x1, y1 = node1
        x2, y2 = node2 
        return np.sqrt((x1-x2)**2 + (y1-y2)**2)
    else:
        res = 0
        for a, b in zip(node1, node2):
            res += abs(a-b)
        return res

@add_router('А*')
def astar(graph, start, goal, background):
    # start = (start[0], start[1])
    path = []
    close_set = set()
    came_from = {}
    gscore = {node: float('infinity') for node in graph}
    gscore[start] = 0
    fscore = {start: _heuristic(start, goal)}
    priority_queue = []
    heapq.heappush(priority_queue, (fscore[start], start))

    images = []
    fig, ax = plt.subplots()
    
    while priority_queue:
        curr_node = heapq.heappop(priority_queue)[1]
        print(curr_node)
        pq_nodes = [x[1] for x in priority_queue]
        if background is not None:
                ax.imshow(background)
        for node in graph.keys():
            
            if len(node) == 2:
                color = 'white'
                if node == goal:
                    color = 'red'  # Целевая вершина
                elif node == curr_node:
                    color = 'yellow'  # Текущая вершина
                elif node in pq_nodes:
                    color = 'blue'  # Открытая вершина
                elif gscore[node] != float('inf'):
                    color = 'gray'  # Закрытая вершина

                ax.plot(node[0], node[1], marker='o', markersize=10, color=color)

                for neighbor, _ in graph[node]:
                    ax.plot([node[0], neighbor[0]], [node[1], neighbor[1]], color='gray')

            else:
                color = 'white'
                if node == goal:
                    color = 'red'  # Целевая вершина
                elif node == curr_node:
                    color = 'yellow'  # Текущая вершина
                elif node in pq_nodes:
                    color = 'blue'  # Открытая вершина
                elif gscore[node] != float('inf'):
                    color = 'gray'  # Закрытая вершина
                else:
                    continue
                ax.plot(node[2], node[1], marker='o', markersize=10, color=color)
                for neighbor, _ in graph[node]:
                    if gscore[neighbor] == float('inf'):
                        continue
                    ax.plot([node[2], neighbor[2]], [node[1], neighbor[1]], color='gray')
            
        ax.set_aspect('equal')
        ax.axis('off')
        img = buffer_plot_and_get(fig)
        images.append(img)
        ax.clear()

        if curr_node == goal:
            while curr_node in came_from:
                path.append(curr_node)
                curr_node = came_from[curr_node]
            return path, images
        
        close_set.add(curr_node)

        for neighbor, weight in graph[curr_node]:
            pre_g_score = gscore[curr_node] + weight
            print(f'node: {neighbor} weight: {weight} pre_g: {pre_g_score} last: {gscore.get(neighbor, 0)}')
            
            if neighbor in close_set and pre_g_score >= gscore.get(neighbor, 0):
                continue
 
            if pre_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in priority_queue]:
                came_from[neighbor] = curr_node
                gscore[neighbor] = pre_g_score
                fscore[neighbor] = pre_g_score + _heuristic(neighbor, goal)
                print(f'added node: {neighbor} weight: {weight} g: {pre_g_score} f: {fscore[neighbor]}')
                heapq.heappush(priority_queue, (fscore[neighbor], neighbor))

    return path, images


def render_astar(graph, start_point, end_point, fig, ax, canvas, fps=60, background=None):
    _, images = astar(graph, start_point, end_point, background)
    def animate(i):
        img.set_array(images[i])
        canvas.draw()
        return img,
    
    img = ax.imshow(images[0], animated=True, cmap='gray')
    ani = animation.FuncAnimation(fig, animate, frames=len(images), interval=100, repeat=True, blit=True)
    # print('check')
    # ani.save('test_astar.gif', writer='imagemagick', fps=fps)

