import matplotlib.pyplot as plt
from  customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import map_tools
import config

WIDTH = 1080
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
        self.frame_1.pack(fill="both", expand=True, side="right")

        self.frame_2 = CTkFrame(master=self.root, width=WIDTH//2, height=HEIGHT//2)
        self.frame_2.pack(fill="both", expand=True, side="left") # fill y

        self.label_1 = self.create_label('Введите начальные и целевые координаты:')
        self.label_1.grid(row=0, column=0, columnspan=5, pady=10, padx=10, sticky=W) 
       
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

        self.label_2 = self.create_label('Выберите что-то')
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
        
        self.optionmenu_map = self.create_optionmenu(["Карта", "Граф видимости", "Расширенная карта", "Диаграмма Вороного", "Клеточная декомпозиция"],
                                                   self.optionmenu_map_callback
                                                   )
        
        self.optionmenu_map.grid(row=4, column=0, columnspan=4, pady=10, padx=10)

        self.optionmenu_algorithm = self.create_optionmenu(["Алгоритм жука", "Реактивный алгоритм жука", "А*", "Алгоритм Дейкстры", "Че-то воронового"],
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
                "Карта": ["Алгоритм жука", "Реактивный алгоритм жука"],
                "Расширенная карта": ["Алгоритм жука", "Реактивный алгоритм жука"],
                "Граф видимости": ["А*", "Алгоритм Дейкстры"],
                "Диаграмма Вороного": ["Че-то воронового"],
                "Клеточная декомпозиция": ["А*", "Алгоритм Дейкстры"]
                }
        
        self.optionmenu_var1 = StringVar(value=combs[choice][0])
        self.optionmenu_algorithm.configure(values=combs[choice], variable=self.optionmenu_var1)

    
    def optionmenu_algorithm_callback(self):
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
        ...

    def button_create_path_callback(self):
        ...
    

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
        map = map_tools.create_map(file_path)
        
        self.ax.clear()
        self.ax.imshow(~map.astype(bool), cmap='gray')
        self.canvas.draw()
