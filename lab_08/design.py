from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from tkinter import Tk, Radiobutton, Canvas, Label, Entry, Button, IntVar

from time import time, sleep
import numpy as np
import matplotlib.path as mplPath
import copy
from itertools import combinations


from process import get_vector, vector_mul, scalar_mul, line_koefs, solve_lines_intersection, is_coord_between,\
    is_dot_between, are_connected_sides, get_normal, find_rectangle, cross_otrs

can_width = 1080
can_height = 720
line_r = 150
TEMP_SIDE_COLOR_CHECK = (255, 0, 255)
TEMP_SIDE_COLOR = "#ff00ff"
SLEEP_TIME = 0.0001

TASK = "Реализация (и исследование) " \
       "отсечения отрезка нерегулярным отсекателем " \
       "методом Кируса-Бека"

def to_hex_from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Лаб. раб. №8')
        self.color_menu = "#ccc"
        self.config(bg="#ccc")
        self.geometry("1536x830-0+0")
        self.resizable(width=False, height=False)
        self.helv11 = tkFont.Font(family='Helvetica', size=11)
        self.helv12 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        self.helv14 = tkFont.Font(family='Helvetica', size=14)
        self.helv14u = tkFont.Font(family='Helvetica', size=14, underline=1)
        self.helv16 = tkFont.Font(family='Helvetica', size=16)

        self.lines = []
        self.history = []
        self.clipper_coords = []
        self.line_coords = []
        self.clippers = []
        self.is_close_figure = 0
        self.click_flag = 0

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

        self.otr_choice = Radiobutton(self.main_frame, variable=self.option_line, value=0, bg=self.color_menu, activebackground=self.color_menu)
        self.otr_choice.grid(row=0, column=0, pady=(10, 0))
        self.rect_choice = Radiobutton(self.main_frame, variable=self.option_line, value=1, bg=self.color_menu, activebackground=self.color_menu)
        self.rect_choice.grid(row=4, column=0, pady=(10, 0))

        # Построение отрезка
        self.otr_label = Label(self.main_frame, text="Построение отрезка", font=self.helv14, bg=self.color_menu)
        self.otr_label.grid(row=0, column=0, columnspan=4)

        self.x1_otr_label = Label(self.main_frame, text="X1:", font=self.helv14, bg=self.color_menu)
        self.x1_otr_label.grid(row=1, column=0)
        self.x1_otr_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.x1_otr_entry.grid(row=1, column=1)

        self.y1_otr_label = Label(self.main_frame, text="Y1:", font=self.helv14, bg=self.color_menu)
        self.y1_otr_label.grid(row=2, column=0)
        self.y1_otr_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.y1_otr_entry.grid(row=2, column=1)

        self.x2_otr_label = Label(self.main_frame, text="X2:", font=self.helv14, bg=self.color_menu)
        self.x2_otr_label.grid(row=1, column=2)
        self.x2_otr_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.x2_otr_entry.grid(row=1, column=3)

        self.y2_otr_label = Label(self.main_frame, text="Y2:", font=self.helv14, bg=self.color_menu)
        self.y2_otr_label.grid(row=2, column=2)
        self.y2_otr_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.y2_otr_entry.grid(row=2, column=3)

        self.add_otr_btn = Button(self.main_frame, text="Добавить", font=self.helv11, height=2, width=18, command=lambda: self.draw_line())
        self.add_otr_btn.grid(row=3, column=0, columnspan=4, pady=10)

        # Построение отсекателя
        self.rect_label = Label(self.main_frame, text="Построение отсекателя", font=self.helv14, bg=self.color_menu)
        self.rect_label.grid(row=4, column=0, columnspan=4)

        self.coords_table = Listbox(self.main_frame, font=self.helv11, width=25, height=7)
        self.coords_table.configure(font=self.helv14)
        self.coords_table.grid(row=5, column=0, columnspan=4, pady=5)

        self.x1_rect_label = Label(self.main_frame, text="X:", font=self.helv14, bg=self.color_menu)
        self.x1_rect_label.grid(row=6, column=0)
        self.x1_rect_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.x1_rect_entry.grid(row=6, column=1)

        self.y1_rect_label = Label(self.main_frame, text="Y:", font=self.helv14, bg=self.color_menu)
        self.y1_rect_label.grid(row=6, column=2)
        self.y1_rect_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.y1_rect_entry.grid(row=6, column=3)

        self.add_rect_btn = Button(self.main_frame, text="Добавить", font=self.helv11, height=2, width=18, command=lambda: self.draw_clipper())
        self.add_rect_btn.grid(row=7, column=0, columnspan=2, pady=10)

        self.fin_fig_btn = Button(self.main_frame, text="Замкнуть", font=self.helv11, height=2, width=18, command=lambda: self.make_figure())
        self.fin_fig_btn.grid(row=7, column=2, columnspan=2, pady=10)


        # --------------- ЦВЕТА ---------------
        self.otr_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.rect_color = (0, 0, 255)
        self.res_color = (255, 0, 0)
        self.size = 15

        # Выбор цвета
        self.color_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=1000)
        self.color_frame.grid(row=8, column=0, columnspan=4)

        # Выбор цвета отрезка
        self.white_otr = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)), activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                                command=lambda: self.set_otrcolor((255, 255, 255)))
        self.white_otr.grid(row=1, column=0)

        self.yellow_otr = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)), activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                                 command=lambda: self.set_otrcolor((255, 255, 0)))
        self.yellow_otr.grid(row=1, column=1)

        self.orange_otr = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)), activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                                 command=lambda: self.set_otrcolor((255, 128, 0)))
        self.orange_otr.grid(row=1, column=2)

        self.red_otr = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)), activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                              command=lambda: self.set_otrcolor((255, 0, 0)))
        self.red_otr.grid(row=1, column=3)

        self.green_otr = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)), activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                                command=lambda: self.set_otrcolor((0, 175, 0)))
        self.green_otr.grid(row=1, column=4)

        self.blue_otr = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)), activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                               command=lambda: self.set_otrcolor((0, 0, 255)))
        self.blue_otr.grid(row=1, column=5)

        self.purple_otr = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)), activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                 command=lambda: self.set_otrcolor((135, 0, 200)))
        self.purple_otr.grid(row=1, column=6)

        self.black_otr = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)), activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                                command=lambda: self.set_otrcolor((0, 0, 0)))
        self.black_otr.grid(row=1, column=7)


        # Выбор цвета отсекателя
        self.white_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 255)),
                                activebackground=to_hex_from_rgb((255, 255, 255)), width=2,
                                command=lambda: self.set_rectcolor((255, 255, 255)))
        self.white_res.grid(row=3, column=0)

        self.yellow_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 255, 0)),
                                 activebackground=to_hex_from_rgb((255, 255, 0)), width=2,
                                 command=lambda: self.set_rectcolor((255, 255, 0)))
        self.yellow_res.grid(row=3, column=1)

        self.orange_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 128, 0)),
                                 activebackground=to_hex_from_rgb((255, 128, 0)), width=2,
                                 command=lambda: self.set_rectcolor((255, 128, 0)))
        self.orange_res.grid(row=3, column=2)

        self.red_res = Button(self.color_frame, bg=to_hex_from_rgb((255, 0, 0)),
                              activebackground=to_hex_from_rgb((255, 0, 0)), width=2,
                              command=lambda: self.set_rectcolor((255, 0, 0)))
        self.red_res.grid(row=3, column=3)

        self.green_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 175, 0)),
                                activebackground=to_hex_from_rgb((0, 175, 0)), width=2,
                                command=lambda: self.set_rectcolor((0, 175, 0)))
        self.green_res.grid(row=3, column=4)

        self.blue_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 255)),
                               activebackground=to_hex_from_rgb((0, 0, 255)), width=2,
                               command=lambda: self.set_rectcolor((0, 0, 255)))
        self.blue_res.grid(row=3, column=5)

        self.purple_res = Button(self.color_frame, bg=to_hex_from_rgb((135, 0, 200)),
                                 activebackground=to_hex_from_rgb((135, 0, 200)), width=2,
                                 command=lambda: self.set_rectcolor((135, 0, 200)))
        self.purple_res.grid(row=3, column=6)

        self.black_res = Button(self.color_frame, bg=to_hex_from_rgb((0, 0, 0)),
                                activebackground=to_hex_from_rgb((0, 0, 0)), width=2,
                                command=lambda: self.set_rectcolor((0, 0, 0)))
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

        self.cur_color_otr = Label(self.color_frame, bg=to_hex_from_rgb(self.otr_color), width=2)
        self.cur_color_otr.grid(row=0, column=7, pady=(5, 0))

            # отсекатель
        self.color_rect_label = Label(self.color_frame, bg=self.color_menu, text='Цвет отсекателя:    Текущий:',
                                      font=self.helv14)
        self.color_rect_label.grid(row=2, column=0, columnspan=7, pady=(5, 0))

        self.cur_color_rect = Label(self.color_frame, bg=to_hex_from_rgb(self.rect_color), width=2)
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
        self.cut_btn.grid(row=9, column=0, columnspan=4, pady=10)


        # Кнопка отката
        self.undo_btn = Button(self.main_frame, text="Откат", font=self.helv11, height=2, width=18, command=lambda: self.undo())
        self.undo_btn.grid(row=10, column=0, columnspan=2)

        # Кнопка очистки
        self.undo_btn = Button(self.main_frame, text="Очистить", font=self.helv11, height=2, width=18, command=lambda: self.clean_canvas())
        self.undo_btn.grid(row=10, column=2, columnspan=2)

        # Условие задачи
        self.info_btn = Button(self, text="Условие задачи", font=self.helv11, height=2, width=18, command=lambda: messagebox.showinfo("Задание", TASK))
        self.info_btn.grid(row=1, column=1)

        self.canvas.bind('<1>', self.click)
        self.bind("<Motion>", self.motion)


    def set_bgcolor(self, color):
        self.bg_color = color
        self.canvas.configure(bg=to_hex_from_rgb(self.bg_color))

    def set_otrcolor(self, color):
        self.otr_color = color
        self.cur_color_otr.configure(bg=to_hex_from_rgb(self.otr_color))

    def set_rectcolor(self, color):
        self.rect_color = color
        self.cur_color_rect.configure(bg=to_hex_from_rgb(self.rect_color))

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

    def draw_clipper(self):
        color_clipper = to_hex_from_rgb(self.rect_color)

        for i in range(len(self.clipper_coords) - 1):
            self.canvas.create_line(self.clipper_coords[i], self.clipper_coords[i + 1], fill=color_clipper, tag='clipper')

    def check_is_close(self):

        if self.clipper_coords[0][0] == self.clipper_coords[-1][0] and self.clipper_coords[0][1] == self.clipper_coords[-1][1]:
            self.is_close_figure = 1
        else:
            self.is_close_figure = 0

    #  отчистака канваса
    def clean_canvas(self):
        self.history = []
        self.lines = []
        self.clipper_coords = []

        self.coords_table.delete('0', 'end')

        self.canvas.delete('line', 'dot1', 'dot2', 'clipper', 'clipper_dot', 'result')
        self.bg_color = (255, 255, 255)
        self.canvas.configure(bg=to_hex_from_rgb(self.bg_color))

    # нарисовать отрезок
    def draw_line(self):
        color = to_hex_from_rgb(self.otr_color)
        try:
            dot1 = self.to_canvas([int(self.x1_otr_entry.get()), int(self.y1_otr_entry.get())])
            dot2 = self.to_canvas([int(self.x2_otr_entry.get()), int(self.y2_otr_entry.get())])
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные координаты отрезка")
            return

        self.lines.append([dot1, dot2])
        self.history.append([[dot1, dot2], 'line'])

        self.canvas.delete('lineHelper')
        self.canvas.create_line(dot1, dot2, fill=color, tag='line')

    # рисовать отсекатель
    def draw_cutter_line(self, new_dot):
        color = to_hex_from_rgb(self.rect_color)

        if len(self.clipper_coords) > 0:
            previous_dot = self.clipper_coords[-1]
            self.canvas.create_line(previous_dot, new_dot, fill=color, tag='clipper')
            self.canvas.delete('clipper_dot')

        self.clipper_coords.append(new_dot)
        cur = copy.deepcopy(self.clipper_coords)
        self.history.append([cur, 'rectangle'])

    # добаление точки по координатам (не через канвас)
    def add_clipper_dot(self):
        try:
            x = int(self.x1_rect_entry.get())
            y = int(self.y1_rect_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Неверно введены координаты")
            return

        self.draw_point(x, y, 0)

    # замкнуть фигуру
    def make_figure(self):
        if len(self.clipper_coords) < 3:
            messagebox.showerror("Ошибка", "Недостаточно точек, чтобы замкнуть фигуру")
            return

        self.draw_point(self.clipper_coords[0][0], self.clipper_coords[0][1], 1)
        self.is_close_figure = 1
        self.click_flag = 0
        self.canvas.delete("lineHelper")

    # определение и запись координат точки по клику
    def click(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return

        if self.option_line.get() == 0:
            if self.click_flag == 0:
                self.click_flag = 1
            elif self.click_flag == 1:
                self.click_flag = 2
            elif self.click_flag == 2:
                self.click_flag = 1
        else:
            self.click_flag = 1

        self.draw_point(event.x, event.y, 1)

    # заполнить листбокс при ундо
    def fill_listbox(self):
        self.coords_table.delete('0', 'end')

        for dot in self.clipper_coords:
            dot = self.to_coords(dot)
            dot_str = "  (%-d; %-d)" % (dot[0], dot[1])
            self.coords_table.insert(END, dot_str)

    def draw_all(self):
        color_line = to_hex_from_rgb(self.otr_color)
        for figure in self.history:
            if figure[1] == 'line':
                self.canvas.create_line(figure[0], fill=color_line, tag='line')

        self.clipper_coords = find_rectangle(self.history)
        if len(self.clipper_coords) != 0:
            self.check_is_close()
            self.draw_clipper()

        self.fill_listbox()

    # отсечь
    def cut_area(self):

        if not self.is_close_figure:
            messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
            return

        if len(self.clipper_coords) < 3:
            messagebox.showinfo("Ошибка", "Не задан отсекатель")
            return

        if cross_otrs(self.clipper_coords):
            messagebox.showinfo("Ошибка", "Отсекатель не должен быть самопересекающимся")
            return

        if not self.check_polygon():
            messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
            return



        self.find_start_dot()
        dot = self.clipper_coords.pop()

        # print(clipper_coords, dot)

        for line in self.lines:
            self.cyrus_beck_algorithm(line, len(self.clipper_coords))

        self.clipper_coords.append(dot)

    # предварительный просмотр линии
    def motion(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return

        if self.option_line.get() == 0:
            if self.click_flag == 1:
                self.canvas.delete("lineHelper")
                self.canvas.create_line(self.start_line[0], self.start_line[1], event.x, event.y,
                                       fill='grey', width=1, tag='lineHelper')

        if self.option_line.get() == 1:
            if self.click_flag == 1 :
                self.canvas.delete("lineHelper")
                self.canvas.create_line(self.start_line[0], self.start_line[1], event.x, event.y,
                                       fill='grey', width=1, tag='lineHelper')

    # откат
    def undo(self):
        if len(self.history) == 0:
            messagebox.showerror("Внимание", "Достигнуто исходное состояние")
            return

        self.canvas.delete('line', 'dot1', 'dot2', 'clipper', 'clipper_dot', 'result')

        deleted = self.history.pop()
        if deleted[1] == 'line':
            self.lines.pop()

        self.draw_all()

    def find_start_dot(self):
        y_max = self.clipper_coords[0][1]
        dot_index = 0

        for i in range(len(self.clipper_coords)):
            if self.clipper_coords[i][1] > y_max:
                y_max = self.clipper_coords[i][1]
                dot_index = i

        self.clipper_coords.pop()

        for _ in range(dot_index):
            self.clipper_coords.append(self.clipper_coords.pop(0))

        self.clipper_coords.append(self.clipper_coords[0])

        if self.clipper_coords[-2][0] > self.clipper_coords[1][0]:
            self.clipper_coords.reverse()

    # отрисовка и вставка в листбокс добавленной точки
    def draw_point(self, ev_x, ev_y, click_):
        if click_:
            x, y = ev_x, ev_y
        else:
            x, y = self.to_canvas([ev_x, ev_y])

        x_y = self.to_coords([x, y])

        if self.click_flag == 1:
            self.start_line = [x, y]

        if self.option_line.get() == 0:
            if self.click_flag == 1:
                self.start_line = [x, y]

                self.x1_otr_entry.delete(0, END)
                self.y1_otr_entry.delete(0, END)
                self.x1_otr_entry.insert(0, "%d" % x_y[0])
                self.y1_otr_entry.insert(0, "%d" % x_y[1])
                self.canvas.delete('dot1')
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                       outline='lightgreen', fill='lightgreen', activeoutline='blue', width=2, tag='dot1')

            if self.click_flag == 2:
                self.x2_otr_entry.delete(0, END)
                self.y2_otr_entry.delete(0, END)
                self.x2_otr_entry.insert(0, "%d" % x_y[0])
                self.y2_otr_entry.insert(0, "%d" % x_y[1])
                self.canvas.delete('dot2')
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                       outline='lightgreen', fill='lightgreen', activeoutline='blue', width=2, tag='dot2')
                self.draw_line()

        elif self.option_line.get() == 1:
            if self.is_close_figure:
                for _ in range(len(self.clipper_coords)):
                    self.coords_table.delete(END)
                self.clipper_coords = []
                self.is_close_figure = 0
                self.canvas.delete('clipper_dot', 'clipper')

            dot_str = "  (%-d; %-d)" % (x_y[0], x_y[1])
            self.coords_table.insert(END, dot_str)
            self.draw_cutter_line([x, y])
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                   outline='blue', fill='blue', activeoutline='lightgreen', width=2, tag='clipper_dot')

    def extra_check(self):  # чтобы не было пересечений

        cutter_lines = []

        for i in range(len(self.clipper_coords) - 1):
            cutter_lines.append([self.clipper_coords[i], self.clipper_coords[i + 1]])  # разбиваю отсекатель на линии

        combs_lines = list(combinations(cutter_lines, 2))  # все возможные комбинации сторон

        for i in range(len(combs_lines)):
            line1 = combs_lines[i][0]
            line2 = combs_lines[i][1]

            if are_connected_sides(line1, line2):
                continue

            a1, b1, c1 = line_koefs(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
            a2, b2, c2 = line_koefs(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

            dot_intersection = solve_lines_intersection(a1, b1, c1, a2, b2, c2)

            if (is_dot_between(line1[0], line1[1], dot_intersection)) \
                    and (is_dot_between(line2[0], line2[1], dot_intersection)):
                return True

        return False

    def check_polygon(self):
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

        check = self.extra_check()

        if check:
            return False

        return True

    def cyrus_beck_algorithm(self, line, count):
        dot1 = line[0]
        dot2 = line[1]

        d = [dot2[0] - dot1[0], dot2[1] - dot1[1]]  # директриса

        t_bottom = 0
        t_top = 1

        for i in range(-2, count - 2):
            normal = get_normal(self.clipper_coords[i], self.clipper_coords[i + 1], self.clipper_coords[i + 2])

            w = [dot1[0] - self.clipper_coords[i][0], dot1[1] - self.clipper_coords[i][1]]

            d_scalar = scalar_mul(d, normal)
            w_scalar = scalar_mul(w, normal)

            if d_scalar == 0:
                if w_scalar < 0:
                    return  # параллельный невидимый
                else:
                    continue  # параллельный видимый

            t = -w_scalar / d_scalar

            if d_scalar > 0:  # ближе к началу отрезка
                if t <= 1:
                    t_bottom = max(t_bottom, t)
                else:
                    return
            elif d_scalar < 0:  # ближе к концу отрезка
                if t >= 0:
                    t_top = min(t_top, t)
                else:
                    return

            if t_bottom > t_top:
                break

        dot1_res = [round(dot1[0] + d[0] * t_bottom), round(dot1[1] + d[1] * t_bottom)]
        dot2_res = [round(dot1[0] + d[0] * t_top), round(dot1[1] + d[1] * t_top)]

        res_color = to_hex_from_rgb(self.res_color)

        if t_bottom <= t_top:
            self.canvas.create_line(dot1_res, dot2_res, fill=res_color, tag='result')



