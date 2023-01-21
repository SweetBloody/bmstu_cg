from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox

from time import time, sleep
import numpy as np
import matplotlib.path as mplPath

from tkinter import Tk, Radiobutton, Canvas, Label, Entry, Button, IntVar
from process import bresenham_int, to_hex_from_rgb

spectrum_var_arr, spectrum_entry_arr, spectrum_widget_arr = [], [], []

can_width = 1080
can_height = 720
line_r = 150
TEMP_SIDE_COLOR_CHECK = (255, 0, 255)
TEMP_SIDE_COLOR = "#ff00ff"
SLEEP_TIME = 0.0001

TASK = "Алгоритм заполнения со списком " \
       "ребер и флагом."

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Лаб. раб. №6')
        self.color_menu = "#ccc"
        self.config(bg="#ccc")
        #self.geometry("1536x800-0+0")
        self.geometry("1536x830-0+0")
        self.resizable(width=False, height=False)
        #self.wm_state('zoomed')
        self.helv11 = tkFont.Font(family='Helvetica', size=11)
        self.helv12 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        self.helv14 = tkFont.Font(family='Helvetica', size=14)
        self.helv14u = tkFont.Font(family='Helvetica', size=14, underline=1)
        self.helv16 = tkFont.Font(family='Helvetica', size=16)

        # self.xy_current = [-400, -350, -300, -250, -200, -150, -100, -50,
        #               0, 50, 100, 150, 200, 250, 300, 350, 400]
        # self.xy_history = [self.xy_current]  # история координат на оси

        self.canvas = Canvas(self, width=can_width, height=can_height, bg="white")
        self.canvas.grid(row=0, column=1, pady=10, padx=10)
        self.coord_center = [can_width // 2, can_height // 2]

        self.image_canvas = PhotoImage(width=can_width, height=can_height)
        self.canvas.create_image((can_width / 2, can_height / 2), image=self.image_canvas, state="normal")

        self.main_frame = Frame(self, bg=self.color_menu, height=150, width=700)
        self.main_frame.grid(row=0, column=0, rowspan=2, padx=30)

        # Кнопка выбора точек
        self.option_coords = IntVar()
        self.option_coords.set(1)

        self.points_choice = Radiobutton(self.main_frame, variable=self.option_coords, value=1, bg=self.color_menu, activebackground=self.color_menu)
        self.points_choice.grid(row=0, column=0, pady=(10, 0))
        self.seed_choice = Radiobutton(self.main_frame, variable=self.option_coords, value=0, bg=self.color_menu, activebackground=self.color_menu)
        self.seed_choice.grid(row=4, column=1, pady=(10, 0))

        # Таблица координат
        self.alg_label = Label(self.main_frame, text="Координаты точек:", font=self.helv14u, bg=self.color_menu)
        self.alg_label.grid(row=0, column=1, columnspan=3, pady=(10, 0))

        self.coords_table = Listbox(self.main_frame, font=self.helv11, width=25, height=9)
        self.coords_table.configure(font=self.helv14)
        self.coords_table.grid(row=1, column=0, columnspan=4, pady=5)

        self.coords_list = [[]]
        self.seed = []

        # Построение точки
        self.x_label = Label(self.main_frame, text="X:", font=self.helv14, bg=self.color_menu)
        self.x_label.grid(row=2, column=0)
        self.x_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.x_entry.grid(row=2, column=1)

        self.y_label = Label(self.main_frame, text="Y:", font=self.helv14, bg=self.color_menu)
        self.y_label.grid(row=2, column=2)
        self.y_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.y_entry.grid(row=2, column=3)

        self.add_btn = Button(self.main_frame, text="Добавить", font=self.helv11, height=2, width=18, command=lambda: self.manual_add_dot())
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Кнопка замыкания фигуры
        self.fin_fig_btn = Button(self.main_frame, text="Замкнуть", font=self.helv11, height=2, width=18, command=lambda: self.make_figure())
        self.fin_fig_btn.grid(row=3, column=2, columnspan=2, pady=10)

        # Затравка
        self.draw_label = Label(self.main_frame, text="Затравка", font=self.helv14u, bg=self.color_menu)
        self.draw_label.grid(row=4, column=1, columnspan=3)

        self.xz_label = Label(self.main_frame, text="X:", font=self.helv14, bg=self.color_menu)
        self.xz_label.grid(row=5, column=0)
        self.xz_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.xz_entry.grid(row=5, column=1)

        self.yz_label = Label(self.main_frame, text="Y:", font=self.helv14, bg=self.color_menu)
        self.yz_label.grid(row=5, column=2)
        self.yz_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.yz_entry.grid(row=5, column=3)

        self.add_btn = Button(self.main_frame, text="Добавить затравку", font=self.helv11, height=2, width=25, command=lambda: self.manual_add_seed())
        self.add_btn.grid(row=6, column=0, columnspan=4, pady=10)

        # Варианты закраски
        self.option_filling = IntVar()
        self.option_filling.set(0)

        self.draw_label = Label(self.main_frame, text="Закраска", font=self.helv14u, bg=self.color_menu)
        self.draw_label.grid(row=7, column=0, columnspan=4)

        self.draw_delay_btn = Radiobutton(self.main_frame, text="С задержкой", font=self.helv11, variable=self.option_filling, value=1, bg=self.color_menu)
        self.draw_delay_btn.grid(row=8, column=0, columnspan=2)

        self.draw_without_delay_btn = Radiobutton(self.main_frame, text="Без задержки", font=self.helv11, variable=self.option_filling, value=0, bg=self.color_menu)
        self.draw_without_delay_btn.grid(row=8, column=2, columnspan=2)

        self.draw_btn = Button(self.main_frame, text="Закрасить", font=self.helv11, height=2, width=25, command=lambda: self.parse_fill())
        self.draw_btn.grid(row=9, column=0, columnspan=4)


        # --------------- ЦВЕТА ---------------
        self.fg_color = (0, 0, 0)
        self.fill_color = (1, 1, 1)
        self.bg_color = (255, 255, 255)
        self.size = 15

        # выбор цвета
        self.color_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=1000)
        self.color_frame.grid(row=10, column=0, columnspan=4, pady=10)

        self.white_line = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)), activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                            command=lambda: self.set_linecolor((255, 255, 255)))
        self.white_line.grid(row=1, column=0)

        self.yellow_line = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)), activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                             command=lambda: self.set_linecolor((255, 255, 0)))
        self.yellow_line.grid(row=1, column=1)

        self.orange_line = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)), activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                             command=lambda: self.set_linecolor((255, 128, 0)))
        self.orange_line.grid(row=1, column=2)

        self.red_line = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)), activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                          command=lambda: self.set_linecolor((255, 0, 0)))
        self.red_line.grid(row=1, column=3)

        self.green_line = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)), activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                            command=lambda: self.set_linecolor((0, 175, 0)))
        self.green_line.grid(row=1, column=4)

        self.blue_line = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)), activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                           command=lambda: self.set_linecolor((0, 0, 255)))
        self.blue_line.grid(row=1, column=5)

        self.purple_line = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)), activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                  command=lambda: self.set_linecolor((135, 0, 200)))
        self.purple_line.grid(row=1, column=6)

        self.black_line = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)), activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                            command=lambda: self.set_linecolor((0, 0, 0)))
        self.black_line.grid(row=1, column=7)

        self.white_fill = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)),
                                 activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                                 command=lambda: self.set_fillcolor((255, 255, 255)))
        self.white_fill.grid(row=3, column=0)

        self.yellow_fill = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)),
                                  activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                                  command=lambda: self.set_fillcolor((255, 255, 0)))
        self.yellow_fill.grid(row=3, column=1)

        self.orange_fill = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)),
                                  activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                                  command=lambda: self.set_fillcolor((255, 128, 0)))
        self.orange_fill.grid(row=3, column=2)

        self.red_fill = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)),
                               activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                               command=lambda: self.set_fillcolor((255, 0, 0)))
        self.red_fill.grid(row=3, column=3)

        self.green_fill = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)),
                                 activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                                 command=lambda: self.set_fillcolor((0, 175, 0)))
        self.green_fill.grid(row=3, column=4)

        self.blue_fill = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)),
                                activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                                command=lambda: self.set_fillcolor((0, 0, 255)))
        self.blue_fill.grid(row=3, column=5)

        self.purple_fill = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)),
                                  activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                  command=lambda: self.set_fillcolor((135, 0, 200)))
        self.purple_fill.grid(row=3, column=6)

        self.black_fill = Button(self.color_frame, bg=to_hex_from_rgb((1, 1, 1)),
                                 activebackground=to_hex_from_rgb((1, 1, 1)), width=2,
                                 command=lambda: self.set_fillcolor((1, 1, 1)))
        self.black_fill.grid(row=3, column=7)

        self.white_bg = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)), activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                          command=lambda: self.set_bgcolor((255, 255, 255)))
        self.white_bg.grid(row=5, column=0)

        self.yellow_bg = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)), activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                           command=lambda: self.set_bgcolor((255, 255, 0)))
        self.yellow_bg.grid(row=5, column=1)

        self.orange_bg = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)), activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                           command=lambda: self.set_bgcolor((255, 128, 0)))
        self.orange_bg.grid(row=5, column=2)

        self.red_bg = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)), activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                        command=lambda: self.set_bgcolor((255, 0, 0)))
        self.red_bg.grid(row=5, column=3)

        self.green_bg = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)), activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                          command=lambda: self.set_bgcolor((0, 175, 0)))
        self.green_bg.grid(row=5, column=4)

        self.blue_bg = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)), activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                         command=lambda: self.set_bgcolor((0, 0, 255)))
        self.blue_bg.grid(row=5, column=5)

        self.purple_bg = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)), activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                command=lambda: self.set_bgcolor((135, 0, 200)))
        self.purple_bg.grid(row=5, column=6)

        self.black_bg = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)), activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                          command=lambda: self.set_bgcolor((0, 0, 0)))
        self.black_bg.grid(row=5, column=7)

        self.color_line_label = Label(self.color_frame, bg=self.color_menu, text='Цвет линии:    Текущий:',
                                      font=self.helv14)
        self.color_line_label.grid(row=0, column=0, columnspan=7)

        self.cur_color_line = Label(self.color_frame, bg=to_hex_from_rgb(self.fg_color), width=2)
        self.cur_color_line.grid(row=0, column=7)

        self.color_fill_label = Label(self.color_frame, bg=self.color_menu, text='Цвет заливки:    Текущий:',
                                      font=self.helv14)
        self.color_fill_label.grid(row=2, column=0, columnspan=7)

        self.cur_color_fill = Label(self.color_frame, bg=to_hex_from_rgb(self.fg_color), width=2)
        self.cur_color_fill.grid(row=2, column=7)

        self.color_bg_label = Label(self.color_frame, bg=self.color_menu, text='Цвет фона: ', font=self.helv14)
        self.color_bg_label.grid(row=4, column=0, columnspan=8)

        # Кнопка отката
        self.undo_btn = Button(self.main_frame, text="Откат", font=self.helv11, height=2, width=18, command=lambda: self.undo())
        self.undo_btn.grid(row=11, column=0, columnspan=2)

        # Кнопка очистки
        self.undo_btn = Button(self.main_frame, text="Очистить", font=self.helv11, height=2, width=18, command=lambda: self.clean_canvas())
        self.undo_btn.grid(row=11, column=2, columnspan=2)

        # Условие задачи
        self.info_btn = Button(self, text="Условие задачи", font=self.helv11, height=2, width=18, command=lambda: messagebox.showinfo("Задание", TASK))
        self.info_btn.grid(row=1, column=1)

        self.canvas.bind('<1>', self.click)
        self.bind("<Configure>", self.del_fill)

    def set_bgcolor(self, color):
        self.bg_color = color
        self.canvas.configure(bg=to_hex_from_rgb(self.bg_color))

    def set_linecolor(self, color):
        self.fg_color = color
        self.cur_color_line.configure(bg=to_hex_from_rgb(self.fg_color))

    def set_fillcolor(self, color):
        self.fill_color = color
        self.cur_color_fill.configure(bg=to_hex_from_rgb(self.fill_color))

    # определение и запись координат точки по клику
    def click(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return
        self.draw_point(event.x, event.y, 1)

    def del_fill(self, event):
        # self.canvas.create_image((can_width / 2, can_height / 2), image=self.image_canvas, state="normal")
        self.canvas.delete('fill')

    # координаты точки из фактических в канвасовские
    def to_canvas(self, dot):
        x = self.coord_center[0] + dot[0]
        y = self.coord_center[1] - dot[1]
        return [x, y]

    # координаты точки из канвасовских в фактические
    def to_coords(self, dot):
        x = (dot[0] - self.coord_center[0])
        y = (-dot[1] + self.coord_center[1])
        return [x, y]

    # нарисовать линию
    def draw_line(self, dots):
        for dot in dots:
            x, y = dot[0:2]
            self.canvas.create_polygon([x, y], [x, y + 1], [x + 1, y + 1], [x + 1, y], fill=dot[2], tag='line')
            self.image_canvas.put(TEMP_SIDE_COLOR, (x, y))

    # отрисовка соединений точек при клике - ребра
    def draw_lines(self, click_dots):
        for figure in click_dots:
            for i in range(len(figure) - 1):
                dots = bresenham_int(figure[i], figure[i + 1], to_hex_from_rgb(self.fg_color))
                self.draw_line(dots)

    # финальная отрисовка ребер
    def draw_sides(self, dots):
        for dot in dots:
            x, y = dot[0:2]
            self.canvas.create_polygon([x, y], [x, y + 1],
                                      [x + 1, y + 1], [x + 1, y],
                                      fill=dot[2], tag='line')

    # добаление точки по координатам (не через канвас)
    def manual_add_dot(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Неверно введены координаты")
            return

        self.draw_point(x, y, 0)

    # добаление точки по координатам (не через канвас)
    def manual_add_seed(self):
        try:
            x = int(self.xz_entry.get())
            y = int(self.yz_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Неверно введены координаты")
            return

        self.draw_point(x, y, 0)

    # проверить, внутри ли фигур затравка
    def seed_inside_figure(self, dot_seed):
        for figure in self.coords_list:
            if len(figure) > 0:
                arr = np.array([[figure[i][0], figure[i][1]] for i in range(len(figure))])
                path = mplPath.Path(arr)

                if path.contains_point(dot_seed):
                    return True
        return False

    # замкнуть фигуру
    def make_figure(self):
        cur_figure = len(self.coords_list)
        cur_dot = len(self.coords_list[cur_figure - 1])

        if cur_dot < 3:
            messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")
            return
        self.draw_point(self.coords_list[cur_figure - 1][0][0], self.coords_list[cur_figure - 1][0][1], 1)
        self.canvas.delete('dot')

        self.coords_list.append(list())

        self.coords_table.insert(END, "-" * 50)

    # закраска
    def parse_fill(self):
        cur_figure = len(self.coords_list) - 1

        if len(self.coords_list[cur_figure]) != 0:
            messagebox.showerror("Ошибка", "Фигура не замкнута")
            return

        delay = False
        if self.option_filling.get() == 1:
            delay = True

        try:
            dot_seed = self.to_canvas(self.seed)
        except:
            messagebox.showerror("Ошибка", "Не выбран затравочный пиксель")

        if not self.seed_inside_figure(dot_seed):
            messagebox.showerror("Ошибка", "Затравочный пиксель находится вне какой-либо фигуры")
            return

        self.fill_with_seed(dot_seed, delay=delay)

    #  отчистака канваса
    def clean_canvas(self):

        self.coords_list.clear()
        self.coords_list.append([])

        self.canvas.delete('line', 'dot')
        self.canvas.configure(bg=to_hex_from_rgb(self.bg_color))
        self.image_canvas.put(to_hex_from_rgb(self.bg_color), to=(0, 0, can_width, can_height))
        self.coords_table.delete(0, END)

    # отрисовка и вставка в листбокс добавленной точки
    def draw_point(self, ev_x, ev_y, click_):

        if click_:
            x, y = ev_x, ev_y
        else:
            x, y = self.to_canvas([ev_x, ev_y])

        x_y = self.to_coords([x, y])

        if self.option_coords.get() == 0:
            self.seed = x_y

            self.xz_entry.delete(0, END)
            self.xz_entry.insert(0, x_y[0])

            self.yz_entry.delete(0, END)
            self.yz_entry.insert(0, x_y[1])

            self.canvas.delete('seed_dot')
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                   outline='lightgreen', fill='lightgreen', activeoutline='pink', width=2,
                                   tag='seed_dot')
            return

        cur_figure = len(self.coords_list) - 1
        self.coords_list[cur_figure].append([int(x), int(y)])

        cur_dot = len(self.coords_list[cur_figure]) - 1

        dot_str = "%d : (%-3.1f; %-3.1f)" % (cur_dot + 1, x_y[0], x_y[1])
        self.coords_table.insert(END, dot_str)

        self.canvas.delete('dot')
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                               outline='grey', fill='pink', activeoutline='lightgreen', width=2, tag='dot')

        color_line = to_hex_from_rgb(self.fg_color)
        if len(self.coords_list[cur_figure]) > 1:
            dots = bresenham_int(self.coords_list[cur_figure][cur_dot - 1], self.coords_list[cur_figure][cur_dot], color_line)
            self.draw_line(dots)

    # построчное заполнение
    def fill_with_seed(self, dot_seed, delay=False):
        color_fill = to_hex_from_rgb(self.fill_color)

        start_time = time()

        stack = list()
        stack.append(dot_seed)

        while stack:
            dot_seed = stack.pop()

            x, y = int(dot_seed[0]), int(dot_seed[1])

            self.image_canvas.put(color_fill, (x, y))
            self.canvas.create_polygon([x, y], [x, y + 1],
                                      [x + 1, y + 1], [x + 1, y],
                                      fill=color_fill, tag='fill')

            tmp_x = x
            tmp_y = y

            # Заполнение текущей строки вправо до ребра или уже закрашенного пикселя
            x = x + 1
            a = self.image_canvas.get(x + 1, y)
            print(a)
            a = self.fill_color
            print(a)
            while self.image_canvas.get(x, y) != TEMP_SIDE_COLOR_CHECK and self.image_canvas.get(x, y) != self.fill_color:
                print(111)
                self.image_canvas.put(color_fill, (x, y))
                self.canvas.create_polygon([x, y], [x, y + 1],
                                          [x + 1, y + 1], [x + 1, y],
                                          fill=color_fill, tag='fill')
                x = x + 1

            x_right = x - 1

            # Заполнение текущей строки влево до ребра или уже закрашенного пикселя
            x = tmp_x - 1

            while self.image_canvas.get(x, y) != TEMP_SIDE_COLOR_CHECK and self.image_canvas.get(x, y) != self.fill_color:
                self.image_canvas.put(color_fill, (x, y))
                self.canvas.create_polygon([x, y], [x, y + 1],
                                          [x + 1, y + 1], [x + 1, y],
                                          fill=color_fill, tag='fill')
                x = x - 1

            x_left = x + 1

            # Сканирование верхней строки
            x = x_left
            y = tmp_y + 1

            while x <= x_right:
                flag = False

                # Поиск, есть ли в строке незакрашенный пиксель
                while (self.image_canvas.get(x, y) != TEMP_SIDE_COLOR_CHECK
                       and self.image_canvas.get(x, y) != self.fill_color
                       and x <= x_right):
                    flag = True

                    x = x + 1

                if flag == True:
                    if (x == x_right
                            and self.image_canvas.get(x, y) != TEMP_SIDE_COLOR_CHECK
                            and self.image_canvas.get(x, y) != self.fill_color):
                        stack.append([x, y])
                    else:
                        stack.append([x - 1, y])

                    flag = False

                x_begin = x

                while ((self.image_canvas.get(x, y) == TEMP_SIDE_COLOR_CHECK
                        or self.image_canvas.get(x, y) == self.fill_color)
                       and x < x_right):
                    x = x + 1

                if x == x_begin:
                    x = x + 1

            # Сканирование нижней строки
            x = x_left

            y = tmp_y - 1

            while x <= x_right:
                flag = False

                # Поиск, есть ли в строке незакрашенный пиксель
                while (self.image_canvas.get(x, y) != TEMP_SIDE_COLOR_CHECK
                       and self.image_canvas.get(x, y) != self.fill_color
                       and x <= x_right):
                    flag = True

                    x = x + 1

                if flag == True:
                    if (x == x_right
                            and self.image_canvas.get(x, y) != TEMP_SIDE_COLOR_CHECK
                            and self.image_canvas.get(x, y) != self.fill_color):
                        stack.append([x, y])
                    else:
                        stack.append([x - 1, y])

                    flag = False

                x_begin = x

                while ((self.image_canvas.get(x, y) == TEMP_SIDE_COLOR_CHECK
                        or self.image_canvas.get(x, y) == self.fill_color)
                       and x < x_right):
                    x = x + 1

                if x == x_begin:
                    x = x + 1

            if delay:
                self.canvas.update()
                sleep(0.001)

        end_time = time()


        new_win = self.time_win(start_time, end_time)
        new_win.mainloop()

    # удаление последней точки
    def del_dot(self):
        try:
            if str(self.coords_table.get(END))[0] == '-':
                self.coords_table.delete(END)

            self.coords_table.delete(END)

        except ValueError:
            messagebox.showerror("Ошибка", "Не выбрана точка")

    # откат
    def undo(self):

        if len(self.coords_list) == 1 and self.coords_list[0] == []:
            messagebox.showerror("Внимание", "Достигнуто исходное состояние")
            return

        self.canvas.delete('line', 'coord')

        d = -1
        if self.coords_list[-1] == []:
            if len(self.coords_list) > 1:
                d = -2
        self.coords_list[d].pop()
        self.del_dot()

        if len(self.coords_list) > 1 and self.coords_list[-2] == []:
            self.coords_list = self.coords_list[:-1]

        self.draw_lines(self.coords_list)

    # окно для вывода замера времени
    def time_win(self, start_time, end_time):
        win = Tk()
        win.title("Время закраски")
        win['bg'] = "grey"
        win.geometry("265x200+630+100")
        win.resizable(False, False)

        time_label = Label(win, text="Время: %-3.2f с" % (end_time - start_time), font=self.helv14,
                           fg='black')
        time_label.place(x=40, y=30, relheight=0.5, relwidth=0.70)

        return win


