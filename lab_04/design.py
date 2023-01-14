from tkinter import *
import tkinter as tk
from tkinter import font as tkFont

from tkinter import Tk, Radiobutton, Checkbutton, Canvas, Label, Entry, Button, DISABLED, NORMAL, IntVar, BooleanVar
from draw import draw_figure, draw_spectrum, clear_canvas, can_width, can_height
from comparisons import time_comparison

spectrum_var_arr, spectrum_entry_arr, spectrum_widget_arr = [], [], []

line_r = 150

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Лаб. раб. №4')
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

        self.canvas = Canvas(self, width=can_width, height=can_height, bg="white")
        self.canvas.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

        self.main_frame = Frame(self, bg=self.color_menu, height=150, width=700)
        self.main_frame.grid(row=0, column=0, rowspan=2, padx=30)

        # Алгоритмы построения
        self.alg_label = Label(self.main_frame, text="Алгоритм построения", font=self.helv14u, bg=self.color_menu)
        self.alg_label.grid(row=0, column=0, columnspan=4)

        self.algorithm = IntVar()
        self.algorithm.set(0)

        self.can_btn = Radiobutton(self.main_frame, text="Каноническое уравнение", variable=self.algorithm, value=0,
                    font=self.helv14, bg=self.color_menu, anchor="w")
        self.can_btn.grid(row=1, column=0, columnspan=4)

        self.par_btn = Radiobutton(self.main_frame, text="Параметрическое уравнение", variable=self.algorithm, value=1,
                    font=self.helv14, bg=self.color_menu, anchor="w")
        self.par_btn.grid(row=2, column=0, columnspan=4)

        self.brez_btn = Radiobutton(self.main_frame, text="Алгоритм Брезенхема", variable=self.algorithm, value=2,
                    font=self.helv14, bg=self.color_menu, anchor="w")
        self.brez_btn.grid(row=3, column=0, columnspan=4)

        self.mid_btn = Radiobutton(self.main_frame, text="Алгоритм средней точки", variable=self.algorithm, value=3,
                    font=self.helv14, bg=self.color_menu, anchor="w")
        self.mid_btn.grid(row=4, column=0, columnspan=4)

        self.lib_btn = Radiobutton(self.main_frame, text="Библиотечная функция", variable=self.algorithm, value=4,
                    font=self.helv14, bg=self.color_menu, anchor="w")
        self.lib_btn.grid(row=5, column=0, columnspan=4)


        # Выбор фигуры
        self.fig_label = Label(self.main_frame, text="Выбор фигуры", font=self.helv14u, bg=self.color_menu)
        self.fig_label.grid(row=6, column=0, columnspan=4)

        self.figure = BooleanVar()
        self.figure.set(0)

        self.circle_btn = Radiobutton(self.main_frame, text="Окружность", variable=self.figure, value=0,
                    font=self.helv14, bg=self.color_menu, anchor="w",
                    command=lambda: self.change_figure(self.rb_entry, self.figure))
        self.circle_btn.grid(row=7, column=0, columnspan=2)

        self.ellipse_btn = Radiobutton(self.main_frame, text="Эллипс", variable=self.figure, value=1,
                    font=self.helv14, bg=self.color_menu, anchor="w",
                    command=lambda: self.change_figure(self.rb_entry, self.figure))
        self.ellipse_btn.grid(row=7, column=2, columnspan=2)


        # Построение фигуры
        self.draw_fig_label = Label(self.main_frame, text="Построение фигуры", font=self.helv14u, bg=self.color_menu)
        self.draw_fig_label.grid(row=10, column=0, columnspan=4)

        self.coord_label = Label(self.main_frame, text="  Xc          Yc         Rx          Ry  ", font=self.helv14,
                                 bg=self.color_menu)
        self.coord_label.grid(row=11, column=0, columnspan=4)

        self.xc_entry = Entry(self.main_frame, font=self.helv14, width=5)
        self.xc_entry.grid(row=12, column=0)

        self.yc_entry = Entry(self.main_frame, font=self.helv14, width=5)
        self.yc_entry.grid(row=12, column=1)

        self.ra_entry = Entry(self.main_frame, font=self.helv14, width=5)
        self.ra_entry.grid(row=12, column=2)

        self.rb_entry = Entry(self.main_frame, font=self.helv14, width=5)
        self.rb_entry.grid(row=12, column=3)

        # self.Button(self, highlightbackground="#7575a3", highlightthickness=30, fg="#e0e0eb", state=DISABLED). \
        #     place(width=260, height=30, x=can_width + 30, y=390)

        self.draw_fig_btn = Button(self.main_frame, text="Построить фигуру", font=self.helv11, height=2, width=25,
                                   command=lambda: draw_figure(self.canvas, self.color_fg, self.algorithm, self.figure,
                                           self.xc_entry, self.yc_entry, self.ra_entry, self.rb_entry))
        self.draw_fig_btn.grid(row=13, column=0, columnspan=4, pady=10)


        # Построение спектра
        self.draw_spec_label = Label(self.main_frame, text="Построение спектра", font=self.helv14u, bg=self.color_menu)
        self.draw_spec_label.grid(row=14, column=0, columnspan=4)

        self.circle_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=700)
        self.ellipse_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=700)

        # self.Button(self, highlightbackground="#7575a3", highlightthickness=30, fg="#e0e0eb", state=DISABLED). \
        #     place(width=260, height=30, x=can_width + 30, y=615)

        self.draw_spec_btn = Button(self.main_frame, text="Построить cпектр", font=self.helv11, height=2, width=25,
               command=lambda: draw_spectrum(self.canvas, self.color_fg, self.algorithm, self.figure,
                                             self.xc_entry, self.yc_entry, spectrum_var_arr, spectrum_entry_arr))
        self.draw_spec_btn.grid(row=16, column=0, columnspan=4, pady=10)

        # self.Button(self, highlightbackground="#7575a3", highlightthickness=30, fg="#e0e0eb", state=DISABLED). \
        #     place(width=260, height=30, x=can_width + 30, y=655)

        self.time_btn = Button(self, text="Сравнение времени", font=self.helv11, height=2, width=20,
               command=lambda: time_comparison(self.canvas, self.color_fg, self.algorithm, self.figure))
        self.time_btn.grid(row=1, column=1)

        # self.Button(self, highlightbackground="#7575a3", highlightthickness=30, fg="#e0e0eb", state=DISABLED). \
        #     place(width=260, height=30, x=can_width + 30, y=695)

        self.clean_btn = Button(self, text="Очистить экран", font=self.helv11, height=2, width=20,
               command=lambda: clear_canvas(self.canvas))
        self.clean_btn.grid(row=1, column=2)

        self.xc_entry.insert(0, int(can_width / 2))
        self.yc_entry.insert(0, int(can_height / 2))

        self.ra_entry.insert(0, 200)
        self.rb_entry.insert(0, 150)
        self.rb_entry.configure(state=DISABLED)

        # --------------- ЦВЕТА ---------------
        self.color_fg = 'black'
        self.bg_color = 'white'
        self.size = 15

        # выбор цвета
        self.color_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=1000)
        self.color_frame.grid(row=9, column=0, columnspan=4, pady=10)

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

        self.color_line_label = Label(self.color_frame, bg=self.color_menu, text='Цвет линии:         Текущий:',
                                      font=self.helv14)
        self.color_line_label.grid(row=0, column=0, columnspan=7)

        self.cur_color_line = Label(self.color_frame, bg=self.color_fg, width=2)
        self.cur_color_line.grid(row=0, column=7)

        self.color_bg_label = Label(self.color_frame, bg=self.color_menu, text='Цвет фона: ', font=self.helv14)
        self.color_bg_label.grid(row=2, column=0, columnspan=8)

        self.change_figure(self.rb_entry, self.figure)

    def change_figure(self, rb_entry, figure):
        if figure.get() == True:
            rb_entry.configure(state=NORMAL)
            self.draw_fields_for_ellipse()
        else:
            rb_entry.configure(state=DISABLED)
            self.draw_fields_for_circle()

    def place_forget(self, spectrum_entry_arr, spectrum_widget_arr):
        for i in spectrum_entry_arr:
            i.place_forget()

        for i in spectrum_widget_arr:
            i.place_forget()

    def activate_fields(self, spectrum_entry, is_activate):
        if is_activate:
            spectrum_entry.configure(state=NORMAL)
        else:
            spectrum_entry.configure(state=DISABLED)

    def change_spectrum_entry(self, step_x_entry, step_y_entry, step_BooleanVar):
        if step_BooleanVar.get() == True:
            step_y_entry.configure(state=NORMAL)
            step_x_entry.configure(state=DISABLED)
        else:
            step_x_entry.configure(state=NORMAL)
            step_y_entry.configure(state=DISABLED)

    def choice_fields(self, spectrum_var_arr, spectrum_entry_arr, index_method):
        if spectrum_var_arr[index_method].get():
            spectrum_var_arr[index_method].set(0)
            return

        size = len(spectrum_var_arr)

        for i in range(size):
            if i != index_method and spectrum_var_arr[i].get() == False:
                spectrum_var_arr[i].set(1)
                self.activate_fields(spectrum_entry_arr[i], True)

        self.activate_fields(spectrum_entry_arr[index_method], False)

    def draw_fields_for_circle(self):
        global spectrum_var_arr, spectrum_entry_arr, spectrum_widget_arr

        self.place_forget(spectrum_entry_arr, spectrum_widget_arr)

        beg_radius_intvar = IntVar()
        end_radius_intvar = IntVar()
        step_intvar = IntVar()
        count_figure_intvar = IntVar()

        beg_radius_intvar.set(1)
        step_intvar.set(1)
        count_figure_intvar.set(1)

