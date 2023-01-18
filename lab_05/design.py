from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox

from time import time, sleep

from tkinter import Tk, Radiobutton, Checkbutton, Canvas, Label, Entry, Button, DISABLED, NORMAL, IntVar, BooleanVar
from process import bresenham_int, line_koefs, solve_lines_intersection, get_edges

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
        self.title('Лаб. раб. №5')
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

        self.xy_current = [-400, -350, -300, -250, -200, -150, -100, -50,
                      0, 50, 100, 150, 200, 250, 300, 350, 400]
        self.xy_history = [self.xy_current]  # история координат на оси

        self.canvas = Canvas(self, width=can_width, height=can_height, bg="white")
        self.canvas.grid(row=0, column=1, pady=10, padx=10)
        self.coord_center = [can_width // 2, can_height // 2]

        self.image_canvas = PhotoImage(width=can_width, height=can_height)

        self.main_frame = Frame(self, bg=self.color_menu, height=150, width=700)
        self.main_frame.grid(row=0, column=0, rowspan=2, padx=30)

        # Таблица координат
        self.alg_label = Label(self.main_frame, text="Координаты точек:", font=self.helv14u, bg=self.color_menu)
        self.alg_label.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        self.coords_table = Listbox(self.main_frame, font=self.helv11, width=25, height=12)
        self.coords_table.configure(font=self.helv14)
        self.coords_table.grid(row=1, column=0, columnspan=4, pady=10)

        self.coords_list = [[]]
        self.sides_list = [[]]

        # Построение точки
        self.x_label = Label(self.main_frame, text="X:", font=self.helv14, bg=self.color_menu)
        self.x_label.grid(row=2, column=0)
        self.x_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.x_entry.grid(row=2, column=1)

        self.y_label = Label(self.main_frame, text="Y:", font=self.helv14, bg=self.color_menu)
        self.y_label.grid(row=2, column=2)
        self.y_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.y_entry.grid(row=2, column=3)

        self.add_btn = Button(self.main_frame, text="Добавить", font=self.helv11, height=2, width=25, command=lambda: self.manual_add_dot())
        self.add_btn.grid(row=3, column=0, columnspan=4, pady=10)

        # Кнопка замыкания фигуры
        self.fin_fig_btn = Button(self.main_frame, text="Замкнуть", font=self.helv11, height=2, width=25, command=lambda: self.make_figure())
        self.fin_fig_btn.grid(row=4, column=0, columnspan=4, pady=10)


        # Варианты закраски
        self.option_filling = IntVar()
        self.option_filling.set(0)

        self.draw_label = Label(self.main_frame, text="Закраска", font=self.helv14u, bg=self.color_menu)
        self.draw_label.grid(row=5, column=0, columnspan=4)

        self.draw_delay_btn = Radiobutton(self.main_frame, text="С задержкой", font=self.helv11, variable=self.option_filling, value=1, bg=self.color_menu)
        self.draw_delay_btn.grid(row=6, column=0, columnspan=2)

        self.draw_without_delay_btn = Radiobutton(self.main_frame, text="Без задержки", font=self.helv11, variable=self.option_filling, value=0, bg=self.color_menu)
        self.draw_without_delay_btn.grid(row=6, column=2, columnspan=2)

        self.draw_btn = Button(self.main_frame, text="Закрасить", font=self.helv11, height=2, width=25, command=lambda: self.parse_fill())
        self.draw_btn.grid(row=7, column=0, columnspan=4)


        # --------------- ЦВЕТА ---------------
        self.fg_color = 'black'
        self.bg_color = 'white'
        self.size = 15

        # выбор цвета
        self.color_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=1000)
        self.color_frame.grid(row=8, column=0, columnspan=4, pady=20)

        self.white_line = Button(self.color_frame, bg="white", activebackground="white", width=2,
                            command=lambda: self.set_linecolor('white'))
        self.white_line.grid(row=1, column=0)

        self.yellow_line = Button(self.color_frame, bg="yellow", activebackground="yellow", width=2,
                             command=lambda: self.set_linecolor("yellow"))
        self.yellow_line.grid(row=1, column=1)

        self.orange_line = Button(self.color_frame, bg="orange", activebackground="orange", width=2,
                             command=lambda: self.set_linecolor("orange"))
        self.orange_line.grid(row=1, column=2)

        self.red_line = Button(self.color_frame, bg="red", activebackground="red", width=2,
                          command=lambda: self.set_linecolor("red"))
        self.red_line.grid(row=1, column=3)

        self.green_line = Button(self.color_frame, bg="green", activebackground="green", width=2,
                            command=lambda: self.set_linecolor("green"))
        self.green_line.grid(row=1, column=4)

        self.blue_line = Button(self.color_frame, bg="darkblue", activebackground="darkblue", width=2,
                           command=lambda: self.set_linecolor("darkblue"))
        self.blue_line.grid(row=1, column=5)

        self.purple_line = Button(self.color_frame, bg="purple", activebackground="purple", width=2,
                                  command=lambda: self.set_linecolor("purple"))
        self.purple_line.grid(row=1, column=6)

        self.black_line = Button(self.color_frame, bg="black", activebackground="black", width=2,
                            command=lambda: self.set_linecolor("black"))
        self.black_line.grid(row=1, column=7)

        self.white_bg = Button(self.color_frame, bg="white", activebackground="white", width=2,
                          command=lambda: self.set_bgcolor("white"))
        self.white_bg.grid(row=3, column=0)

        self.yellow_bg = Button(self.color_frame, bg="yellow", activebackground="yellow", width=2,
                           command=lambda: self.set_bgcolor("yellow"))
        self.yellow_bg.grid(row=3, column=1)

        self.orange_bg = Button(self.color_frame, bg="orange", activebackground="orange", width=2,
                           command=lambda: self.set_bgcolor("orange"))
        self.orange_bg.grid(row=3, column=2)

        self.red_bg = Button(self.color_frame, bg="red", activebackground="red", width=2,
                        command=lambda: self.set_bgcolor("red"))
        self.red_bg.grid(row=3, column=3)

        self.green_bg = Button(self.color_frame, bg="green", activebackground="green", width=2,
                          command=lambda: self.set_bgcolor("green"))
        self.green_bg.grid(row=3, column=4)

        self.blue_bg = Button(self.color_frame, bg="darkblue", activebackground="darkblue", width=2,
                         command=lambda: self.set_bgcolor("darkblue"))
        self.blue_bg.grid(row=3, column=5)

        self.purple_bg = Button(self.color_frame, bg="purple", activebackground="purple", width=2,
                                command=lambda: self.set_bgcolor("purple"))
        self.purple_bg.grid(row=3, column=6)

        self.black_bg = Button(self.color_frame, bg="black", activebackground="black", width=2,
                          command=lambda: self.set_bgcolor("black"))
        self.black_bg.grid(row=3, column=7)

        self.color_line_label = Label(self.color_frame, bg=self.color_menu, text='Цвет линии и заливки:    Текущий:',
                                      font=self.helv14)
        self.color_line_label.grid(row=0, column=0, columnspan=7)

        self.cur_color_line = Label(self.color_frame, bg=self.fg_color, width=2)
        self.cur_color_line.grid(row=0, column=7)

        self.color_bg_label = Label(self.color_frame, bg=self.color_menu, text='Цвет фона: ', font=self.helv14)
        self.color_bg_label.grid(row=2, column=0, columnspan=8)

        # Кнопка отката
        self.undo_btn = Button(self.main_frame, text="Откат", font=self.helv11, height=2, width=18, command=lambda: self.undo())
        self.undo_btn.grid(row=9, column=0, columnspan=2)

        # Кнопка очистки
        self.undo_btn = Button(self.main_frame, text="Очистить", font=self.helv11, height=2, width=18, command=lambda: self.clean_canvas())
        self.undo_btn.grid(row=9, column=2, columnspan=2)

        # Условие задачи
        self.info_btn = Button(self, text="Условие задачи", font=self.helv11, height=2, width=18, command=lambda: messagebox.showinfo("Задание", TASK))
        self.info_btn.grid(row=1, column=1)

        self.canvas.bind('<1>', self.click)
        self.bind("<Configure>", self.del_fill)

    def set_bgcolor(self, color):
        self.bg_color = color
        self.canvas.configure(bg=self.bg_color)

    def set_linecolor(self, color):
        self.fg_color = color
        self.cur_color_line.configure(bg=self.fg_color)

    # определение и запись координат точки по клику
    def click(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return
        self.draw_point(event.x, event.y, 1)

    def del_fill(self, event):
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

    # отрисовка соединений точек при клике - ребра
    def draw_lines(self, click_dots):
        for figure in click_dots:
            for i in range(len(figure) - 1):
                dots = bresenham_int(figure[i], figure[i + 1], self.fg_color)
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

    # очерчивание границ по ребрам
    def round_figure(self):
        for figure in range(len(self.sides_list)):
            sides_num = len(self.sides_list[figure]) - 1

            for side in range(sides_num + 1):
                self.round_side(self.sides_list[figure][side][0], self.sides_list[figure][side][1])

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
        self.sides_list.append(list())

        self.coords_table.insert(END, "-" * 50)

    # закраска
    def parse_fill(self):
        cur_figure = len(self.coords_list) - 1

        if len(self.coords_list[cur_figure]) != 0:
            messagebox.showerror("Ошибка", "Фигура не замкнута")
            return

        block_edges = get_edges(self.coords_list)

        delay = False
        if self.option_filling.get() == 1:
            delay = True

        self.fill_with_sides_and_flag(block_edges, delay=delay)

    #  отчистака канваса
    def clean_canvas(self):

        self.coords_list.clear()
        self.sides_list.clear()

        self.coords_list.append([])
        self.sides_list.append([])
        self.canvas.delete('line', 'dot')
        self.canvas.configure(bg=self.bg_color)
        self.coords_table.delete(0, END)

    # отрисовка и вставка в листбокс добавленной точки
    def draw_point(self, ev_x, ev_y, click_):

        if click_:
            x, y = ev_x, ev_y
        else:
            x, y = self.to_canvas([ev_x, ev_y])

        x_y = self.to_coords([x, y])
        cur_figure = len(self.coords_list) - 1
        self.coords_list[cur_figure].append([int(x), int(y)])

        cur_dot = len(self.coords_list[cur_figure]) - 1

        dot_str = "%d : (%-3.1f; %-3.1f)" % (cur_dot + 1, x_y[0], x_y[1])
        self.coords_table.insert(END, dot_str)

        self.canvas.delete('dot')
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                               outline='grey', fill='pink', activeoutline='lightgreen', width=2, tag='dot')

        color_line = self.fg_color
        if len(self.coords_list[cur_figure]) > 1:
            self.sides_list[cur_figure].append([self.coords_list[cur_figure][cur_dot - 1], self.coords_list[cur_figure][cur_dot]])
            dots = bresenham_int(self.coords_list[cur_figure][cur_dot - 1], self.coords_list[cur_figure][cur_dot], color_line)

            self.draw_line(dots)

    def fill_with_sides_and_flag(self, block_edges, delay=False):
        self.round_figure()
        self.canvas.update()

        color_fill = self.fg_color
        color_line = self.fg_color
        color_background = self.bg_color

        x_max = block_edges[2]
        x_min = block_edges[0]

        y_max = block_edges[3]
        y_min = block_edges[1]

        start_time = time()
        print("time = ", start_time)

        for y in range(y_min, y_max - 1, -1):
            flag = False

            for x in range(x_min, x_max + 2):
                if self.image_canvas.get(x, y) == TEMP_SIDE_COLOR_CHECK:
                    flag = not flag

                if flag:
                    self.image_canvas.put(color_fill, (x, y))
                    self.canvas.create_polygon([x, y], [x, y + 1],
                                              [x + 1, y + 1], [x + 1, y],
                                              fill=color_fill, tag='fill')
                else:
                    self.image_canvas.put(color_background, (x, y))
                    self.canvas.create_polygon([x, y], [x, y + 1],
                                              [x + 1, y + 1], [x + 1, y],
                                              fill=color_background, tag='fill')

            if delay:
                self.canvas.update()
                sleep(SLEEP_TIME)

        end_time = time()
        print("time = ", end_time)

        # Sides
        for fig in self.sides_list:
            for side in fig:
                dots = bresenham_int(side[0], side[1], color_line)
                self.draw_sides(dots)

        new_win = self.time_win(start_time, end_time)
        new_win.mainloop()

    # очерчивание границ по ребрам
    def round_side(self, dot1, dot2):
        if dot1[1] == dot2[1]:
            return

        a_side, b_side, c_side = line_koefs(dot1[0], dot1[1], dot2[0], dot2[1])

        if dot1[1] > dot2[1]:
            y_max = dot1[1]
            y_min = dot2[1]
            x = dot2[0]
        else:
            y_max = dot2[1]
            y_min = dot1[1]
            x = dot1[0]

        y = y_min

        while y < y_max:
            a_scan_line, b_scan_line, c_scan_line = line_koefs(x, y, x + 1, y)

            x_intersec, y_intersec = solve_lines_intersection(a_side, b_side, c_side, a_scan_line, b_scan_line,
                                                              c_scan_line)

            x_ = int(x_intersec)
            if self.image_canvas.get(x_ + 1, y) != TEMP_SIDE_COLOR_CHECK:
                x_ += 1

            else:
                x_ += 2

            self.image_canvas.put(TEMP_SIDE_COLOR, (x_, y))
            print(int(x_intersec), x_)

            self.canvas.create_polygon([x_, y], [x_, y + 1],
                                      [x_ + 1, y + 1], [x_ + 1, y],
                                      fill=TEMP_SIDE_COLOR, tag='line')

            y += 1

            self.canvas.update()

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

        s = -1
        if self.sides_list[-1] == []:
            if len(self.sides_list) > 1:
                s = -2
        if self.sides_list[0] != []:
            self.sides_list[s].pop()

        if len(self.coords_list) > 1 and self.coords_list[-2] == []:
            self.coords_list = self.coords_list[:-1]
        if len(self.sides_list) > 1 and self.sides_list[-2] == []:
            self.sides_list = self.sides_list[:-1]

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


