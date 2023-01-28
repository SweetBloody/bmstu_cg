from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from tkinter import Tk, Radiobutton, Canvas, Label, Entry, Button, IntVar

from math import sqrt, acos, degrees, pi, sin, cos, radians, floor, fabs
from numpy import arange

can_width = 1080
can_height = 720

CV_COLOR = "#ffffff"  # f3e6ff" #"#cce6ff"
MAIN_TEXT_COLOR = "lightgrey"  # "lightblue" a94dff
TEXT_COLOR = "#ce99ff"

TEMP_SIDE_COLOR_CHECK = (255, 0, 255)  # purple
TEMP_SIDE_COLOR = "#ff00ff"

BOX_COLOR = "lightgrey"

COLOR_LINE = "#000002"  # (0, 0, 0) # black
COLOR_LINE_CHECK = (0, 0, 2)

FILL_COLOR = "#ff6e41"

# Define

X_DOT = 0
Y_DOT = 1
Z_DOT = 2

FROM = 0
TO = 1
STEP = 2

FROM_SPIN_BOX = -1000.0
TO_SPIN_BOX = 1000.0
STEP_SPIN_BOX = 0.1

DEFAULT_SCALE = 45
DEFAULT_ANGLE = 5

TASK = "Реализация (и исследование) " \
       "алгоритма плавающего горизонта"


