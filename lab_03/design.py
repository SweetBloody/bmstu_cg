from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from math import fabs, ceil, radians, cos, sin, floor, trunc
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time

from cda import cda_test, draw_line_cda
from bresenham_float import test_brez_float, draw_line_brez_float
from bresenham_int import test_brez_int, draw_line_brez_int
from bresenham_smooth import test_brez_smooth
from wu import test_vu
from porcess import sign, get_rgb_intensivity

can_width = 1080
can_height = 720
line_r = 150

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Лаб. раб. №3')
        self.color_menu = "#ccc"
        self.config(bg="#ccc")
        self.geometry('1536x800-0+0')
        self.resizable(width=False, height=False)
        self.wm_state('zoomed')
        helv11 = tkFont.Font(family='Helvetica', size=11)
        helv12 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        helv14 = tkFont.Font(family='Helvetica', size=14)
        helv14u = tkFont.Font(family='Helvetica', size=14, underline=1)
        helv16 = tkFont.Font(family='Helvetica', size=16)

        # выбор цвета
        self.color_frame = Frame(self, bg=self.color_menu, height=150, width=700)
        self.color_frame.grid(row=9, column=0, columnspan=4)

        self.canv = Canvas(self, width=can_width, height=can_height, bg='white')
        self.canvas = self.canv
        self.canvas_test = self.canv
        self.canv.grid(row=0, column=4, rowspan=12, columnspan=2, pady=10)
        self.center = (375, 200)

        # Список Алгоритмов
        self.method_list = Listbox(self, selectmode=EXTENDED, width=50, height=6, font=helv11)
        self.method_list.grid(row=0, column=0, columnspan=4, pady=10, padx=20)
        self.fill_list(self.method_list)
        self.funcs = (draw_line_cda, draw_line_brez_float, draw_line_brez_int,
                      self.draw_line_brez_smooth, self.draw_line_vu, self.canvas.create_line)
        self.test_funcs = (cda_test, test_brez_float, test_brez_int, test_brez_smooth, test_vu)

        self.start_label = Label(self, bg=self.color_menu, text='Начало линии:', font=helv14)
        self.end_label = Label(self, bg=self.color_menu, text='Конец линии:', font=helv14)
        self.start_label.grid(row=1, column=0, columnspan=4)
        self.end_label.grid(row=3, column=0, columnspan=4)

        self.x1_label = Label(self, bg=self.color_menu, text='X:', font=helv14)
        self.y1_label = Label(self, bg=self.color_menu, text='Y:', font=helv14)
        self.x2_label = Label(self, bg=self.color_menu, text='X:', font=helv14)
        self.y2_label = Label(self, bg=self.color_menu, text='Y:', font=helv14)
        self.x1_label.grid(row=2, column=0)
        self.y1_label.grid(row=2, column=2)
        self.x2_label.grid(row=4, column=0)
        self.y2_label.grid(row=4, column=2)

        self.x1_entry = Entry(self, bg="white", font=helv14, width=9)
        self.y1_entry = Entry(self, bg="white", font=helv14, width=9)
        self.x2_entry = Entry(self, bg="white", font=helv14, width=9)
        self.y2_entry = Entry(self, bg="white", font=helv14, width=9)
        self.x1_entry.grid(row=2, column=1)
        self.y1_entry.grid(row=2, column=3)
        self.x2_entry.grid(row=4, column=1)
        self.y2_entry.grid(row=4, column=3)
        self.x1_entry.insert(0, str(can_width / 2))
        self.y1_entry.insert(0, str(can_height / 2))
        self.x2_entry.insert(0, str(can_width / 2 + line_r))
        self.y2_entry.insert(0, str(can_height / 2 + line_r))

        self.btn_draw = Button(self, text="Построить отрезок", font=helv11, height=2, width=25, command=lambda: self.draw(0))
        self.btn_draw.grid(row=5, column=0, columnspan=4)

        self.angle_label = Label(self, bg=self.color_menu, text="Угол поворота (в градусах):", font=helv14)
        self.angle_label.grid(row=6, column=0, columnspan=4)

        self.angle_entry = Entry(self, bg="white", font=helv14, width=9)
        self.angle_entry.grid(row=7, column=0, columnspan=4)
        self.angle_entry.insert(0, "15")

        self.btn_sun = Button(self, text="Построить солнышко", font=helv11, height=2, width=25, command=lambda: self.draw(1))
        self.btn_sun.grid(row=8, column=0, columnspan=4)

        self.length_label = Label(self, bg=self.color_menu, text="Длина линии (по умолчанию 100):", font=helv14)
        self.length_label.grid(row=10, column=0, columnspan=4)

        self.length_entry = Entry(self, bg="white", font=helv14, width=9)
        self.length_entry.grid(row=11, column=0, columnspan=4)

        self.btn_time = Button(self, text="Сравнение времени\nпостроения", font=helv11, height=2, width=20, command=lambda: self.analyze(0))
        self.btn_time.grid(row=12, column=0, columnspan=2)

        self.btn_smooth = Button(self, text="Сравнение\nступенчатости", font=helv11, height=2, width=20, command=lambda: self.analyze(1))
        self.btn_smooth.grid(row=12, column=2, columnspan=2)

        self.btn_clean = Button(self, text="Очистить экран", font=helv11, height=2, width=20, command=self.clean)
        self.btn_clean.grid(row=12, column=4)

        self.btn_help = Button(self, text="Справка", font=helv11, height=2, width=20, command=self.show_info)
        self.btn_help.grid(row=12, column=5)

        # --------------- ЦВЕТА ---------------
        self.line_color = 'black'
        self.bg_color = 'white'
        self.size = 15

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

        self.color_line_label = Label(self.color_frame, bg=self.color_menu, text='Цвет линии:         Текущий:', font=helv14)
        self.color_line_label.grid(row=0, column=0, columnspan=7)

        self.cur_color_line = Label(self.color_frame, bg=self.line_color, width=2)
        self.cur_color_line.grid(row=0, column=7)

        self.color_bg_label = Label(self.color_frame, bg=self.color_menu, text='Цвет фона: ', font=helv14)
        self.color_bg_label.grid(row=2, column=0, columnspan=8)

        self.draw_axes()

    def draw_line_brez_smooth(self, canvas, ps, pf, fill):
        I = 100
        fill = get_rgb_intensivity(canvas, fill, self.bg_color, I)
        dx = pf[0] - ps[0]
        dy = pf[1] - ps[1]
        sx = sign(dx)
        sy = sign(dy)
        dy = abs(dy)
        dx = abs(dx)
        if dy >= dx:
            dx, dy = dy, dx
            steep = 1
        else:
            steep = 0
        tg = dy / dx * I
        e = I / 2
        w = I - tg
        x = ps[0]
        y = ps[1]
        stairs = []
        st = 1
        while x != pf[0] or y != pf[1]:
            canvas.create_line(x, y, x + 1, y + 1, fill=fill[round(e) - 1])
            if e < w:
                if steep == 0:
                    x += sx
                else:
                    y += sy
                st += 1  # stepping
                e += tg
            elif e >= w:
                x += sx
                y += sy
                e -= w
                stairs.append(st)
                st = 0
        if st:
            stairs.append(st)
        return stairs

    def draw_line_vu(self, canvas, ps, pf, fill):
        x1 = ps[0]
        x2 = pf[0]
        y1 = ps[1]
        y2 = pf[1]
        I = 100
        stairs = []
        fills = get_rgb_intensivity(canvas, fill, self.bg_color, I)
        if x1 == x2 and y1 == y2:
            canvas.create_line(x1, y1, x1 + 1, y1 + 1, fill=fills[100])

        steep = abs(y2 - y1) > abs(x2 - x1)

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            tg = 1
        else:
            tg = dy / dx

        xend = round(x1)
        yend = y1 + tg * (xend - x1)
        xpx1 = xend
        y = yend + tg

        xend = int(x2 + 0.5)
        xpx2 = xend
        st = 0

        if steep:
            for x in range(xpx1, xpx2):
                canvas.create_line(int(y), x + 1, int(y) + 1, x + 2,
                                   fill=fills[int((I - 1) * (abs(1 - y + int(y))))])
                canvas.create_line(int(y) + 1, x + 1, int(y) + 2, x + 2,
                                   fill=fills[int((I - 1) * (abs(y - int(y))))])

                if (abs(int(x) - int(x + 1)) >= 1 and tg > 1) or \
                        (not 1 > abs(int(y) - int(y + tg)) >= tg):
                    stairs.append(st)
                    st = 0
                else:
                    st += 1
                y += tg
        else:
            for x in range(xpx1, xpx2):
                canvas.create_line(x + 1, int(y), x + 2, int(y) + 1,
                                   fill=fills[round((I - 1) * (abs(1 - y + floor(y))))])
                canvas.create_line(x + 1, int(y) + 1, x + 2, int(y) + 2,
                                   fill=fills[round((I - 1) * (abs(y - floor(y))))])

                if (abs(int(x) - int(x + 1)) >= 1 and tg > 1) or \
                        (not 1 > abs(int(y) - int(y + tg)) >= tg):
                    stairs.append(st)
                    st = 0
                else:
                    st += 1
                y += tg
        return stairs

    # Получение параметров для отрисовки
    def draw(self, test_mode):
        choice = self.method_list.curselection()
        if len(choice) == 1:
            xs, ys = self.x1_entry.get(), self.y1_entry.get()
            xf, yf = self.x2_entry.get(), self.y2_entry.get()
            if not xs and not ys:
                messagebox.showwarning('Ошибка ввода',
                                       'Не заданы координаты начала отрезка!')
            elif not xs or not ys:
                messagebox.showwarning('Ошибка ввода',
                                       'Не задана одна из координат начала отрезка!')
            elif not xf and not yf:
                messagebox.showwarning('Ошибка ввода',
                                       'Не заданы координаты конца отрезка!')
            elif not xf or not yf:
                messagebox.showwarning('Ошибка ввода',
                                       'Не задана одна из координат конца отрезка!')
            else:
                # try:
                xs, ys = round(float(xs)), round(float(ys))
                xf, yf = round(float(xf)), round(float(yf))
                if xs != xf or ys != yf:
                    if not test_mode:
                        if choice[0] == 5:
                            self.canvas.create_line([xs, ys], [xf, yf], fill=self.line_color)
                        else:
                            self.funcs[choice[0]](self.canvas, [xs, ys], [xf, yf], fill=self.line_color)
                    else:
                        angle = self.angle_entry.get()
                        if angle:
                            try:
                                angle = round(float(angle))
                            except:
                                messagebox.showwarning('Ошибка ввода',
                                                       'Введено не целочисленное значение для шага анализа!')

                            if angle:
                                self.test(1, choice[0], self.funcs[choice[0]], angle, [xs, ys], [xf, yf])
                            else:
                                messagebox.showwarning('Ошибка ввода',
                                                       'Задано нулевое значение для угла поворота!')

                        else:
                            messagebox.showwarning('Ошибка ввода',
                                                   'Не задано значение для шага анализа!')
                else:
                    messagebox.showwarning('Ошибка ввода',
                                           'Начало и конец отрезка совпадают!')
            # except:
            # messagebox.showwarning('Ошибка ввода',
            #                       'Нечисловое значение для параметров отрезка!')
        elif not len(choice):
            messagebox.showwarning('Ошибка ввода',
                                   'Не выбран метод построения отрезка!')
        else:
            messagebox.showwarning('Ошибка ввода',
                                   'Выбрано более одного метода простроения отрезка!')

    # Получение параметров для анализа
    def analyze(self, mode):
        try:
            length = self.length_entry.get()
            if length:
                length = int(length)
            else:
                length = 100
            if not mode:
                self.time_bar(length)
            else:
                ind = self.method_list.curselection()
                if ind:
                    if ind[-1] != 5:
                        self.smooth_analyze(ind, length)
                    else:
                        messagebox.showwarning('Предупреждение',
                                               'Стандартный метод не может '
                                               'быть проанализирован на ступенчатость!')
                else:
                    messagebox.showwarning('Предупреждение',
                                           'Не выбрано ни одного '
                                           'метода построения отрезка!')
        except:
            messagebox.showwarning('Предупреждение',
                                   'Введено нечисловое значение для длины отрезка!')

    # замер времени
    def test(self, flag, ind, method, angle, pb, pe):
        total = 0
        steps = int(360 // angle)
        for i in range(steps):
            cur1 = time.time()
            if flag == 0:
                # method(pb, pe)
                if ind == 5:
                    method(pb, pe, fill=self.bg_color)
                else:
                    method(self.canvas, pb, pe, fill=self.bg_color)
            else:
                if ind == 5:
                    method(pb, pe, fill=self.line_color)
                else:
                    method(self.canvas, pb, pe, fill=self.line_color)
            cur2 = time.time()
            self.turn_point(radians(angle), pe, pb)
            total += cur2 - cur1
        return total / steps


    # гистограмма времени
    def time_bar(self, length):
        self.close_plt()
        root = Tk()
        root.geometry('900x700')
        root.resizable(0, 0)
        root.title("Анализ времени")
        fig = plt.figure()
        times = []
        angle = 1
        pb = [self.center[0], self.center[1]]
        pe = [self.center[0] + 100, self.center[1]]
        for i in range(5):
            #        times.append(test(0, i, test_funcs[i], angle, pb, pe))
            times.append(self.test(0, i, self.funcs[i], angle, pb, pe))
        self.clean()
        Y = range(len(times))
        L = ('ЦДА', 'Брезенхем (float)',
             'Брезенхем (int)', 'Брезенхем\nсо сглаживанием', 'ВУ')
        fig.add_subplot(111)
        canvasAgg = FigureCanvasTkAgg(fig, master=root)
        plt.bar(Y, times, align='center')
        plt.xticks(Y, L)
        plt.ylabel("Время построения в сек. (Длина отрезка = " + str(length) + ")")
        canvasAgg.draw()
        canvas = canvasAgg.get_tk_widget()
        canvas.pack(fill=BOTH, expand=1)
        root.mainloop()

    # Поворот точки для сравнения ступенчатости
    def turn_point(self, angle, p, center):
        x = p[0]
        p[0] = round(center[0] + (x - center[0]) * cos(angle) + (p[1] - center[1]) * sin(angle))
        p[1] = round(center[1] - (x - center[0]) * sin(angle) + (p[1] - center[1]) * cos(angle))

    # Анализ ступечатости
    def smooth_analyze(self, methods, length):
        self.close_plt()
        root = Tk()
        root.geometry('900x700')
        root.resizable(0, 0)
        root.title("Анализ времени")
        names = ('ЦДА', 'Брезенхем (float)',
                 'Брезенхем (int)', 'Брезенхем\nсо сглаживанием', 'Ву')
        fig = plt.figure(1)
        fig.add_subplot(111)
        canvasAgg = FigureCanvasTkAgg(fig, master=root)
        plt.title("Анализ ступенчатости")
        plt.xlabel("Угол")
        plt.ylabel("Количество ступеней (Длина отрезка = " + str(length) + ")")
        plt.grid(True)
        plt.legend(loc='best')

        for i in methods:
            max_len = []
            nums = []
            angles = []
            angle = 0
            step = 2
            pb = [self.center[0], self.center[1]]
            pe = [self.center[0] + length, self.center[1]]

            for j in range(90 // step):
                stairs = self.funcs[i](self.canvas, pb, pe, self.line_color)
                self.turn_point(radians(step), pe, pb)
                if stairs:
                    max_len.append(max(stairs))
                else:
                    max_len.append(0)
                nums.append(len(stairs))
                angles.append(angle)
                angle += step
            self.clean()
            plt.figure(1)
            plt.plot(angles, nums, label=names[i])
            plt.legend()
        canvasAgg.draw()
        canvas = canvasAgg.get_tk_widget()
        canvas.pack(fill=BOTH, expand=1)
        root.mainloop()

    # Оси координат
    def draw_axes(self):
        return
        color = 'gray'
        self.canvas.create_line(0, 2, can_width, 2, fill="darkred", arrow=LAST)
        self.canvas.create_line(2, 0, 2, can_height, fill="darkred", arrow=LAST)
        for i in range(50, can_width, 50):
            self.canvas.create_text(i, 10, text=str(abs(i)), fill=color)
            self.canvas.create_line(i, 0, i, 5, fill=color)

        for i in range(50, can_height, 50):
            self.canvas.create_text(15, i, text=str(abs(i)), fill=color)
            self.canvas.create_line(0, i, 5, i, fill=color)

    # очистка канваса
    def clean(self):
        self.canvas.delete("all")
        self.draw_axes()

    # Справка
    def show_info(self):
        messagebox.showinfo('Информация',
                            'С помощью данной программы можно построить отрезки пятью способами:\n'
                            '1) методом цифрового дифференциального анализатора;\n'
                            '2) методом Брезенхема с действитльными коэфициентами;\n'
                            '3) методом Брезенхема с целыми коэфициентами;\n'
                            '4) методом Брезенхема со сглаживанием;\n'
                            '5) методом Ву;\n'
                            '6) стандартым методом.\n'
                            '\nДля построения отрезка необходимо задать его начало\n'
                            'и конец и выбрать метод построения из списка предложенных.\n'
                            '\nДля визуального анализа (построения пучка отрезков)\n'
                            'необходимо задать начало и конец,\n'
                            'выбрать метод для анализа,\n'
                            'а также угол поворота отрезка.\n')

    # Список методов прорисовки отрезка
    def fill_list(self, lst):
        lst.insert(END, "Цифровой дифференциальный анализатор")
        lst.insert(END, "Брезенхем (float)")
        lst.insert(END, "Брезенхем (int)")
        lst.insert(END, "Брезенхем со сглаживанием")
        lst.insert(END, "Ву")
        lst.insert(END, "Стандартный")

    def set_bgcolor(self, color):
        self.bg_color = color
        self.canvas.configure(bg=self.bg_color)

    def set_linecolor(self, color):
        self.line_color = color
        self.cur_color_line.configure(bg=self.line_color)

    def close_plt(self):
        plt.figure(1)
        plt.close()
        plt.figure(2)
        plt.close()
