from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from tkinter.ttk import Treeview
from process import *

points = []
c_width = 640
c_height = 540
k_scale = 1.1

task_text = 'На плоскости дано\nмножество точек.\n' \
            'Найти такой треугольник с\nвершинами в этих точках,\n' \
            'у которого разность площадей\nтреугольника и вписанной\n' \
            'окружности (круга) минимальна.'


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Лаб. раб. №1")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2 - 455
        height = height // 2 - 420
        self.geometry('910x770+{}+{}'.format(width, height))
        self.resizable(width=False, height=False)
        self.config(bg="#ccc")
        helv10 = tkFont.Font(family='Helvetica', size=10)
        helv12 = tkFont.Font(family='Helvetica', size=12, weight=tkFont.BOLD)
        helv14 = tkFont.Font(family='Helvetica', size=14)
        helv16 = tkFont.Font(family='Helvetica', size=16)

        # Таблица координат точек
        self.table = Treeview(self, show="headings", columns=("#1", "#2", "#3"), height=26)
        self.table.column("#1", width=78)
        self.table.column("#2", width=78)
        self.table.column("#3", width=78)
        self.table.heading("#1", text="№")
        self.table.heading("#2", text="X")
        self.table.heading("#3", text="Y")
        self.table.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.table.bind('<<TreeviewSelect>>', self.select_point)

        # Графический результат
        self.canvas = Canvas(self, width=c_width, height=c_height, bg='white')
        self.canvas.grid(row=0, column=2)
        self.canvas_clear()

        # Ввод координат
        self.txt_x = Label(self, width=5, height=1, font=helv12, bg='#ccc', text='X:')
        self.txt_x.grid(row=1, column=0)

        self.txt_y = Label(self, width=5, height=1, font=helv12, bg='#ccc', text='Y:')
        self.txt_y.grid(row=1, column=1)

        self.point_x = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.point_x.grid(row=2, column=0)

        self.point_y = Entry(self, font=helv14, width=9, justify=RIGHT)
        self.point_y.grid(row=2, column=1)

        # Кнопки
        self.btn_addPoint = Button(self, text="Добавить точку", font=helv10, width=22, height=2, command=self.add_point)
        self.btn_addPoint.grid(row=3, column=0, columnspan=2)

        self.btn_changePoint = Button(self, text="Изменить", font=helv10, width=11, height=1, command=self.change_point)
        self.btn_changePoint.grid(row=4, column=0)

        self.btn_deletePoint = Button(self, text="Удалить", font=helv10, width=11, height=1, command=self.delete_point)
        self.btn_deletePoint.grid(row=4, column=1)

        self.bind('<Return>', self.press_enter)
        self.bind('<Delete>', self.press_delete)

        # Текстовый ответ
        self.text = Label(self, width=53, height=8, font=helv16, justify=LEFT, text='...', bg='#efefee')
        self.text.grid(row=1, column=2, rowspan=4)

        # Окно с задачей
        self.task = tk.Tk()
        self.task.title("Задание")
        self.task.resizable(width=False, height=False)
        width_t = width - 320
        height_t = height + 260
        self.task.geometry('320x250+{}+{}'.format(width_t, height_t))
        self.task_text = Label(self.task, width=40, height=10, font=helv16, justify=CENTER, text=task_text, bg='#efefee')
        self.task_text.pack()
        self.task.mainloop()

    # Кнопка добавления точки
    def add_point(self):
        try:
            x = float(self.point_x.get())
            y = float(self.point_y.get())
            points.append(Point(x, y))
            self.table.insert("", END, values=(len(points), x, y))
            self.point_x.delete(0, END)
            self.point_y.delete(0, END)

            self.print_array()
            self.process()
        except Exception as exception:
            print(exception)
            self.point_x.delete(0, END)
            self.point_y.delete(0, END)
            messagebox.showerror('Ошибка добавления', 'Неверный ввод!')

    # Добавление точки по нажатию на Enter
    def press_enter(self, event):
        if not self.table.selection():
            self.add_point()
        else:
            self.change_point()

    # Выбор точки в таблице
    def select_point(self, event):
        self.point_x.delete(0, END)
        self.point_x.insert(0, self.table.item(self.table.selection()[0], option='values')[1])
        self.point_y.delete(0, END)
        self.point_y.insert(0, self.table.item(self.table.selection()[0], option='values')[2])

    # Кнопка изменения точки
    def change_point(self):
        try:
            index = int(self.table.item(self.table.selection()[0], option='values')[0])
            x = float(self.point_x.get())
            y = float(self.point_y.get())
            self.table.delete(self.table.selection()[0])
            self.table.insert("", index - 1, values=(index, x, y))
            points[index - 1] = Point(x, y)
            self.point_x.delete(0, END)
            self.point_y.delete(0, END)

            self.print_array()
            self.process()
        except Exception as exception:
            print(exception)
            messagebox.showerror('Ошибка исправления', 'Выберите точку в списке!')

    # Кнопка удаления точки
    def delete_point(self):
        try:
            index = int(self.table.item(self.table.selection()[0], option='values')[0])
            item = self.table.next(self.table.selection()[0])
            self.table.delete(self.table.selection()[0])
            points.pop(index - 1)
            for i in range(index - 1, len(points)):
                values = self.table.item(item, option='values')
                next = self.table.next(item)
                self.table.delete(item)
                self.table.insert("", i, values=(i + 1, values[1], values[2]))
                item = next

            self.print_array()
            self.process()
        except Exception as exception:
            print(exception)
            if str(exception) == "pop from empty list":
                messagebox.showerror('Ошибка удаления', 'Список пуст!')
            elif str(exception) == 'tuple index out of range':
                messagebox.showerror('Ошибка удаления', 'Выберите точку в списке!')

    # Удаление точки по нажатию Delete
    def press_delete(self, event):
        self.delete_point()

    # Нахождение треугольника с минимальной разностью площадей между треуг и вписанной окр
    def process(self):
        min_diff = 0
        if len(points) > 2:
            a, b, c = triangle_lengths(points[0], points[1], points[2])
            if triangle_exists(a, b, c) == 1:
                min_diff = triangle_square(a, b, c) - circle_square(a, b, c)
            res_points = [0, 1, 2]
            for i in range(len(points) - 2):
                for j in range(i + 1, len(points) - 1):
                    for k in range(j + 1, len(points)):
                        a, b, c = triangle_lengths(points[i], points[j], points[k])
                        if triangle_exists(a, b, c) == 1:
                            diff = triangle_square(a, b, c) - circle_square(a, b, c)
                            if diff < min_diff and diff != 0:
                                min_diff = diff
                                res_points = [i, j, k]
                            elif min_diff == 0:
                                min_diff = diff
                                res_points = [i, j, k]
            if min_diff == 0:
                self.text.config(text='Данные точки не могут образовать треугольник,\n'
                                      'так как они лежат на одной прямой или\nсовпадают')
                self.canvas_clear()
            else:
                a, b, c = triangle_lengths(points[res_points[0]], points[res_points[1]], points[res_points[2]])
                tr_S = triangle_square(a, b, c)
                cir_S = circle_square(a, b, c)
                self.text.config(text='Треугольник образован точками:'
                                      '\n№{0}. x = {1}, y = {2};\n№{3}. x = {4}, y = {5};\n№{6}. x = {7}, y = {8};\n'
                                      'Площадь треугольника = {9:.6}\nПлощадь вписанной окружности (круга) = {10:.6}\n'
                                      'Разность площадей = {11:.6}\n'
                                 .format(res_points[0] + 1, points[res_points[0]].x, points[res_points[0]].y,
                                         res_points[1] + 1, points[res_points[1]].x, points[res_points[1]].y,
                                         res_points[2] + 1, points[res_points[2]].x, points[res_points[2]].y,
                                         tr_S, cir_S, tr_S - cir_S))
                self.draw_result(res_points[0], res_points[1], res_points[2])
        else:
            self.text.config(text='Недостаточно точек!')
            self.canvas_clear()

    # Очистка canvas
    def canvas_clear(self):
        self.canvas.delete('all')
        # self.canvas.create_line(5, c_height - 5, 5, c_height - 35, width=2, arrow=LAST)
        # self.canvas.create_line(5, c_height - 5, 35, c_height - 5, width=2, arrow=LAST)

    # Автоматическое масштабирование изображения
    def auto_scaling(self, point_1, point_2, point_3):
        x1, y1 = point_1.x, point_1.y
        x2, y2 = point_2.x, point_2.y
        x3, y3 = point_3.x, point_3.y
        delta = 40
        while c_width - delta > max(x1, x2, x3) - min(x1, x2, x3) and \
                c_height - delta > max(y1, y2, y3) - min(y1, y2, y3):
            x1 *= k_scale
            y1 *= k_scale
            x2 *= k_scale
            y2 *= k_scale
            x3 *= k_scale
            y3 *= k_scale
        while c_width - delta < max(x1, x2, x3) - min(x1, x2, x3) or \
                c_height - delta < max(y1, y2, y3) - min(y1, y2, y3):
            x1 /= k_scale
            y1 /= k_scale
            x2 /= k_scale
            y2 /= k_scale
            x3 /= k_scale
            y3 /= k_scale

        min_x = min(x1, x2, x3)
        min_y = min(y1, y2, y3)

        x1 -= min_x - 20
        x2 -= min_x - 20
        x3 -= min_x - 20
        y1 -= min_y - 20
        y2 -= min_y - 20
        y3 -= min_y - 20

        point_1.x, point_1.y = x1, y1
        point_2.x, point_2.y = x2, y2
        point_3.x, point_3.y = x3, y3
        return point_1, point_2, point_3

    # Изменение системы координат
    def change_coords(self, point_1, point_2, point_3):
        point_1.y = c_height - 5 - point_1.y
        point_2.y = c_height - 5 - point_2.y
        point_3.y = c_height - 5 - point_3.y

        point_1.x += 5
        point_2.x += 5
        point_3.x += 5
        return point_1, point_2, point_3

    # Отрисовка надписей
    def draw_sign(self, x0, y0, x, y):
        delta = 5
        if x > x0 and y > y0:
            return delta, delta
        elif x < x0 and y > y0:
            return -delta, delta
        elif x < x0 and y < y0:
            return -delta, -delta
        elif x > x0 and y < y0:
            return delta, -delta

    # Отрисовка результатов
    def draw_result(self, i, j, k):
        self.canvas_clear()

        point_1 = Point(points[i].x, points[i].y)
        point_2 = Point(points[j].x, points[j].y)
        point_3 = Point(points[k].x, points[k].y)

        point_1, point_2, point_3 = self.auto_scaling(point_1, point_2, point_3)
        point_1, point_2, point_3 = self.change_coords(point_1, point_2, point_3)

        # Длины сторон треугольника
        a, b, c = triangle_lengths(point_1, point_2, point_3)

        # Центр и радиус вписанной окружности
        x0, y0 = circle_coords(point_1, point_2, point_3)
        r = circle_radius(a, b, c)

        self.canvas.create_polygon([point_1.x, point_1.y, point_2.x, point_2.y, point_3.x, point_3.y],
                                   outline='blue', fill='white')
        self.canvas.create_oval(x0 - r, y0 - r, x0 + r, y0 + r, outline='red', fill='white')

        # Отрисовка точек и надписей
        r = 2
        dx, dy = self.draw_sign(x0, y0, point_1.x, point_1.y)
        self.canvas.create_oval(point_1.x - r, point_1.y + r, point_1.x + r, point_1.y - r, outline='red', fill='red')
        self.canvas.create_text(point_1.x + dx, point_1.y + dy, text=str(i + 1))

        dx, dy = self.draw_sign(x0, y0, point_2.x, point_2.y)
        self.canvas.create_oval(point_2.x - r, point_2.y + r, point_2.x + r, point_2.y - r, outline='red', fill='red')
        self.canvas.create_text(point_2.x + dx, point_2.y + dy, text=str(j + 1))

        dx, dy = self.draw_sign(x0, y0, point_3.x, point_3.y)
        self.canvas.create_oval(point_3.x - r, point_3.y + r, point_3.x + r, point_3.y - r, outline='red', fill='red')
        self.canvas.create_text(point_3.x + dx, point_3.y + dy, text=str(k + 1))

    def print_array(self):
        print('Array:')
        for point in points:
            print('x = {0}, y = {1}'.format(point.x, point.y))
