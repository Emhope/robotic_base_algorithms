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

        for node in graph.keys():
            color = 'white'
            if node == goal:
                color = 'red'  # Целевая вершина
            elif node == curr_node:
                color = 'yellow'  # Текущая вершина
            elif node in [x[1] for x in priority_queue]:
                color = 'blue'  # Открытая вершина
            elif distances[node] != float('infinity'):
                color = 'gray'  # Закрытая вершина
            ax.plot(node[0], node[1], marker='o', markersize=10, color=color)
            for neighbor, _ in graph[node].items():
                ax.plot([node[0], neighbor[0]], [node[1], neighbor[1]], color='gray')

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

        for neighbor, weight in graph[curr_node].items():
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = curr_node
                heapq.heappush(priority_queue, (distance, neighbor))

        iteration += 1

    return distances, path, images

#     distances = {node: float('infinity') for node in graph}
#     distances[start] = 0
#     predecessors = {node: None for node in graph}
#     priority_queue = [(0, start)]

#     images = []
#     fig, ax = plt.subplots()

#     iteration = 0
#     while priority_queue:
#         curr_dist, curr_node = heapq.heappop(priority_queue)
    
#         for node in graph.keys():
#             color = 'white'
#             if node == goal:
#                 color = 'red'  # Целевая вершина
#             elif node == curr_node:
#                 color = 'yellow'  # Текущая вершина
#             elif node in [x[1] for x in priority_queue]:
#                 color = 'blue'  # Открытая вершина
#             elif distances[node] != float('infinity'):
#                 color = 'gray'  # Закрытая вершина
#             if len(node) == 3:
#                 ax.plot(node[2], node[1], marker='o', markersize=10, color=color)
#             else:
#                 ax.plot(node[0], node[1], marker='o', markersize=10, color=color)
                
#             for neighbor, _ in graph[node]:
#                 if len(node) == 3:
#                     ax.plot([node[2], neighbor[2]], [node[1], neighbor[1]], color='gray')
#                 else:
#                     ax.plot([node[0], neighbor[0]], [node[1], neighbor[1]], color='gray')

#             ax.set_aspect('equal')
#             ax.axis('off')
#             img = buffer_plot_and_get(fig)
#             images.append(img)
#             ax.clear()

#         if curr_node == goal:
#             path = []
#             while curr_node is not None:
#                 path.append(curr_node)
#                 curr_node = predecessors[curr_node]
#             path.reverse()

#             return path, distances[goal], images

#         for neighbor, weight in graph[curr_node]:
#             distance = curr_dist + weight
#             if distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 predecessors[neighbor] = curr_node
#                 heapq.heappush(priority_queue, (distance, neighbor))

#         iteration += 1

#     return None, float('infinity'), images





def render_dijkstra(graph, start_point, end_point, fig, ax, canvas, fps=60):
    _, _, images = dijkstra(graph, start_point, end_point)
    def animate(i):
        img.set_array(images[i*fps//10])
        canvas.draw()
        return img,
    img = ax.imshow(images[0], animated=True, cmap='gray')
    ani = animation.FuncAnimation(fig, animate, frames=len(images)//(fps//10), interval=100, repeat=True, blit=True)
    # ani.save('scatter.gif', writer='imagemagick', fps=fps)



def _heuristic(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

@add_router('А*')
def astar(graph, start, goal):
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

        for node in graph.keys():
            color = 'white'
            if node == goal:
                color = 'red'  # Целевая вершина
            elif node == curr_node:
                color = 'yellow'  # Текущая вершина
            elif node in [x[1] for x in priority_queue]:
                color = 'blue'  # Открытая вершина
            elif gscore[node] != float('inf'):
                color = 'gray'  # Закрытая вершина
            ax.plot(node[0], node[1], marker='o', markersize=10, color=color)
            for neighbor, _ in graph[node].items():
                ax.plot([node[0], neighbor[0]], [node[1], neighbor[1]], color='gray')

        if curr_node == goal:
            data = []
            while curr_node in came_from:
                data.append(curr_node)
                curr_node = came_from[curr_node]
            return data, images
        
        close_set.add(curr_node)

        for neighbor, _ in graph[curr_node].items():
            pre_g_score = gscore[curr_node] + _heuristic(curr_node, neighbor)
 
            if neighbor in close_set and pre_g_score >= gscore.get(neighbor, 0):
                continue
 
            if  pre_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in priority_queue]:
                came_from[neighbor] = curr_node
                gscore[neighbor] = pre_g_score
                fscore[neighbor] = pre_g_score + _heuristic(neighbor, goal)
                heapq.heappush(priority_queue, (fscore[neighbor], neighbor))

    return None, images


def render_astar(graph, start_point, end_point, fig, ax, canvas, fps=60):
    _, _, images = astar(graph, start_point, end_point)
    def animate(i):
        img.set_array(images[i*fps//10])
        canvas.draw()
        return img,
    
    img = ax.imshow(images[0], animated=True, cmap='gray')
    ani = animation.FuncAnimation(fig, animate, frames=len(images)//(fps//10), interval=100, repeat=True, blit=True)

