import matplotlib.pyplot as plt
from  customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import map_tools
import config
import cv2
import copy
import voronoi
from utils import minkowski
from graph_plotters import plotters as show_actions
from routers import routers as route_actions
from bug_2 import render_bug2
from vis_graph import vis_vis_graph_layer, create_graph
from config_space import create_config_space
from routers import render_dijkstra, render_astar
from cache import Cache
from ceil_decomp import create_ceil_graph_2d, create_ceil_graph_3d
'''
нач и кон точка, вороной, convert graphs (A* to voronoi/vis graph)
'''

WIDTH = 1200
HEIGHT = 600

set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App:
    def __init__(self) -> None:
        self.root = CTk()
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.title('Path planning')
        self.GUI()
        self.root.mainloop()


    def GUI(self):
        
        self.frame_1 = CTkFrame(master=self.root, width=WIDTH//2, height=HEIGHT//2)
        self.frame_1.pack(fill="both", side="right") # expand=True,

        self.frame_2 = CTkFrame(master=self.root, width=WIDTH//2, height=HEIGHT//2)
        self.frame_2.pack(fill="both", expand=True, side="left") # fill y

        self.label_1 = self.create_label('Введите начальные и целевые координаты:')
        self.label_1.grid(row=0, column=0, columnspan=5, pady=10, padx=10, sticky=W) 

        self.label_4 = self.create_label('Введите шаг дискретизации:')
        self.label_4.grid(row=3, column=5, pady=10, padx=10) 
        self.entry_step = self.create_entry()
        self.entry_step.grid(row=4, column=5, pady=10, padx=10, sticky=W)
        self.entry_step.delete(0, END)
        self.entry_step.insert(0, "50")

        self.label_5 = self.create_label('Введите угол:')
        self.label_5.grid(row=5, column=5, pady=10, padx=10, sticky=W) 
        self.entry_angle = self.create_entry()
        self.entry_angle.grid(row=6, column=5, pady=10, padx=10, sticky=W)

        self.label_x0 = self.create_label('X0:')
        self.label_x0.grid(row=1, column=0, pady=10, padx=10, sticky=W)
        self.label_y0 = self.create_label('Y0:')
        self.label_y0.grid(row=2, column=0, pady=10, padx=10, sticky=W)

        self.entry_x0 = self.create_entry()
        self.entry_x0.grid(row=1, column=1, pady=10, padx=10, sticky=W)
        self.entry_y0 = self.create_entry()
        self.entry_y0.grid(row=2, column=1, pady=10, padx=10, sticky=W)

        self.label_x1 = self.create_label('X1:')
        self.label_x1.grid(row=1, column=2, pady=10, padx=10, sticky=W)
        self.label_y1 = self.create_label('Y1:')
        self.label_y1.grid(row=2, column=2, pady=10, padx=10, sticky=W)

        self.entry_x1 = self.create_entry()
        self.entry_x1.grid(row=1, column=3, pady=10, padx=10, sticky=W)
        self.entry_y1 = self.create_entry()
        self.entry_y1.grid(row=2, column=3, pady=10, padx=10, sticky=W)

        self.label_2 = self.create_label('Выберите графическое представление карты')
        self.label_2.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky=W)

        self.label_3 = self.create_label('Выберите алгоритм')
        self.label_3.grid(row=5, column=0, columnspan=4, pady=10, padx=10, sticky=W)

        self.button_show = self.create_button('Показать', self.button_show_callback)
        self.button_show.grid(row=4, column=4, pady=10, padx=10)

        self.button_create_path = self.create_button('Построить путь', self.button_create_path_callback)
        self.button_create_path.grid(row=6, column=4, pady=10, padx=10)

        self.button_upload_map = self.create_button('Загрузить карту', self.button_upload_map_callback)
        self.button_upload_map.grid(row=1, column=4, pady=10, padx=10)

        self.fig, self.ax = self.create_plot()
        
        self.optionmenu_map = self.create_optionmenu(list(show_actions.keys()),
                                                   self.optionmenu_map_callback
                                                   )
        
        self.optionmenu_map.grid(row=4, column=0, columnspan=4, pady=10, padx=10)

        self.optionmenu_algorithm = self.create_optionmenu(["Алгоритм жука", "А*", "Алгоритм Дейкстры"],
                                                   self.optionmenu_algorithm_callback
                                                   )
        
        self.optionmenu_algorithm.grid(row=6, column=0, columnspan=4, pady=10, padx=10)

    
    def create_entry(self):
        self.entry = CTkEntry(master=self.frame_1,
                              width=64,
                              height=16,
                              )
             
        self.entry.insert(0, 0)  

        return self.entry
    
    def create_optionmenu(self, vals, cmd=None):
        self.optionmenu_var = StringVar(value=vals[0])
        self.optionmenu = CTkOptionMenu(master=self.frame_1,
                                          width=220,
                                          values=vals,
                                          command=cmd,
                                          variable=self.optionmenu_var
                                          )
        
        return self.optionmenu
        
    
    def optionmenu_map_callback(self, choice):
        combs = {
                "Карта": ["Алгоритм жука"],
                "Расширенная карта": [""],
                "Граф видимости": ["А*", "Алгоритм Дейкстры"],
                "Диаграмма Вороного": ["А*", "Алгоритм Дейкстры"],
                "Клеточная декомпозиция": ["А*", "Алгоритм Дейкстры"]
                }
        
        self.optionmenu_var1 = StringVar(value=combs[choice][0])
        self.optionmenu_algorithm.configure(values=combs[choice], variable=self.optionmenu_var1)

    
    def optionmenu_algorithm_callback(self, choice):
        ...
        

    def create_label(self, text=''):
        self.label = CTkLabel(master=self.frame_1,
                              text=text,
                              )
        
        return self.label
    

    def create_button(self, text='', cmd=None):
        self.button = CTkButton(master=self.frame_1,
                                text=text,
                                command=cmd
                                )
        
        return self.button

    def button_show_callback(self):
        action = self.optionmenu_map.get()

        if action == "Карта":
            self.ax.clear()
            self.ax.imshow(~self.map, cmap='gray')
        
        if action == "Граф видимости":
            self.ax.clear()
            if self.vis_graph is None:
                self.vis_graph = create_graph(self.config_space)
            self.curr_graph = copy.deepcopy(self.vis_graph)
            self.angle = self.get_entry_ang_step(self.entry_angle)
            map = self.config_space[self.get_entry_ang_step(self.entry_angle) % 180 // config.angle_step,: ,:]
            vis_vis_graph_layer(self.ax, self.curr_graph, map, self.get_entry_ang_step(self.entry_angle) % 180 // config.angle_step) #vlskjan

        if action == "Диаграмма Вороного":
            self.curr_graph = voronoi.create_voronoi_graph(self.map)
            self.ax.clear()
            self.curr_graph.draw_graph(self.ax)
            masses = voronoi.obs_centers(self.map)
            self.ax.scatter(masses.transpose()[1], masses.transpose()[0])
            self.ax.imshow(~self.map, cmap='gray')

        if action == "Расширенная карта":
            self.ax.clear()
            map = self.config_space[self.get_entry_ang_step(self.entry_angle) % 180 // config.angle_step,: ,:]
            self.ax.imshow(~map, cmap='gray')

        if action == "Клеточная декомпозиция":
            self.ax.clear()
            angle = self.get_entry_ang_step(self.entry_angle) % 180 // config.angle_step
            if self.ceil_graph is None or angle != self.last_ceil_step:
                self.ceil_graph = create_ceil_graph_2d(self.config_space[angle], self.get_entry_ang_step(self.entry_step))
            self.curr_graph = copy.deepcopy(self.ceil_graph)
            self.ax.imshow(~self.config_space[angle].astype(bool), cmap='gray')
            self.curr_graph.draw_graph(self.ax)        
                    
        self.canvas.draw()
        

    def button_create_path_callback(self):
        current_value = self.optionmenu_algorithm.get()
        self.ax.clear()

        if current_value == "Алгоритм жука":
            start_point, end_point = self.get_entry_values()
            render_bug2(self.map, start_point, end_point, self.fig, self.ax, self.canvas)
            
        
        if current_value == "А*":
            start_point, end_point = self.get_entry_values()
            # if self.optionmenu.get() == "Клеточная декомпозиция":
            self.step = self.get_entry_ang_step(self.entry_step)
            self.curr_graph = create_ceil_graph_2d(self.map, self.step)
            self.canvas.draw()
            self.ax.clear()
            start_point = ((start_point[0] // self.step) * self.step + self.step//2, (start_point[1] // self.step)* self.step + self.step//2)
            end_point = ((end_point[0] // self.step) * self.step + self.step//2, (end_point[1] // self.step)* self.step + self.step//2)
            render_astar(self.curr_graph, start_point, end_point, self.fig, self.ax, self.canvas, fps=60)            

        if current_value == "Алгоритм Дейкстры":
            start_point, end_point = self.get_entry_values()            
            self.step = self.get_entry_ang_step(self.entry_step)
            
            if self.optionmenu_map.get() == "Диаграмма Вороного":
                self.curr_graph.add_endpoint(start_point)
                self.curr_graph.add_endpoint(end_point)
                self.curr_graph.draw_graph(self.ax)
                self.canvas.draw()
                self.ax.clear()
                render_dijkstra(self.curr_graph, start_point, end_point, self.fig, self.ax, self.canvas, fps=60)

            elif self.optionmenu_map.get() == "Клеточная декомпозиция":
                #self.curr_graph = create_ceil_graph_2d(self.map, self.step)
                self.canvas.draw()
                self.ax.clear()
                start_point = ((start_point[0] // self.step) * self.step + self.step//2, (start_point[1] // self.step)* self.step + self.step//2)
                end_point = ((end_point[0] // self.step) * self.step + self.step//2, (end_point[1] // self.step)* self.step + self.step//2)
                print('check')
                render_dijkstra(self.curr_graph, start_point, end_point, self.fig, self.ax, self.canvas, fps=60)

        self.canvas.draw()


    def create_plot(self):

        fig = plt.Figure(figsize=(4, 8))
        ax = fig.add_subplot(aspect='equal')
        ax.autoscale_view()        
                
        plt.rc('xtick', labelsize=8)     
        plt.rc('ytick', labelsize=8)            
                
        self.canvas = FigureCanvasTkAgg(fig, self.frame_2)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, self.frame_2)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        return fig, ax
    
    def button_upload_map_callback(self):
        file_path = filedialog.askopenfilename(initialdir='../raw_data/',
                               title='Select a file')
        self.map = map_tools.create_map(file_path)
        self.draw_map()
        self.config_space = create_config_space(self.map)
        self.curr_graph = None
        self.vis_graph = None
        self.ceil_graph = None
        self.last_ceil_step = -1
        

    def draw_map(self):
        ''''
        отрисовка карты
        '''
        self.ax.clear()
        self.ax.imshow(~self.map.astype(bool), cmap='gray')
        self.canvas.draw()


    def get_entry_values(self):
        '''
        получаем координаты начала и конца в виде кортежа (x,y)
        '''
        start = (int(self.entry_x0.get()), int(self.entry_y0.get()))
        end = (int(self.entry_x1.get()), int(self.entry_y1.get()))

        return start, end


    def get_entry_ang_step(self, entry):
        return int(entry.get())