# 15
        self.ellipse_frame.grid_forget()
        self.circle_frame.grid(row=15, column=0, columnspan=4, pady=10)

        beg_radius_Checkbutton = Checkbutton(
            self.circle_frame,
            text="Начальный радиус:",
            variable=beg_radius_intvar,
            font=self.helv14, bg=self.color_menu, anchor="w",
            command=lambda: self.choice_fields(spectrum_var_arr, spectrum_entry_arr, 0))
        beg_radius_Checkbutton.grid(row=0, column=0)

        end_radius_Checkbutton = Checkbutton(
            self.circle_frame,
            text="Конечный радиус:",
            variable=end_radius_intvar,
            font=self.helv14, bg=self.color_menu, anchor="w",
            command=lambda: self.choice_fields(spectrum_var_arr, spectrum_entry_arr, 1))
        end_radius_Checkbutton.grid(row=1, column=0)

        step_Checkbutton = Checkbutton(
            self.circle_frame,
            text="Шаг построения:",
            variable=step_intvar,
            font=self.helv14, bg=self.color_menu, anchor="w",
            command=lambda: self.choice_fields(spectrum_var_arr, spectrum_entry_arr, 2))
        step_Checkbutton.grid(row=2, column=0)

        count_figure_Checkbutton = Checkbutton(
            self.circle_frame,
            text="Количество фигур:",
            variable=count_figure_intvar,
            font=self.helv14, bg=self.color_menu, anchor="w",
            command=lambda: self.choice_fields(spectrum_var_arr, spectrum_entry_arr, 3))
        count_figure_Checkbutton.grid(row=3, column=0)

        beg_radius_entry = Entry(self.circle_frame, font=self.helv14, width=5)
        beg_radius_entry.grid(row=0, column=1)

        end_radius_entry = Entry(self.circle_frame, font=self.helv14, width=5)
        end_radius_entry.grid(row=1, column=1)

        step_entry = Entry(self.circle_frame, font=self.helv14, width=5)
        step_entry.grid(row=2, column=1)

        count_figure_entry = Entry(self.circle_frame, font=self.helv14, width=5)
        count_figure_entry.grid(row=3, column=1)

        step_entry.insert(0, 10)
        count_figure_entry.insert(0, 15)

        beg_radius_entry.insert(0, 200)
        end_radius_entry.insert(0, 340)
        end_radius_entry.configure(state=DISABLED)

        spectrum_var_arr = [beg_radius_intvar, end_radius_intvar,
                            step_intvar, count_figure_intvar]
        spectrum_entry_arr = [beg_radius_entry, end_radius_entry,
                              step_entry, count_figure_entry]
        spectrum_widget_arr = [beg_radius_Checkbutton, end_radius_Checkbutton,
                               step_Checkbutton, count_figure_Checkbutton]

    def draw_fields_for_ellipse(self):
        global spectrum_var_arr, spectrum_entry_arr, spectrum_widget_arr

        self.place_forget(spectrum_entry_arr, spectrum_widget_arr)

        step_BooleanVar = BooleanVar()
        step_BooleanVar.set(0)

        self.circle_frame.grid_forget()
        self.ellipse_frame.grid(row=15, column=0, columnspan=4, pady=10)

        radius_x_Label = Label(
            self.ellipse_frame,
            text="Нач. значение Rx:",
            font=self.helv14, bg=self.color_menu, anchor="w")
        radius_x_Label.grid(row=0, column=0)

        radius_y_Label = Label(
            self.ellipse_frame,
            text="Нач. значение Ry:",
            font=self.helv14, bg=self.color_menu, anchor="w")
        radius_y_Label.grid(row=1, column=0)

        step_x_Radiobutton = Radiobutton(
            self.ellipse_frame,
            text="Шаг построения (ΔRx):",
            variable=step_BooleanVar, value=0,
            font=self.helv14, bg=self.color_menu, anchor="w",
            command=lambda: self.change_spectrum_entry(step_x_entry, step_y_entry, step_BooleanVar))
        step_x_Radiobutton.grid(row=2, column=0)

        step_y_Radiobutton = Radiobutton(
            self.ellipse_frame,
            text="Шаг построения (ΔRy):",
            variable=step_BooleanVar, value=1,
            font=self.helv14, bg=self.color_menu, anchor="w",
            command=lambda: self.change_spectrum_entry(step_x_entry, step_y_entry, step_BooleanVar))
        step_y_Radiobutton.grid(row=3, column=0)

        count_figure_Label = Label(
            self.ellipse_frame,
            text="Количество фигур:",
            font=self.helv14, bg=self.color_menu, anchor="w")
        count_figure_Label.grid(row=4, column=0)

        radius_x_entry = Entry(self.ellipse_frame, font=self.helv14, width=5)
        radius_x_entry.grid(row=0, column=1)

        radius_y_entry = Entry(self.ellipse_frame, font=self.helv14, width=5)
        radius_y_entry.grid(row=1, column=1)

        step_x_entry = Entry(self.ellipse_frame, font=self.helv14, width=5)
        step_x_entry.grid(row=2, column=1)

        step_y_entry = Entry(self.ellipse_frame, font=self.helv14, width=5)
        step_y_entry.grid(row=3, column=1)

        count_figure_entry = Entry(self.ellipse_frame, font=self.helv14, width=5)
        count_figure_entry.grid(row=4, column=1)

        radius_x_entry.insert(0, 200)
        radius_y_entry.insert(0, 100)

        count_figure_entry.insert(0, 20)
        step_x_entry.insert(0, 10)
        step_y_entry.insert(0, 10)
        step_y_entry.configure(state=DISABLED)

        spectrum_var_arr = [step_BooleanVar]
        spectrum_entry_arr = [radius_x_entry, radius_y_entry, step_x_entry, step_y_entry,
                              count_figure_entry]
        spectrum_widget_arr = [radius_x_Label, radius_y_Label, step_x_Radiobutton, step_y_Radiobutton,
                               count_figure_Label]

    def set_bgcolor(self, color):
        self.bg_color = color
        self.canvas.configure(bg=self.bg_color)

    def set_linecolor(self, color):
        self.color_fg = color
        self.cur_color_line.configure(bg=self.color_fg)
