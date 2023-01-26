from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from tkinter import Tk, Radiobutton, Canvas, Label, Entry, Button, IntVar


import copy
from itertools import combinations


from process import get_vector, vector_mul, scalar_mul, line_koefs, solve_lines_intersection, is_coord_between,\
    is_dot_between, are_connected_sides, extra_check, get_normal, is_visible, get_lines_parametric_intersec,\
    sutherland_hodgman_algorythm, make_unique, is_dot_in_side, get_sides, remove_odd_sides

can_width = 1080
can_height = 720
line_r = 150
TEMP_SIDE_COLOR_CHECK = (255, 0, 255)
TEMP_SIDE_COLOR = "#ff00ff"
SLEEP_TIME = 0.0001
CLIPPER = 1
FIGURE = 0

TASK = "Реализация (и исследование) " \
       "отсечения отрезка нерегулярным отсекателем " \
       "методом Кируса-Бека"

def to_hex_from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Лаб. раб. №9')
        self.color_menu = "#ccc"
        self.config(bg="#ccc")
        self.geometry("1536x900-0+0")
        self.resizable(width=False, height=False)
        self.helv11 = tkFont.Font(family='Helvetica', size=11)
        self.helv12 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        self.helv14 = tkFont.Font(family='Helvetica', size=14)
        self.helv14u = tkFont.Font(family='Helvetica', size=14, underline=1)
        self.helv16 = tkFont.Font(family='Helvetica', size=16)

        self.figure_coords = [[]]
        self.clipper_coords = []
        self.history = []
        self.lines = []
        self.clippers = []
        self.click_rectangle = 0
        self.click_clipper = 0
        self.start_rectangle = []
        self.start_clipper = []
        self.is_close_clipper = 0
        self.is_close_figure = 0

        self.canvas = Canvas(self, width=can_width, height=can_height, bg="white")
        self.canvas.grid(row=0, column=1, pady=10, padx=10)
        self.coord_center = [can_width // 2, can_height // 2]

        self.image_canvas = PhotoImage(width=can_width, height=can_height)
        self.canvas.create_image((can_width / 2, can_height / 2), image=self.image_canvas, state="normal")

        self.main_frame = Frame(self, bg=self.color_menu, height=150, width=700)
        self.main_frame.grid(row=0, column=0, rowspan=2, padx=30)

        # Кнопка выбора точек
        self.option_line = IntVar()
        self.option_line.set(0)

        self.fig_choice = Radiobutton(self.main_frame, variable=self.option_line, value=0, bg=self.color_menu, activebackground=self.color_menu)
        self.fig_choice.grid(row=0, column=0, pady=(10, 0))
        self.clipper_choice = Radiobutton(self.main_frame, variable=self.option_line, value=1, bg=self.color_menu, activebackground=self.color_menu)
        self.clipper_choice.grid(row=2, column=0, pady=(10, 0))

        # Построение многоугольников
        self.fig_label = Label(self.main_frame, text="Координаты многоугольников", font=self.helv14, bg=self.color_menu)
        self.fig_label.grid(row=0, column=0, columnspan=4)

        self.fig_table = Listbox(self.main_frame, font=self.helv11, width=25, height=7)
        self.fig_table.configure(font=self.helv14)
        self.fig_table.grid(row=1, column=0, columnspan=4, pady=5)

        # Построение отсекателя
        self.clipper_label = Label(self.main_frame, text="Построение отсекателя", font=self.helv14, bg=self.color_menu)
        self.clipper_label.grid(row=2, column=0, columnspan=4)

        self.clipper_table = Listbox(self.main_frame, font=self.helv11, width=25, height=7)
        self.clipper_table.configure(font=self.helv14)
        self.clipper_table.grid(row=3, column=0, columnspan=4, pady=5)

        self.x_label = Label(self.main_frame, text="X:", font=self.helv14, bg=self.color_menu)
        self.x_label.grid(row=4, column=0)
        self.x_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.x_entry.grid(row=4, column=1)

        self.y_label = Label(self.main_frame, text="Y:", font=self.helv14, bg=self.color_menu)
        self.y_label.grid(row=4, column=2)
        self.y_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.y_entry.grid(row=4, column=3)

        self.add_btn = Button(self.main_frame, text="Добавить", font=self.helv11, height=2, width=18, command=lambda: self.draw_clipper())
        self.add_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.fin_fig_btn = Button(self.main_frame, text="Замкнуть", font=self.helv11, height=2, width=18, command=lambda: self.make_figure())
        self.fin_fig_btn.grid(row=5, column=2, columnspan=2, pady=10)


        # --------------- ЦВЕТА ---------------
        self.fig_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.clipper_color = (0, 0, 255)
        self.res_color = (255, 0, 0)
        self.size = 15

        # Выбор цвета
        self.color_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=1000)
        self.color_frame.grid(row=6, column=0, columnspan=4)

        # Выбор цвета отрезка
        self.white_otr = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)), activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                                command=lambda: self.set_figcolor((255, 255, 255)))
        self.white_otr.grid(row=1, column=0)

        self.yellow_otr = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)), activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                                 command=lambda: self.set_figcolor((255, 255, 0)))
        self.yellow_otr.grid(row=1, column=1)

        self.orange_otr = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)), activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                                 command=lambda: self.set_figcolor((255, 128, 0)))
        self.orange_otr.grid(row=1, column=2)

        self.red_otr = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)), activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                              command=lambda: self.set_figcolor((255, 0, 0)))
        self.red_otr.grid(row=1, column=3)

        self.green_otr = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)), activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                                command=lambda: self.set_figcolor((0, 175, 0)))
        self.green_otr.grid(row=1, column=4)

        self.blue_otr = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)), activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                               command=lambda: self.set_figcolor((0, 0, 255)))
        self.blue_otr.grid(row=1, column=5)

        self.purple_otr = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)), activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                 command=lambda: self.set_figcolor((135, 0, 200)))
        self.purple_otr.grid(row=1, column=6)

        self.black_otr = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)), activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                                command=lambda: self.set_figcolor((0, 0, 0)))
        self.black_otr.grid(row=1, column=7)


        # Выбор цвета отсекателя
        self.white_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)),
                                activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                                command=lambda: self.set_clippercolor((255, 255, 255)))
        self.white_res.grid(row=3, column=0)

        self.yellow_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)),
                                 activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                                 command=lambda: self.set_clippercolor((255, 255, 0)))
        self.yellow_res.grid(row=3, column=1)

        self.orange_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)),
                                 activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                                 command=lambda: self.set_clippercolor((255, 128, 0)))
        self.orange_res.grid(row=3, column=2)

        self.red_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)),
                              activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                              command=lambda: self.set_clippercolor((255, 0, 0)))
        self.red_res.grid(row=3, column=3)

        self.green_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)),
                                activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                                command=lambda: self.set_clippercolor((0, 175, 0)))
        self.green_res.grid(row=3, column=4)

        self.blue_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)),
                               activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                               command=lambda: self.set_clippercolor((0, 0, 255)))
        self.blue_res.grid(row=3, column=5)

        self.purple_res = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)),
                                 activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                 command=lambda: self.set_clippercolor((135, 0, 200)))
        self.purple_res.grid(row=3, column=6)

        self.black_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)),
                                activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                                command=lambda: self.set_clippercolor((0, 0, 0)))
        self.black_res.grid(row=3, column=7)


        # Выбор цвета результата
        self.white_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)),
                                activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                                command=lambda: self.set_rescolor((255, 255, 255)))
        self.white_res.grid(row=5, column=0)

        self.yellow_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)),
                                 activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                                 command=lambda: self.set_rescolor((255, 255, 0)))
        self.yellow_res.grid(row=5, column=1)

        self.orange_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)),
                                 activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                                 command=lambda: self.set_rescolor((255, 128, 0)))
        self.orange_res.grid(row=5, column=2)

        self.red_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)),
                              activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                              command=lambda: self.set_rescolor((255, 0, 0)))
        self.red_res.grid(row=5, column=3)

        self.green_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)),
                                activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                                command=lambda: self.set_rescolor((0, 175, 0)))
        self.green_res.grid(row=5, column=4)

        self.blue_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)),
                               activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                               command=lambda: self.set_rescolor((0, 0, 255)))
        self.blue_res.grid(row=5, column=5)

        self.purple_res = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)),
                                 activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                 command=lambda: self.set_rescolor((135, 0, 200)))
        self.purple_res.grid(row=5, column=6)

        self.black_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)),
                                activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                                command=lambda: self.set_rescolor((0, 0, 0)))
        self.black_res.grid(row=5, column=7)


        # Выбор цвета фона
        self.white_bg = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)), activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                          command=lambda: self.set_bgcolor((255, 255, 255)))
        self.white_bg.grid(row=7, column=0)

        self.yellow_bg = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)), activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                           command=lambda: self.set_bgcolor((255, 255, 0)))
        self.yellow_bg.grid(row=7, column=1)

        self.orange_bg = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)), activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                           command=lambda: self.set_bgcolor((255, 128, 0)))
        self.orange_bg.grid(row=7, column=2)

        self.red_bg = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)), activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                        command=lambda: self.set_bgcolor((255, 0, 0)))
        self.red_bg.grid(row=7, column=3)

        self.green_bg = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)), activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                          command=lambda: self.set_bgcolor((0, 175, 0)))
        self.green_bg.grid(row=7, column=4)

        self.blue_bg = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)), activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                         command=lambda: self.set_bgcolor((0, 0, 255)))
        self.blue_bg.grid(row=7, column=5)

        self.purple_bg = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)), activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                command=lambda: self.set_bgcolor((135, 0, 200)))
        self.purple_bg.grid(row=7, column=6)

        self.black_bg = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)), activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                          command=lambda: self.set_bgcolor((0, 0, 0)))
        self.black_bg.grid(row=7, column=7)

        # Надписи
            # отрезок
        self.color_otr_label = Label(self.color_frame, bg=self.color_menu, text='Цвет отрезка:    Текущий:',
                                     font=self.helv14)
        self.color_otr_label.grid(row=0, column=0, columnspan=7, pady=(5, 0))

        self.cur_color_otr = Label(self.color_frame, bg=to_hex_from_rgb(self.fig_color), width=2)
        self.cur_color_otr.grid(row=0, column=7, pady=(5, 0))

            # отсекатель
        self.color_rect_label = Label(self.color_frame, bg=self.color_menu, text='Цвет отсекателя:    Текущий:',
                                      font=self.helv14)
        self.color_rect_label.grid(row=2, column=0, columnspan=7, pady=(5, 0))

        self.cur_color_rect = Label(self.color_frame, bg=to_hex_from_rgb(self.clipper_color), width=2)
        self.cur_color_rect.grid(row=2, column=7, pady=(5, 0))

            # результат
        self.color_res_label = Label(self.color_frame, bg=self.color_menu, text='Цвет результата:    Текущий:',
                                      font=self.helv14)
        self.color_res_label.grid(row=4, column=0, columnspan=7, pady=(5, 0))

        self.cur_color_res = Label(self.color_frame, bg=to_hex_from_rgb(self.res_color), width=2)
        self.cur_color_res.grid(row=4, column=7, pady=(5, 0))

            # фон
        self.color_bg_label = Label(self.color_frame, bg=self.color_menu, text='Цвет фона: ', font=self.helv14)
        self.color_bg_label.grid(row=6, column=0, columnspan=8, pady=(5, 0))


        # Кнопка отсечения
        self.cut_btn = Button(self.main_frame, text="Отсечь", font=self.helv11, height=2, width=18, command=lambda: self.cut_area())
        self.cut_btn.grid(row=7, column=0, columnspan=4, pady=10)


        # Кнопка отката
        self.undo_btn = Button(self.main_frame, text="Откат", font=self.helv11, height=2, width=18, command=lambda: self.undo())
        self.undo_btn.grid(row=8, column=0, columnspan=2)

        # Кнопка очистки
        self.undo_btn = Button(self.main_frame, text="Очистить", font=self.helv11, height=2, width=18, command=lambda: self.clean_canvas())
        self.undo_btn.grid(row=8, column=2, columnspan=2)

        # Условие задачи
        self.info_btn = Button(self, text="Условие задачи", font=self.helv11, height=2, width=18, command=lambda: messagebox.showinfo("Задание", TASK))
        self.info_btn.grid(row=1, column=1)

        self.canvas.bind('<1>', self.click)
        self.bind("<Motion>", self.motion)

    def set_bgcolor(self, color):
        self.bg_color = color
        self.canvas.configure(bg=to_hex_from_rgb(self.bg_color))

    def set_figcolor(self, color):
        self.fig_color = color
        self.cur_color_otr.configure(bg=to_hex_from_rgb(self.fig_color))

    def set_clippercolor(self, color):
        self.clipper_color = color
        self.cur_color_rect.configure(bg=to_hex_from_rgb(self.clipper_color))

    def set_rescolor(self, color):
        self.res_color = color
        self.cur_color_res.configure(bg=to_hex_from_rgb(self.res_color))

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

    # добаление точки по координатам (не через канвас)
    def add_dot(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Неверно введены координаты")
            return

        self.draw_point(x, y, 0)

    # рисовать отсекатель
    def draw_line_clipper(self, new_dot):
        color = to_hex_from_rgb(self.clipper_color)

        if len(self.clipper_coords) > 0:
            previous_dot = self.clipper_coords[-1]
            self.canvas.create_line(previous_dot, new_dot, fill=color, tag='clipper')
            self.canvas.delete('clipper_dot')

        self.clipper_coords.append(new_dot)
        cur = copy.deepcopy(self.clipper_coords)
        self.history.append([cur, 'rectangle'])

    def draw_line_rectangle(self, new_dot):
        color = to_hex_from_rgb(self.fig_color)

        if len(self.figure_coords[-1]) > 0:
            previous_dot = self.figure_coords[-1][-1]
            self.canvas.create_line(previous_dot, new_dot, fill=color, tag='figure')

        self.figure_coords[-1].append(new_dot)
        cur = copy.deepcopy(self.figure_coords)
        self.history.append([cur, 'figure'])

    # замкнуть фигуру
    def make_figure(self):
        if self.option_line.get() == FIGURE:
            if len(self.figure_coords[-1]) < 3:
                messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")
                return

            self.is_close_figure = 1
            self.draw_point(self.figure_coords[-1][0][0], self.figure_coords[-1][0][1], 1)
            if self.click_clipper == 0:
                self.click_clipper = 1

        elif self.option_line.get() == CLIPPER:
            if len(self.clipper_coords) < 3:
                messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")
                return

            self.draw_point(self.clipper_coords[0][0], self.clipper_coords[0][1], 1)
            self.is_close_clipper = 1
            if self.click_clipper == 0:
                self.click_clipper = 1
            self.start_clipper = []

    # отрисовка и вставка в листбокс добавленной точки
    def draw_point(self, ev_x, ev_y, click_):
        if click_:
            x, y = ev_x, ev_y
        else:
            x, y = self.to_canvas([ev_x, ev_y])

        x_y = self.to_coords([x, y])

        if self.option_line.get() == 0:
            if self.click_rectangle == 0:
                self.click_rectangle = 1
            self.start_rectangle = [x, y]
            dot_str = "  (%-d; %-d)" % (x_y[0], x_y[1])
            self.fig_table.insert(END, dot_str)
            self.draw_line_rectangle([x, y])
            self.canvas.delete('figure_dot', 'lineHelper')
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                   outline='pink', fill='pink', activeoutline='lightgreen', width=2, tag='figure_dot')
            if self.is_close_figure:
                self.click_rectangle = 0
                self.start_rectangle = []
                self.fig_table.insert(END, 50 * '-')
                self.figure_coords.append([])
                self.is_close_figure = 0

        elif self.option_line.get() == 1:
            self.start_clipper = [x, y]
            print(self.start_clipper)
            if self.is_close_clipper:
                for _ in range(len(self.clipper_coords)):
                    self.clipper_table.delete(END)
                self.click_clipper = 0
                self.clipper_coords = []
                self.is_close_clipper = 0
                self.canvas.delete('clipper_dot', 'clipper')

            dot_str = "  (%-d; %-d)" % (x_y[0], x_y[1])
            self.clipper_table.insert(END, dot_str)
            self.canvas.delete('lineHelper')
            self.draw_line_clipper([x, y])

            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                   outline='pink', fill='pink', activeoutline='lightgreen', width=2, tag='clipper_dot')

    def check_polygon(self):  # через проход по всем точкам, поворот которых должен быть все время в одну сторону
        if len(self.clipper_coords) < 3:
            return False

        sign = 0

        if vector_mul(get_vector(self.clipper_coords[1], self.clipper_coords[2]),
                      get_vector(self.clipper_coords[0], self.clipper_coords[1])) > 0:
            sign = 1
        else:
            sign = -1

        for i in range(3, len(self.clipper_coords)):
            if sign * vector_mul(get_vector(self.clipper_coords[i - 1], self.clipper_coords[i]),
                                 get_vector(self.clipper_coords[i - 2], self.clipper_coords[i - 1])) < 0:
                return False

        check = extra_check(self.clipper_coords)

        if check:
            return False

        if sign < 0:
            self.clipper_coords.reverse()

        return True

    def cut_area(self):
        if not self.is_close_clipper:
            messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
            return

        if self.is_close_figure:
            messagebox.showinfo("Ошибка", "Отекаемый многоугольник не замкнут")
            return

        if len(self.clipper_coords) < 3:
            messagebox.showinfo("Ошибка", "Не задан отсекатель")
            return

        if not self.check_polygon():
            messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
            return

        self.canvas.delete('result')
        for figure in self.figure_coords:

            if len(figure) == 0:
                continue

            if extra_check(figure):
                messagebox.showinfo("Ошибка", "Неверно задан отсекаемый многоугольник")
                return

            result = copy.deepcopy(figure)

            for cur_dot_ind in range(-1, len(self.clipper_coords) - 1):
                line = [self.clipper_coords[cur_dot_ind], self.clipper_coords[cur_dot_ind + 1]]

                position_dot = self.clipper_coords[cur_dot_ind + 1]

                result = sutherland_hodgman_algorythm(line, position_dot, result)

                if len(result) <= 2:
                    return

            self.draw_result_figure(result)

    def draw_result_figure(self, figure_dots):
        fixed_figure = remove_odd_sides(figure_dots)

        res_color = to_hex_from_rgb(self.res_color)

        result_figure = [[]]
        for line in fixed_figure:
            self.canvas.create_line(line[0], line[1], fill=res_color, tag='result')
            result_figure[0].append(line)
        result_figure.append('result')
        self.history.append(result_figure)

    # предварительный просмотр линии
    def motion(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return

        if self.option_line.get() == 0:
            if self.click_rectangle == 1:
                self.canvas.delete("lineHelper")
                self.canvas.create_line(self.start_rectangle[0], self.start_rectangle[1], event.x, event.y,
                                       fill='grey', width=1, dash=(7, 9), tag='lineHelper')
        if self.option_line.get() == 1:
            if self.click_clipper == 1:
                self.canvas.delete("lineHelper")
                print(self.start_clipper)
                self.canvas.create_line(self.start_clipper[0], self.start_clipper[1], event.x, event.y,
                                       fill='grey', width=1, dash=(7, 9), tag='lineHelper')

    # определение и запись координат точки по клику
    def click(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return

        self.draw_point(event.x, event.y, 1)

    # определить крайний отсекатель для ундо
    def find_rectangle(self, history):
        for i in range(len(history) - 1, -1, -1):
            if history[i][1] == 'rectangle':
                return history[i][0]

        return []

    # заполнить листбокс при ундо
    def fill_listbox(self):
        self.clipper_table.delete('0', 'end')
        self.fig_table.delete('0', 'end')

        for dot in self.clipper_coords:
            dot = self.to_coords(dot)
            dot_str = "  (%-d; %-d)" % (dot[0], dot[1])
            self.clipper_table.insert(END, dot_str)

        for figure in self.figure_coords:
            for dot in figure:
                dot = self.to_coords(dot)
                dot_str = "  (%-d; %-d)" % (dot[0], dot[1])
                self.fig_table.insert(END, dot_str)
            if len(figure) != 0:
                self.fig_table.insert(END, 50 * "-")

    def draw_figure(self):
        color_line = to_hex_from_rgb(self.fig_color)

        for figures in self.history:
            if figures[1] == 'figure':
                for figure in figures[0]:
                    for i in range(len(figure) - 1):
                        if len(figure) > 1:
                            self.canvas.create_line(figure[i], figure[i + 1], fill=color_line, tag='figure')

    # для ундо
    def draw_all(self):
        self.draw_figure()

        self.clipper_coords = self.find_rectangle(self.history)
        if len(self.clipper_coords) != 0:
            self.check_is_close()
            self.draw_clipper()

        self.fill_listbox()

    def check_is_close(self):
        if self.clipper_coords[0][0] == self.clipper_coords[-1][0] and self.clipper_coords[0][1] == self.clipper_coords[-1][1]:
            self.is_close_clipper = 1
        else:
            self.is_close_clipper = 0

    def draw_clipper(self):
        color_clipper = to_hex_from_rgb(self.clipper_color)

        for i in range(len(self.clipper_coords) - 1):
            self.canvas.create_line(self.clipper_coords[i], self.clipper_coords[i + 1], fill=color_clipper, tag='clipper')

    # откат
    def undo(self):
        if len(self.history) == 0:
            messagebox.showerror("Внимание", "Достигнуто исходное состояние")
            return

        self.canvas.delete('figure', 'dot1', 'dot2', 'clipper', 'clipper_dot', 'result', 'figure_dot')

        deleted = self.history.pop()
        if deleted[1] == 'figure':
            if len(self.figure_coords[-1]) == 0:
                self.figure_coords = self.figure_coords[:-1]
            self.figure_coords[-1].pop()

        self.draw_all()

    #  отчистака канваса
    def clean_canvas(self):
        self.history = []
        self.lines = []
        self.clipper_coords = []
        self.figure_coords = [[]]

        self.fig_table.delete('0', 'end')
        self.fig_table.delete('0', 'end')

        self.clipper_table.delete('0', 'end')
        self.clipper_table.delete('0', 'end')

        self.canvas.delete('figure', 'dot1', 'dot2', 'clipper', 'clipper_dot', 'figure_dot', 'result', 'lineHelper')
        self.canvas_color = ((255, 255, 255), "#ffffff")
        self.canvas.configure(bg=to_hex_from_rgb(self.bg_color))

