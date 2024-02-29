import voronoi
import numpy as np
import config
import ceil_decomp


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
    ax.imshow(map)
    return None, map

@add_plotter('Граф видимости')
def vis_g_show(ax, map):
    ...


@add_plotter('Клеточная декомпозиция')
def ceil_show(ax, map):
    m = ceil_decomp.create_ceil_graph_3d