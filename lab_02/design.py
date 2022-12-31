from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from process import *
import copy

can_width = 1090
can_height = 720
coord_x = can_width // 2
coord_y = can_height // 2
main_alarm = Alarm(100, 100)
states = []


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лаб. раб. №2")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry('1536x800-0+0')
        self.wm_state('zoomed')
        self.config(bg="#ccc")
        helv11 = tkFont.Font(family='Helvetica', size=11)
        helv12 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        helv14 = tkFont.Font(family='Helvetica', size=14)
        helv14u = tkFont.Font(family='Helvetica', size=14, underline=1)
        helv16 = tkFont.Font(family='Helvetica', size=16)

        # Центральная точка
        self.central_coords = Label(self, width=35, height=3, font=helv14, justify=CENTER,
                          text='Центральная точка:\n'
                               'x = {0:.6}, y = {1:.6}'.format(float(main_alarm.center_x), float(main_alarm.center_y)),
                                    bg='#ccc')
        self.central_coords.grid(row=0, column=0, columnspan=4)

        # Графический результат
        self.canvas = Canvas(self, width=can_width, height=can_height, bg='white')
        self.canvas.grid(row=0, column=4, rowspan=12, pady=10)

        # Перенос
        #  надпись
        self.move_label = Label(self, width=35, height=1, font=helv14u, justify=CENTER,
                          text='Перенос', bg='#ccc')
        self.move_label.grid(row=1, column=0, columnspan=4)
        #  ввод координат x
        self.move_x_label = Label(self, width=3, height=1, font=helv14, justify=CENTER,
                          text='dx:', bg='#ccc')
        self.move_x_label.grid(row=2, column=0)

        self.move_x = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.move_x.grid(row=2, column=1)
        #  ввод координат y
        self.move_y_label = Label(self, width=3, height=1, font=helv14, justify=CENTER,
                          text='dy:', bg='#ccc')
        self.move_y_label.grid(row=2, column=2)

        self.move_y = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.move_y.grid(row=2, column=3)
        #  кнопка переноса
        self.move_btn = Button(self, text='Осуществить перенос', font=helv11, width=22, height=2, command=self.move_image)
        self.move_btn.grid(row=3, column=0, columnspan=4)

        # Надпись центр масштабирования
        self.center_label = Label(self, width=35, height=1, font=helv14, justify=CENTER,
                          text='Центр масштабирования и поворота', bg='#ccc')
        self.center_label.grid(row=4, column=0, columnspan=4)
        #  ввод координат x
        self.center_x_label = Label(self, width=3, height=1, font=helv14, justify=CENTER,
                          text='x:', bg='#ccc')
        self.center_x_label.grid(row=5, column=0)

        self.center_x = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.center_x.insert(0, '{}'.format(main_alarm.center_y))
        self.center_x.grid(row=5, column=1)
        #  ввод координат y
        self.center_y_label = Label(self, width=3, height=1, font=helv14, justify=CENTER,
                          text='y:', bg='#ccc')
        self.center_y_label.grid(row=5, column=2)

        self.center_y = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.center_y.insert(0, '{}'.format(main_alarm.center_y))
        self.center_y.grid(row=5, column=3)

        # Масштабирование
        #  надпись
        self.scale_label = Label(self, width=35, height=1, font=helv14u, justify=CENTER,
                          text='Масштабирование', bg='#ccc')
        self.scale_label.grid(row=6, column=0, columnspan=4)
        #  ввод коэффициента по x
        self.scale_x_label = Label(self, width=3, height=1, font=helv14, justify=CENTER,
                          text='kx:', bg='#ccc')
        self.scale_x_label.grid(row=7, column=0)

        self.scale_x = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.scale_x.grid(row=7, column=1)
        #  ввод коэффициента по y
        self.scale_y_label = Label(self, width=3, height=1, font=helv14, justify=CENTER,
                          text='ky:', bg='#ccc')
        self.scale_y_label.grid(row=7, column=2)

        self.scale_y = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.scale_y.grid(row=7, column=3)
        #  кнопка масштабирования
        self.scale_btn = Button(self, text='Осуществить масштабирование', font=helv11, width=27, height=2, command=self.scale_image)
        self.scale_btn.grid(row=8, column=0, columnspan=4)

        # Поворот
        #  надпись
        self.rotate_label = Label(self, width=35, height=1, font=helv14u, justify=CENTER,
                          text='Поворот', bg='#ccc')
        self.rotate_label.grid(row=9, column=0, columnspan=4)
        #  ввод угла поворота
        self.rotate_angle_label = Label(self, width=5, height=1, font=helv14, justify=CENTER,
                          text='Угол:', bg='#ccc')
        self.rotate_angle_label.grid(row=10, column=0, columnspan=2)

        self.rotate_angle = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.rotate_angle.grid(row=10, column=2, columnspan=2)
        #  кнопка поворота
        self.rotate_btn = Button(self, text='Осуществить Поворот', font=helv11, width=27, height=2, command=self.rotate_image)
        self.rotate_btn.grid(row=11, column=0, columnspan=4)

        # Кнопка отката назад
        self.back_btn = Button(self, text='Вернуть назад', font=helv11, width=27, height=2, command=self.back_image)
        self.back_btn.grid(row=12, column=4)

        # Будильник
        self.alarm = Alarm(main_alarm.center_x, main_alarm.center_y)

        self.canvas_clear()
        self.change_coords()
        self.draw_alarm()

    # Чтение полей координат с центром масштабирования и поворота
    def read_center(self):
        try:
            xc = int(self.center_x.get())
            yc = int(self.center_y.get())
            return 1, xc, yc
        except Exception as exception:
            print(exception)
            messagebox.showerror('Ошибка', 'Неверный ввод центра масштабирования\n'
                                           'и поворота!\n'
                                           'Введите целое число!')
            return 0, 0, 0

    # Чтение полей коэффициентов масштабирования
    def read_scale(self):
        try:
            kx = float(self.scale_x.get())
            ky = float(self.scale_y.get())
            if kx == 0 or ky == 0:
                messagebox.showerror('Ошибка', 'Неверный ввод коэффициента масштабирования!\n'
                                               'Введите число большее нуля!')
                return 0, 0, 0
            return 1, kx, ky
        except Exception as exception:
            print(exception)
            messagebox.showerror('Ошибка', 'Неверный ввод коэффициента масштабирования!\n'
                                           'Введите число!')
            return 0, 0, 0

    # Чтение поля поворота
    def read_rotate(self):
        try:
            angle = float(self.rotate_angle.get())
            return 1, angle
        except Exception as exception:
            print(exception)
            messagebox.showerror('Ошибка', 'Неверный ввод значения поворота!\n'
                                           'Введите число!')
            return 0, 0

    # Кнопка переноса
    def move_image(self):
        try:
            global main_alarm
            self.add_state()
            main_alarm = coord_change_move(main_alarm,
                                           int(self.move_x.get()),
                                           int(self.move_y.get()))
            self.canvas_clear()
            self.change_coords()
            self.draw_alarm()
            self.central_coords.config(text='Центральная точка:\n'
                                            'x = {0:.6}, y = {1:.6}'.format(float(main_alarm.center_x),
                                                                            float(main_alarm.center_y)))
        except Exception as exception:
            print(exception)
            messagebox.showerror('Ошибка', 'Неверный ввод смещения!\n'
                                           'Введите целое число!')

    # Кнопка масштабирования
    def scale_image(self):
        global main_alarm
        ch1, xc, yc = self.read_center()
        ch2, kx, ky = self.read_scale()
        if ch1 and ch2:
            self.add_state()
            main_alarm = coord_change_scale(main_alarm, xc, yc, kx, ky)
            self.canvas_clear()
            self.change_coords()
            self.draw_alarm()
            self.central_coords.config(text='Центральная точка:\n'
                                            'x = {0:.6}, y = {1:.6}'.format(float(main_alarm.center_x),
                                                                            float(main_alarm.center_y)))

    # Кнопка поворота
    def rotate_image(self):
            global main_alarm
            ch1, xc, yc = self.read_center()
            ch2, angle = self.read_rotate()
            if ch1 and ch2:
                self.add_state()
                main_alarm = coord_change_rotate(main_alarm, xc, yc, angle)
                self.canvas_clear()
                self.change_coords()
                self.draw_alarm()
                self.central_coords.config(text='Центральная точка:\n'
                                                'x = {0:.6}, y = {1:.6}'.format(float(main_alarm.center_x),
                                                                                float(main_alarm.center_y)))

    # Кнопка отката
    def back_image(self):
        try:
            global main_alarm
            main_alarm = states[len(states) - 1]
            states.pop(len(states) - 1)
            self.canvas_clear()
            self.change_coords()
            self.draw_alarm()
            self.central_coords.config(text='Центральная точка:\n'
                                            'x = {0:.6}, y = {1:.6}'.format(float(main_alarm.center_x),
                                                                            float(main_alarm.center_y)))
        except Exception as exception:
            print(exception)
            messagebox.showerror('Ошибка', 'Вы перешли в начальное состояние!')

    # Отрисовка системы координат
    def canvas_clear(self):
        self.canvas.delete('all')
        self.canvas.create_line(coord_x, can_height - 5, coord_x, 5, width=2, arrow=LAST)
        self.canvas.create_line(5, coord_y, can_width - 5, coord_y, width=2, arrow=LAST)
        self.canvas_spots()

    # Отрисовка штрихов
    def canvas_spots(self):
        y1 = change_y(-5)
        y2 = change_y(5)
        for i in range(50, 501, 50):
            x1 = change_x(i)
            x2 = change_x(-i)
            self.canvas.create_line(x1, y1, x1, y2, width=2)
            self.canvas.create_text(x1, y1 + 5, text=str(i))
            self.canvas.create_line(x2, y1, x2, y2, width=2)
            self.canvas.create_text(x2, y1 + 5, text=str(-i))

        x1 = change_x(-5)
        x2 = change_x(5)
        for i in range(50, 301, 50):
            y1 = change_y(i)
            y2 = change_y(-i)
            self.canvas.create_line(x1, y1, x2, y1, width=2)
            self.canvas.create_text(x1 - 10, y1, text=str(i))
            self.canvas.create_line(x1, y2, x2, y2, width=2)
            self.canvas.create_text(x1 - 10, y2, text=str(-i))

    # Отрисовка будильника
    def draw_alarm(self):
        # Циферблат будильника
        num = self.alarm.num_points - 1
        self.canvas.create_line(self.alarm.alarm_points[0][0],
                                self.alarm.alarm_points[0][1],
                                self.alarm.alarm_points[num][0],
                                self.alarm.alarm_points[num][1], fill='orange')
        self.canvas.create_line(self.alarm.bell_points[0][0],
                                self.alarm.bell_points[0][1],
                                self.alarm.bell_points[num][0],
                                self.alarm.bell_points[num][1], fill='green')
        for i in range(num):
            x = self.alarm.alarm_points[i][0]
            y = self.alarm.alarm_points[i][1]
            x1 = self.alarm.alarm_points[i + 1][0]
            y1 = self.alarm.alarm_points[i + 1][1]
            self.canvas.create_line(x, y, x1, y1, fill='orange')
            x = self.alarm.bell_points[i][0]
            y = self.alarm.bell_points[i][1]
            x1 = self.alarm.bell_points[i + 1][0]
            y1 = self.alarm.bell_points[i + 1][1]
            self.canvas.create_line(x, y, x1, y1, fill='green')

        # Отметки на часах (3, 6, 9, 12 часов)
        for i in range(4):
            self.canvas.create_line(self.alarm.hours[i][0], self.alarm.hours[i][1],
                                    self.alarm.hours[i][2], self.alarm.hours[i][3],
                                    fill='black')

        # Стрелки часов
        for i in range(2):
            self.canvas.create_line(self.alarm.arrows[i][0], self.alarm.arrows[i][1],
                                    self.alarm.arrows[i][2], self.alarm.arrows[i][3],
                                    fill='black')

        # Ножки будильника
        for i in range(2):
            self.canvas.create_line(self.alarm.legs[i][0], self.alarm.legs[i][1],
                                    self.alarm.legs[i][2], self.alarm.legs[i][3],
                                    fill='purple')

        # Звонок
        for i in range(160):
            x1 = self.alarm.bottom_arc[i][0]
            y1 = self.alarm.bottom_arc[i][1]
            x2 = self.alarm.bottom_arc[i + 1][0]
            y2 = self.alarm.bottom_arc[i + 1][1]
            self.canvas.create_line(x1, y1, x2, y2, fill='blue')
            x1 = self.alarm.top_arc[i][0]
            y1 = self.alarm.top_arc[i][1]
            x2 = self.alarm.top_arc[i + 1][0]
            y2 = self.alarm.top_arc[i + 1][1]
            self.canvas.create_line(x1, y1, x2, y2, fill='blue')

        self.canvas.create_line(self.alarm.parts[0][0], self.alarm.parts[0][1],
                                self.alarm.parts[0][2], self.alarm.parts[0][3],
                                fill='red')
        self.canvas.create_line(self.alarm.parts[1][0], self.alarm.parts[1][1],
                                self.alarm.parts[1][2], self.alarm.parts[1][3],
                                fill='red')

    # Изменение системы координат
    def change_coords(self):
        self.alarm.center_x = change_x(main_alarm.center_x)
        self.alarm.center_y = change_y(main_alarm.center_y)

        for i in range(4):
            self.alarm.hours[i][0] = change_x(main_alarm.hours[i][0])
            self.alarm.hours[i][1] = change_y(main_alarm.hours[i][1])
            self.alarm.hours[i][2] = change_x(main_alarm.hours[i][2])
            self.alarm.hours[i][3] = change_y(main_alarm.hours[i][3])

        for i in range(2):
            self.alarm.arrows[i][0] = change_x(main_alarm.arrows[i][0])
            self.alarm.arrows[i][1] = change_y(main_alarm.arrows[i][1])
            self.alarm.arrows[i][2] = change_x(main_alarm.arrows[i][2])
            self.alarm.arrows[i][3] = change_y(main_alarm.arrows[i][3])
            self.alarm.legs[i][0] = change_x(main_alarm.legs[i][0])
            self.alarm.legs[i][1] = change_y(main_alarm.legs[i][1])
            self.alarm.legs[i][2] = change_x(main_alarm.legs[i][2])
            self.alarm.legs[i][3] = change_y(main_alarm.legs[i][3])
            self.alarm.parts[i][0] = change_x(main_alarm.parts[i][0])
            self.alarm.parts[i][1] = change_y(main_alarm.parts[i][1])
            self.alarm.parts[i][2] = change_x(main_alarm.parts[i][2])
            self.alarm.parts[i][3] = change_y(main_alarm.parts[i][3])

        for i in range(self.alarm.num_points):
            self.alarm.alarm_points[i][0] = change_x(main_alarm.alarm_points[i][0])
            self.alarm.alarm_points[i][1] = change_y(main_alarm.alarm_points[i][1])
            self.alarm.bell_points[i][0] = change_x(main_alarm.bell_points[i][0])
            self.alarm.bell_points[i][1] = change_y(main_alarm.bell_points[i][1])

        for i in range(161):
            self.alarm.bottom_arc[i][0] = change_x(main_alarm.bottom_arc[i][0])
            self.alarm.bottom_arc[i][1] = change_y(main_alarm.bottom_arc[i][1])
            self.alarm.top_arc[i][0] = change_x(main_alarm.top_arc[i][0])
            self.alarm.top_arc[i][1] = change_y(main_alarm.top_arc[i][1])

    # Добавление нового состояния в список всех состояний
    def add_state(self):
        prev_alarm = copy.deepcopy(main_alarm)
        states.append(prev_alarm)