def to_hex_from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Лаб. раб. №10')
        self.color_menu = "#ccc"
        self.config(bg="#ccc")
        self.geometry("1610x800-0+0")
        self.resizable(width=False, height=False)
        self.helv11 = tkFont.Font(family='Helvetica', size=11)
        self.helv12 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        self.helv14 = tkFont.Font(family='Helvetica', size=14)
        self.helv14u = tkFont.Font(family='Helvetica', size=14, underline=1)
        self.helv16 = tkFont.Font(family='Helvetica', size=16)

        self.trans_matrix = []

        self.canvas = Canvas(self, width=can_width, height=can_height, bg="white")
        self.canvas.grid(row=0, column=1, pady=10, padx=10)
        self.coord_center = [can_width // 2, can_height // 2]

        self.main_frame = Frame(self, bg=self.color_menu, height=150, width=700)
        self.main_frame.grid(row=0, column=0, rowspan=2, padx=30)

        # Выбор функции
        self.func_label = Label(self.main_frame, text="Выбор функций", font=self.helv14u, bg=self.color_menu)
        self.func_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        self.option_function = IntVar()
        self.option_function.set(1)

        self.graph1_option = Radiobutton(self.main_frame, text="sin(x) * sin(z)", font=self.helv14, variable=self.option_function, value=1, bg=self.color_menu, activebackground=self.color_menu)
        self.graph1_option.grid(row=1, column=0, columnspan=2)

        self.graph2_option = Radiobutton(self.main_frame, text="sin(cos(x)) * sin(z)", font=self.helv14, variable=self.option_function, value=2, bg=self.color_menu, activebackground=self.color_menu)
        self.graph2_option.grid(row=1, column=2, columnspan=2)

        self.graph3_option = Radiobutton(self.main_frame, text="cos(x) * z / 3", font=self.helv14, variable=self.option_function, value=3, bg=self.color_menu, activebackground=self.color_menu)
        self.graph3_option.grid(row=2, column=0, columnspan=2, pady=(0, 30))

        self.graph4_option = Radiobutton(self.main_frame, text="cos(x) * cos(sin(z))", font=self.helv14, variable=self.option_function, value=4, bg=self.color_menu, activebackground=self.color_menu)
        self.graph4_option.grid(row=2, column=2, columnspan=2, pady=(0, 30))

        # Установка пределов
        self.limit_label = Label(self.main_frame, text="Установка пределов", font=self.helv14u, bg=self.color_menu)
        self.limit_label.grid(row=3, column=0, columnspan=4, pady=(0, 10))

        self.limit_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=700)
        self.limit_frame.grid(row=4, column=0, columnspan=4, pady=(0, 30))

        # ось X
        self.ox_axis_label = Label(self.limit_frame, text="Ось OX", font=self.helv14, bg=self.color_menu)
        self.ox_axis_label.grid(row=0, column=0, padx=(0, 10))

        self.x_from_label = Label(self.limit_frame, text="от: ", font=self.helv14, bg=self.color_menu)
        self.x_from_label.grid(row=0, column=1, padx=(0, 10))

        self.x_from_entry = Spinbox(self.limit_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                               increment=STEP_SPIN_BOX, width=4)
        self.x_from_entry.grid(row=0, column=2, padx=(0, 10))

        self.x_to_label = Label(self.limit_frame, text="до: ", font=self.helv14, bg=self.color_menu)
        self.x_to_label.grid(row=0, column=3, padx=(0, 10))

        self.x_to_entry = Spinbox(self.limit_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                               increment=STEP_SPIN_BOX, width=4)
        self.x_to_entry.grid(row=0, column=4, padx=(0, 10))

        self.x_step_label = Label(self.limit_frame, text="шаг: ", font=self.helv14, bg=self.color_menu)
        self.x_step_label.grid(row=0, column=5, padx=(0, 10))

        self.x_step_entry = Spinbox(self.limit_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                                  increment=STEP_SPIN_BOX, width=4)
        self.x_step_entry.grid(row=0, column=6)

        self.x_from_entry.delete(0, END)
        self.x_from_entry.insert(0, "-12")

        self.x_to_entry.delete(0, END)
        self.x_to_entry.insert(0, "12")

        self.x_step_entry.delete(0, END)
        self.x_step_entry.insert(0, "0.1")

        # ось Z
        self.oz_axis_label = Label(self.limit_frame, text="Ось OZ", font=self.helv14, bg=self.color_menu)
        self.oz_axis_label.grid(row=1, column=0, padx=(0, 10))

        self.z_from_label = Label(self.limit_frame, text="от: ", font=self.helv14, bg=self.color_menu)
        self.z_from_label.grid(row=1, column=1, padx=(0, 10))

        self.z_from_entry = Spinbox(self.limit_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                                    increment=STEP_SPIN_BOX, width=4)
        self.z_from_entry.grid(row=1, column=2, padx=(0, 10))

        self.z_to_label = Label(self.limit_frame, text="до: ", font=self.helv14, bg=self.color_menu)
        self.z_to_label.grid(row=1, column=3, padx=(0, 10))

        self.z_to_entry = Spinbox(self.limit_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                                  increment=STEP_SPIN_BOX, width=4)
        self.z_to_entry.grid(row=1, column=4, padx=(0, 10))

        self.z_step_label = Label(self.limit_frame, text="шаг: ", font=self.helv14, bg=self.color_menu)
        self.z_step_label.grid(row=1, column=5, padx=(0, 10))

        self.z_step_entry = Spinbox(self.limit_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                                  increment=STEP_SPIN_BOX, width=4)
        self.z_step_entry.grid(row=1, column=6)

        self.z_from_entry.delete(0, END)
        self.z_from_entry.insert(0, "-12")

        self.z_to_entry.delete(0, END)
        self.z_to_entry.insert(0, "12")

        self.z_step_entry.delete(0, END)
        self.z_step_entry.insert(0, "0.1")

        # Поворот
        self.rotate_label = Label(self.main_frame, text="Поворот", font=self.helv14u, bg=self.color_menu)
        self.rotate_label.grid(row=5, column=0, columnspan=4, pady=(0, 10))

        # по X
        self.x_rotate_label = Label(self.main_frame, text="OX:", font=self.helv14, bg=self.color_menu)
        self.x_rotate_label.grid(row=6, column=0, pady=(0, 5))

        self.x_rotate_entry = Spinbox(self.main_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                                  increment=STEP_SPIN_BOX, width=6)
        self.x_rotate_entry.grid(row=6, column=1, pady=(0, 5))

        self.x_rotate_btn = Button(self.main_frame, text="Повернуть", font=self.helv11, height=2, width=18,
                                   command=lambda: self.rotate_x())
        self.x_rotate_btn.grid(row=6, column=2, columnspan=2, pady=(0, 5))

        self.x_rotate_entry.delete(0, END)
        self.x_rotate_entry.insert(0, str(DEFAULT_ANGLE))

        # по Y
        self.y_rotate_label = Label(self.main_frame, text="OY:", font=self.helv14, bg=self.color_menu)
        self.y_rotate_label.grid(row=7, column=0, pady=(0, 5))

        self.y_rotate_entry = Spinbox(self.main_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                                      increment=STEP_SPIN_BOX, width=6)
        self.y_rotate_entry.grid(row=7, column=1, pady=(0, 5))

        self.y_rotate_btn = Button(self.main_frame, text="Повернуть", font=self.helv11, height=2, width=18,
                                   command=lambda: self.rotate_y())
        self.y_rotate_btn.grid(row=7, column=2, columnspan=2, pady=(0, 5))

        self.y_rotate_entry.delete(0, END)
        self.y_rotate_entry.insert(0, str(DEFAULT_ANGLE))

        # по Z
        self.z_rotate_label = Label(self.main_frame, text="OZ:", font=self.helv14, bg=self.color_menu)
        self.z_rotate_label.grid(row=8, column=0, pady=(0, 30))

        self.z_rotate_entry = Spinbox(self.main_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                                      increment=STEP_SPIN_BOX, width=6)
        self.z_rotate_entry.grid(row=8, column=1, pady=(0, 30))

        self.z_rotate_btn = Button(self.main_frame, text="Повернуть", font=self.helv11, height=2, width=18,
                                   command=lambda: self.rotate_z())
        self.z_rotate_btn.grid(row=8, column=2, columnspan=2, pady=(0, 30))

        self.z_rotate_entry.delete(0, END)
        self.z_rotate_entry.insert(0, str(DEFAULT_ANGLE))


        # Масштабирование
        self.scale_label = Label(self.main_frame, text="Масштабирование", font=self.helv14u, bg=self.color_menu)
        self.scale_label.grid(row=9, column=0, columnspan=4, pady=(0, 10))

        self.scale_label = Label(self.main_frame, text="Коэффициент:", font=self.helv14, bg=self.color_menu)
        self.scale_label.grid(row=10, column=0, columnspan=2)

        self.scale_entry = Spinbox(self.main_frame, font=self.helv14, from_=FROM_SPIN_BOX, to=TO_SPIN_BOX,
                                      increment=STEP_SPIN_BOX, width=6)
        self.scale_entry.grid(row=10, column=2, columnspan=2)

        self.scale_btn = Button(self.main_frame, text="Масштабировать", font=self.helv11, height=2, width=18,
                                   command=lambda: self.scale_graph())
        self.scale_btn.grid(row=11, column=0, columnspan=4, pady=(5, 20))

        self.scale_entry.delete(0, END)
        self.scale_entry.insert(0, str(DEFAULT_SCALE))

        # --------------- ЦВЕТА ---------------
        self.func_color = (0, 0, 0)
        self.size = 15

        # Выбор цвета
        self.color_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=1000)
        self.color_frame.grid(row=12, column=0, columnspan=4, pady=(0, 30))

        # Выбор цвета отрезка
        self.white_func = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)),
                                 activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                                 command=lambda: self.set_func_color((255, 255, 255)))
        self.white_func.grid(row=1, column=0)

        self.yellow_func = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)),
                                  activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                                  command=lambda: self.set_func_color((255, 255, 0)))
        self.yellow_func.grid(row=1, column=1)

        self.orange_func = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)),
                                  activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                                  command=lambda: self.set_func_color((255, 128, 0)))
        self.orange_func.grid(row=1, column=2)

        self.red_func = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)),
                               activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                               command=lambda: self.set_func_color((255, 0, 0)))
        self.red_func.grid(row=1, column=3)

        self.green_func = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)),
                                 activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                                 command=lambda: self.set_func_color((0, 175, 0)))
        self.green_func.grid(row=1, column=4)

        self.blue_func = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)),
                                activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                                command=lambda: self.set_func_color((0, 0, 255)))
        self.blue_func.grid(row=1, column=5)

        self.purple_func = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)),
                                  activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                  command=lambda: self.set_func_color((135, 0, 200)))
        self.purple_func.grid(row=1, column=6)

        self.black_func = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)),
                                 activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                                 command=lambda: self.set_func_color((0, 0, 0)))
        self.black_func.grid(row=1, column=7)

        self.color_func_label = Label(self.color_frame, bg=self.color_menu, text='Цвет графика:    Текущий:',
                                     font=self.helv14)
        self.color_func_label.grid(row=0, column=0, columnspan=7, pady=(5, 0))

        self.cur_color_func = Label(self.color_frame, bg=to_hex_from_rgb(self.func_color), width=2)
        self.cur_color_func.grid(row=0, column=7, pady=(5, 0))

        # Кнопка отрисовки результата
        self.undo_btn = Button(self.main_frame, text="Отрисовать результат", font=self.helv11, height=2, width=18, command=lambda: self.build_graph(new_graph=True))
        self.undo_btn.grid(row=13, column=0, columnspan=2)

        # Кнопка очистки
        self.clean_btn = Button(self.main_frame, text="Очистить", font=self.helv11, height=2, width=18, command=lambda: self.reboot_prog())
        self.clean_btn.grid(row=13, column=2, columnspan=2)

        # Условие задачи
        self.info_btn = Button(self, text="Условие задачи", font=self.helv11, height=2, width=18, command=lambda: messagebox.showinfo("Задание", TASK))
        self.info_btn.grid(row=1, column=1)

        # self.canvas.bind('<1>', self.click)
        # self.bind("<Motion>", self.motion)

    def set_func_color(self, color):
        self.func_color = color
        self.cur_color_func.configure(bg=to_hex_from_rgb(self.func_color))

    def set_trans_matrix(self):
        self.trans_matrix.clear()

        for i in range(4):
            tmp_arr = []

            for j in range(4):
                tmp_arr.append(int(i == j))

            self.trans_matrix.append(tmp_arr)

    def check_option(self, option):
        messagebox.showinfo("Выбран", "Выбрана опция %d" % (option))

    def clear_canvas(self):
        self.canvas.delete("all")

    def get_fill_check_color(self, collor_fill):
        return (int(collor_fill[1:3], 16), int(collor_fill[3:5], 16), int(collor_fill[5:7], 16))

    def reboot_prog(self):
        self.canvas.delete("all")

    def parse_funcs(self, func_num):
        func = lambda x, z: sin(x) * cos(z)

        if (func_num == 1):
            func = lambda x, z: sin(x) * sin(z)
        elif (func_num == 2):
            func = lambda x, z: sin(cos(x)) * sin(z)
        elif (func_num == 3):
            func = lambda x, z: cos(x) * z / 3
        elif (func_num == 4):
            func = lambda x, z: cos(x) * cos(sin(z))

        return func

    def read_limits(self):
        try:
            x_from = float(self.x_from_entry.get())
            x_to = float(self.x_to_entry.get())
            x_step = float(self.x_step_entry.get())

            x_limits = [x_from, x_to, x_step]

            z_from = float(self.z_from_entry.get())
            z_to = float(self.z_to_entry.get())
            z_step = float(self.z_step_entry.get())

            z_limits = [z_from, z_to, z_step]

            return x_limits, z_limits
        except:
            return -1, -1

    def rotate_matrix(self, matrix):
        res_matrix = [[0 for i in range(4)] for j in range(4)]

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    res_matrix[i][j] += self.trans_matrix[i][k] * matrix[k][j]

        self.trans_matrix = res_matrix

    def rotate_x(self):
        try:
            angle = float(self.x_rotate_entry.get()) / 180 * pi
        except:
            messagebox.showerror("Ошибка", "Угол - число")
            return

        if (len(self.trans_matrix) == 0):
            messagebox.showerror("Ошибка", "График не задан")
            return

        rotating_matrix = [[1, 0, 0, 0],
                           [0, cos(angle), sin(angle), 0],
                           [0, -sin(angle), cos(angle), 0],
                           [0, 0, 0, 1]]

        self.rotate_matrix(rotating_matrix)

        self.build_graph()

    def rotate_y(self):
        try:
            angle = float(self.y_rotate_entry.get()) / 180 * pi
        except:
            messagebox.showerror("Ошибка", "Угол - число")
            return

        if (len(self.trans_matrix) == 0):
            messagebox.showerror("Ошибка", "График не задан")
            return

        rotating_matrix = [[cos(angle), 0, -sin(angle), 0],
                           [0, 1, 0, 0],
                           [sin(angle), 0, cos(angle), 0],
                           [0, 0, 0, 1]]

        self.rotate_matrix(rotating_matrix)

        self.build_graph()

    def rotate_z(self):
        try:
            angle = float(self.z_rotate_entry.get()) / 180 * pi
        except:
            messagebox.showerror("Ошибка", "Угол - число")
            return

        if (len(self.trans_matrix) == 0):
            messagebox.showerror("Ошибка", "График не задан")
            return

        rotating_matrix = [[cos(angle), sin(angle), 0, 0],
                           [-sin(angle), cos(angle), 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]]

        self.rotate_matrix(rotating_matrix)

        self.build_graph()

    def scale_graph(self):
        try:
            scale_param = float(self.scale_entry.get())
        except:
            messagebox.showerror("Ошибка", "Коэффициент масштабирования должен быть числом")
            return

        if (len(self.trans_matrix) == 0):
            messagebox.showerror("Ошибка", "График не задан")
            return

        self.build_graph(scale_param=scale_param)

    def trans_dot(self, dot, scale_param):
        dot.append(1)

        res_dot = [0, 0, 0, 0]

        for i in range(4):
            for j in range(4):
                res_dot[i] += dot[j] * self.trans_matrix[j][i]

        for i in range(3):
            res_dot[i] *= scale_param

        res_dot[0] += can_width // 2
        res_dot[1] += can_height // 2

        return res_dot[:3]

    def is_visible(self, dot):
        return (0 <= dot[X_DOT] <= can_width) and \
               (0 <= dot[Y_DOT] <= can_height)

    def draw_pixel(self, x, y):
        color = to_hex_from_rgb(self.func_color)

        self.canvas.create_line(x, y, x + 1, y + 1, fill=color)

    def draw_dot(self, x, y, high_horizon, low_horizon):
        if (not self.is_visible([x, y])):
            return False

        if (y > high_horizon[x]):
            high_horizon[x] = y
            self.draw_pixel(x, y)
        elif (y < low_horizon[x]):
            low_horizon[x] = y
            self.draw_pixel(x, y)

        return True

    def draw_horizon_part(self, dot1, dot2, high_horizon, low_horizon):
        if (dot1[X_DOT] > dot2[X_DOT]):
            dot1, dot2 = dot2, dot1

        dx = dot2[X_DOT] - dot1[X_DOT]
        dy = dot2[Y_DOT] - dot1[Y_DOT]

        if (dx > dy):
            l = dx
        else:
            l = dy

        dx /= l
        dy /= l

        x = dot1[X_DOT]
        y = dot1[Y_DOT]

        for _ in range(int(l) + 1):
            if (not self.draw_dot(round(x), y, high_horizon, low_horizon)):
                return

            x += dx
            y += dy

    def draw_horizon(self, function, high_horizon, low_horizon, limits, z, scale_param):
        f = lambda x: function(x, z)

        prev = None

        for x in arange(limits[FROM], limits[TO] + limits[STEP], limits[STEP]):
            cur = self.trans_dot([x, f(x), z], scale_param)

            if (prev):
                self.draw_horizon_part(prev, cur, high_horizon, low_horizon)

            prev = cur

    def draw_horizon_limits(self, f, x_limits, z_limits, scale_param):
        color = to_hex_from_rgb(self.func_color)

        for z in arange(z_limits[FROM], z_limits[TO] + z_limits[STEP], z_limits[STEP]):
            dot1 = self.trans_dot([x_limits[FROM], f(x_limits[FROM], z), z], scale_param)
            dot2 = self.trans_dot([x_limits[FROM], f(x_limits[FROM], z + x_limits[STEP]), z + x_limits[STEP]], scale_param)

            self.canvas.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT], dot2[Y_DOT], fill=color)

            dot1 = self.trans_dot([x_limits[TO], f(x_limits[TO], z), z], scale_param)
            dot2 = self.trans_dot([x_limits[TO], f(x_limits[TO], z + x_limits[STEP]), z + x_limits[STEP]], scale_param)

            self.canvas.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT], dot2[Y_DOT], fill=color)

    def build_graph(self, new_graph=False, scale_param=DEFAULT_SCALE):
        self.reboot_prog()

        if (new_graph):
            self.set_trans_matrix()

        f = self.parse_funcs(self.option_function.get())

        x_limits, z_limits = self.read_limits()

        print(x_limits, z_limits)

        high_horizon = [0 for i in range(can_width + 1)]
        low_horizon = [can_height for i in range(can_width + 1)]

        #  Горизонт
        for z in arange(z_limits[FROM], z_limits[TO] + z_limits[STEP], z_limits[STEP]):
            self.draw_horizon(f, high_horizon, low_horizon, x_limits, z, scale_param)

        # Границы горизонта
        self.draw_horizon_limits(f, x_limits, z_limits, scale_param)

