import voronoi
import numpy as np
import config
<<<<<<< HEAD
from config_space import create_config_space
import copy
=======
import ceil_decomp

>>>>>>> 3e9003fde60427d3445aedfcdc99958f4200744e

plotters = dict()


def add_plotter(name):
    def adder(f):
        plotters[name] = f
        return f
    return adder


def mass_overlay(map, ax):
    masses = voronoi.obs_centers(map, config.voronoi_obs_thresh)
    ax.scatter(*masses.transpose()[::-1])

@add_plotter('Диаграмма Вороного')
def voronoi_show(ax, map):
    ax.clear()
    g = voronoi.create_voronoi_graph(map, config.voronoi_obs_thresh)
    g.draw_graph(ax)
    mass_overlay(map, ax)
    return g, None

@add_plotter('Карта')
def map_show(ax, map):
    ax.clear()
<<<<<<< HEAD
    return None, map

@add_plotter('Граф видимости')
def visibiliy_graph_show(ax, g):
    ...

@add_plotter('Расширенная карта')
def minkowski_show(ax, map):
    ax.clear()
    config_space = create_config_space(copy.copy(map))
    map = config_space[int(0),: ,:]
    return None, map

@add_plotter('Клеточная декомпозиция')
def cell_decomp_show(ax, g):
    ...
=======
    ax.imshow(map)
    return None, map

@add_plotter('Граф видимости')
def vis_g_show(ax, map):
    ...


@add_plotter('Клеточная декомпозиция')
def ceil_show(ax, map):
    m = ceil_decomp.create_ceil_graph_3d
>>>>>>> 3e9003fde60427d3445aedfcdc99958f4200744e
