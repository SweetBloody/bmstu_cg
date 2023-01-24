from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox


from tkinter import Tk, Radiobutton, Canvas, Label, Entry, Button, IntVar

from process import get_dot_bits, check_visible, get_bit, are_bits_equal, find_rectangle

can_width = 1080
can_height = 720
line_r = 150
TEMP_SIDE_COLOR_CHECK = (255, 0, 255)
TEMP_SIDE_COLOR = "#ff00ff"
SLEEP_TIME = 0.0001

TASK = "Реализация (и исследование) " \
       "отсечения отрезка регулярным отсекателем " \
       "методом Сазерленда-Коэна"

def to_hex_from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Лаб. раб. №7')
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
        self.click_flag = 0
        self.start_line = []

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

        self.x1_rect_label = Label(self.main_frame, text="X1:", font=self.helv14, bg=self.color_menu)
        self.x1_rect_label.grid(row=5, column=0)
        self.x1_rect_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.x1_rect_entry.grid(row=5, column=1)

        self.y1_rect_label = Label(self.main_frame, text="Y1:", font=self.helv14, bg=self.color_menu)
        self.y1_rect_label.grid(row=6, column=0)
        self.y1_rect_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.y1_rect_entry.grid(row=6, column=1)

        self.x2_rect_label = Label(self.main_frame, text="X2:", font=self.helv14, bg=self.color_menu)
        self.x2_rect_label.grid(row=5, column=2)
        self.x2_rect_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.x2_rect_entry.grid(row=5, column=3)

        self.y2_rect_label = Label(self.main_frame, text="Y2:", font=self.helv14, bg=self.color_menu)
        self.y2_rect_label.grid(row=6, column=2)
        self.y2_rect_entry = Entry(self.main_frame, bg="white", font=self.helv14, width=9)
        self.y2_rect_entry.grid(row=6, column=3)

        self.add_rect_btn = Button(self.main_frame, text="Добавить", font=self.helv11, height=2, width=18, command=lambda: self.draw_clipper())
        self.add_rect_btn.grid(row=7, column=0, columnspan=4, pady=10)


        # --------------- ЦВЕТА ---------------
        self.otr_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.rect_color = (0, 0, 255)
        self.res_color = (255, 0, 0)
        self.size = 15

        # Выбор цвета
        self.color_frame = Frame(self.main_frame, bg=self.color_menu, height=150, width=1000)
        self.color_frame.grid(row=8, column=0, columnspan=4, pady=10)

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
        self.cut_btn.grid(row=9, column=0, columnspan=4, pady=20)


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

    # определение и запись координат точки по клику
    def click(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return

        if self.click_flag == 0:
            self.click_flag = 1
        elif self.click_flag == 1:
            self.click_flag = 2
        elif self.click_flag == 2:
            self.click_flag = 1

        self.draw_point(event.x, event.y, 1)

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

    #  отчистака канваса
    def clean_canvas(self):
        self.history = []
        self.lines = []
        self.clipper_coords = []

        self.canvas.delete('line', 'dot1', 'dot2', 'clipper1', 'clipper2', 'clipper', 'result')
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
        self.history.append([dot1, dot2, 'line'])

        self.canvas.delete('lineHelper')
        self.canvas.create_line(dot1, dot2, fill=color, tag='line')

    # нарисовать отсекатель
    def draw_clipper(self):
        self.canvas.delete('clipper', 'lineHelper')
        color = to_hex_from_rgb(self.rect_color)

        dot1 = self.to_canvas([int(self.x1_rect_entry.get()), int(self.y1_rect_entry.get())])
        dot2 = self.to_canvas([int(self.x2_rect_entry.get()), int(self.y2_rect_entry.get())])

        self.clipper_coords = [dot1, dot2]
        self.history.append([dot1, dot2, 'rectangle'])

        self.canvas.create_rectangle(dot1, dot2, outline=color, tag='clipper')

    # определение и запись координат точки по клику
    def click(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return

        if self.click_flag == 0:
            self.click_flag = 1
        elif self.click_flag == 1:
            self.click_flag = 2
        elif self.click_flag == 2:
            self.click_flag = 1

        self.draw_point(event.x, event.y, 1)

    def draw_all(self):
        color_line = to_hex_from_rgb(self.otr_color)
        color_clipper = to_hex_from_rgb(self.rect_color)
        for figure in self.history:
            if figure[2] == 'line':
                self.canvas.create_line(figure[0], figure[1], fill=color_line, tag='line')
            elif figure[2] == 'rectangle':
                self.canvas.create_rectangle(figure[0], figure[1], outline=color_clipper, tag='clipper')

    # отсечь
    def cut_area(self):

        if len(self.clipper_coords) < 1:
            messagebox.showinfo("Ошибка", "Не задан отсекатель")
            return

        if len(self.lines) < 1:
            messagebox.showinfo("Ошибка", "Не задан ни один отрезок")
            return

        clipper = [min(self.clipper_coords[0][0], self.clipper_coords[1][0]), max(self.clipper_coords[0][0], self.clipper_coords[1][0]),
                   min(self.clipper_coords[0][1], self.clipper_coords[1][1]), max(self.clipper_coords[0][1], self.clipper_coords[1][1])]

        for line in self.lines:
            self.method_sazerland_kohen(clipper, line)

    # предварительный просмотр линии
    def motion(self, event):
        if event.x < 0 or event.x > can_width or event.y < 0 or event.y > can_height:
            return

        if self.option_line.get() == 0:
            if self.click_flag == 1:
                self.canvas.delete("lineHelper")
                self.canvas.create_line(self.start_line[0], self.start_line[1], event.x, event.y,
                                       fill='grey', width=1,  tag='lineHelper')
        if self.option_line.get() == 1:
            if self.click_flag == 1:
                self.canvas.delete("lineHelper")
                self.canvas.create_rectangle(self.start_line[0], self.start_line[1], event.x, event.y,
                                            width=1, outline='grey', tag='lineHelper')

    # откат
    def undo(self):
        if len(self.history) == 0:
            messagebox.showerror("Внимание", "Достигнуто исходное состояние")
            return

        self.canvas.delete('line', 'dot1', 'dot2', 'clipper1', 'clipper2', 'clipper', 'result')

        deleted = self.history.pop()
        if deleted[2] == 'line':
            self.lines.pop()
        elif deleted[2] == 'rectangle':
            self.clipper_coords = find_rectangle(self.history)

        self.draw_all()

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
                                       outline='lightgreen', fill='lightgreen', activeoutline='pink', width=2,
                                       tag='dot1')

            if self.click_flag == 2:
                self.x2_otr_entry.delete(0, END)
                self.y2_otr_entry.delete(0, END)
                self.x2_otr_entry.insert(0, "%d" % x_y[0])
                self.y2_otr_entry.insert(0, "%d" % x_y[1])
                self.canvas.delete('dot2')
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                       outline='lightgreen', fill='lightgreen', activeoutline='pink', width=2,
                                       tag='dot2')
                self.draw_line()

        elif self.option_line.get() == 1:
            if self.click_flag == 1:
                self.start_line = [x, y]
                self.x1_rect_entry.delete(0, END)
                self.y1_rect_entry.delete(0, END)
                self.x1_rect_entry.insert(0, "%d" % x_y[0])
                self.y1_rect_entry.insert(0, "%d" % x_y[1])
                self.canvas.delete('clipper1')
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                       outline='pink', fill='pink', activeoutline='lightgreen', width=2, tag='clipper1')
            if self.click_flag == 2:
                self.x2_rect_entry.delete(0, END)
                self.y2_rect_entry.delete(0, END)
                self.x2_rect_entry.insert(0, "%d" % x_y[0])
                self.y2_rect_entry.insert(0, "%d" % x_y[1])
                self.canvas.delete('clipper2')
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2,
                                       outline='pink', fill='pink', activeoutline='lightgreen', width=2, tag='clipper2')
                self.draw_clipper()

    def method_sazerland_kohen(self, clipper, line):
        dot1 = [line[0][0], line[0][1]]
        dot2 = [line[1][0], line[1][1]]

        fl = 0

        if dot1[0] == dot2[0]:
            fl = -1  # вертикальный
        else:
            m = (dot2[1] - dot1[1]) / (dot2[0] - dot1[0])

            if m == 0:
                fl = 1  # горизонтальный

        for i in range(4):
            dot1_bits = get_dot_bits(clipper, dot1)
            dot2_bits = get_dot_bits(clipper, dot2)

            vision = check_visible(dot1_bits, dot2_bits)

            if vision == -1:
                return  # выйти и не рисовать
            elif vision == 1:
                break  # нарисовать и выйти

            if are_bits_equal(dot1_bits, dot2_bits, i):
                continue

            if get_bit(dot1_bits, i) == 0:
                tmp = dot1
                dot1 = dot2
                dot2 = tmp

            if fl != -1:  # если отрезок не вертикальный
                if i < 2:  # работаем с правой и левой сторонами
                    dot1[1] = m * (clipper[i] - dot1[0]) + dot1[1]
                    dot1[0] = clipper[i]
                    continue
                else:  # работаем с нижней и верхней сторонами
                    dot1[0] = (1 / m) * (clipper[i] - dot1[1]) + dot1[0]

            dot1[1] = clipper[i]

        res_color = to_hex_from_rgb(self.res_color)
        self.canvas.create_line(dot1, dot2, fill=res_color, tag='result')

