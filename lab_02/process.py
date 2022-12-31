from math import sin, cos, radians, sqrt
import copy


can_width = 1090
can_height = 720
coord_x = can_width // 2
coord_y = can_height // 2


class Alarm(object):
    def __init__(self, center_x, center_y):
        # Центр будильника
        self.center_x = center_x
        self.center_y = center_y

        # Параметры будильника
        self.alarm_radius_x = 50
        self.alarm_radius_y = 50
        self.alarm_dt = 0
        self.num_points = 720
        self.alarm_points = list([0, 0] for i in range(self.num_points))

        # Отметки на часах (3, 6, 9, 12 часов)
        self.hours = [[self.center_x, self.center_y + self.alarm_radius_y, self.center_x, self.center_y + self.alarm_radius_y * 0.75],
                      [self.center_x + self.alarm_radius_x, self.center_y, self.center_x + self.alarm_radius_x * 0.75, self.center_y],
                      [self.center_x, self.center_y - self.alarm_radius_y, self.center_x, self.center_y - self.alarm_radius_y * 0.75],
                      [self.center_x - self.alarm_radius_x, self.center_y, self.center_x - self.alarm_radius_x * 0.75, self.center_y]]

        # Стрелки часов
        self.arrows = [[self.center_x, self.center_y, self.center_x, self.center_y + self.alarm_radius_y * 0.5],
                       [self.center_x, self.center_y, self.center_x + self.alarm_radius_x * 0.4, self.center_y]]

        # Ножки будильника
        self.legs = [[self.center_x - self.alarm_radius_x * sin(radians(25)),
                      self.center_y - self.alarm_radius_y * cos(radians(25)),
                      self.center_x - self.alarm_radius_x * 1.5 * sin(radians(25)),
                      self.center_y - self.alarm_radius_y * 1.5 * cos(radians(25))],
                     [self.center_x + self.alarm_radius_x * sin(radians(25)),
                      self.center_y - self.alarm_radius_y * cos(radians(25)),
                      self.center_x + self.alarm_radius_x * 1.5 * sin(radians(25)),
                      self.center_y - self.alarm_radius_y * 1.5 * cos(radians(25))]]

        # Звонок будильника
        self.arc_a = self.alarm_radius_x
        self.arc_b = self.alarm_radius_y * 0.75
        self.bottom_arc_dy = self.alarm_radius_y * 0.4
        self.top_arc_dy = self.alarm_radius_y * 0.6
        self.bottom_arc = list([0, 0] for i in range(161))
        self.top_arc = list([0, 0] for i in range(161))
        self.parts = [[self.arc_a * cos(radians(50)) + self.center_x,
                       self.arc_b * sin(radians(50)) + self.center_y + self.bottom_arc_dy,
                       self.arc_a * cos(radians(50)) + self.center_x,
                       self.arc_b * sin(radians(50)) + self.center_y + self.top_arc_dy],
                      [self.arc_a * cos(radians(130)) + self.center_x,
                       self.arc_b * sin(radians(130)) + self.center_y + self.bottom_arc_dy,
                       self.arc_a * cos(radians(130)) + self.center_x,
                       self.arc_b * sin(radians(130)) + self.center_y + self.top_arc_dy]]

        self.bell_radius_x = self.alarm_radius_x * 0.2
        self.bell_radius_y = self.alarm_radius_y * 0.2
        self.bell_points = list([0, 0] for i in range(self.num_points))

        self.alarm_create()
        self.arc_create()

    # Массив точек циферблата будильника
    def alarm_create(self):
        t = 0
        step = 0.5
        for i in range(self.num_points):
            x = self.alarm_radius_x * cos(radians(t)) + self.center_x
            y = self.alarm_radius_y * sin(radians(t)) + self.center_y
            self.alarm_points[i][0] = x
            self.alarm_points[i][1] = y
            x = self.bell_radius_x * cos(radians(t)) + self.center_x
            y = self.bell_radius_y * sin(radians(t)) + self.center_y +\
                  self.top_arc_dy + self.arc_b + self.bell_radius_y
            self.bell_points[i][0] = x
            self.bell_points[i][1] = y
            t += step

    # Массив точек для звонка будильника
    def arc_create(self):
        t = 0
        for i in range(161):
            x = self.arc_a * cos(radians(t + 50)) + self.center_x
            y1 = self.arc_b * sin(radians(t + 50)) + self.center_y + self.bottom_arc_dy
            y2 = self.arc_b * sin(radians(t + 50)) + self.center_y + self.top_arc_dy
            self.bottom_arc[i][0] = x
            self.bottom_arc[i][1] = y1
            self.top_arc[i][0] = x
            self.top_arc[i][1] = y2
            t += 0.5


# Изменение абсцисс
def change_x(x):
    return coord_x + x


# Изменение ординат
def change_y(y):
    return can_height - coord_y - y


# Параметры эллипса
def ellipse_param(a, b):
    e = sqrt(1 - (b * b) / (a * a))
    print(e)
    p = b * b / a
    return e, p


# Уравнение эллипса в полярных координатах
def polar_ellipse(a, b, t):
    e = sqrt(1 - (b * b) / (a * a))
    p = b * b / a
    return p / (1 - e * cos(t))


# Перемещение координаты
def move(c, ds):
    return c + ds


# Изменение координат для перемещения
def coord_change_move(alarm, dx, dy):
    temp_alarm = copy.deepcopy(alarm)
    temp_alarm.center_x = move(alarm.center_x, dx)
    temp_alarm.center_y = move(alarm.center_y, dy)

    for i in range(4):
        temp_alarm.hours[i][0] = move(alarm.hours[i][0], dx)
        temp_alarm.hours[i][1] = move(alarm.hours[i][1], dy)
        temp_alarm.hours[i][2] = move(alarm.hours[i][2], dx)
        temp_alarm.hours[i][3] = move(alarm.hours[i][3], dy)

    for i in range(2):
        temp_alarm.arrows[i][0] = move(alarm.arrows[i][0], dx)
        temp_alarm.arrows[i][1] = move(alarm.arrows[i][1], dy)
        temp_alarm.arrows[i][2] = move(alarm.arrows[i][2], dx)
        temp_alarm.arrows[i][3] = move(alarm.arrows[i][3], dy)
        temp_alarm.legs[i][0] = move(alarm.legs[i][0], dx)
        temp_alarm.legs[i][1] = move(alarm.legs[i][1], dy)
        temp_alarm.legs[i][2] = move(alarm.legs[i][2], dx)
        temp_alarm.legs[i][3] = move(alarm.legs[i][3], dy)
        temp_alarm.parts[i][0] = move(alarm.parts[i][0], dx)
        temp_alarm.parts[i][1] = move(alarm.parts[i][1], dy)
        temp_alarm.parts[i][2] = move(alarm.parts[i][2], dx)
        temp_alarm.parts[i][3] = move(alarm.parts[i][3], dy)

    for i in range(alarm.num_points):
        temp_alarm.alarm_points[i][0] = move(alarm.alarm_points[i][0], dx)
        temp_alarm.alarm_points[i][1] = move(alarm.alarm_points[i][1], dy)
        temp_alarm.bell_points[i][0] = move(alarm.bell_points[i][0], dx)
        temp_alarm.bell_points[i][1] = move(alarm.bell_points[i][1], dy)

    for i in range(161):
        temp_alarm.bottom_arc[i][0] = move(alarm.bottom_arc[i][0], dx)
        temp_alarm.bottom_arc[i][1] = move(alarm.bottom_arc[i][1], dy)
        temp_alarm.top_arc[i][0] = move(alarm.top_arc[i][0], dx)
        temp_alarm.top_arc[i][1] = move(alarm.top_arc[i][1], dy)
    return temp_alarm


# Масштабирование x
def scale_x(x, xc, kx):
    return xc + kx * (x - xc)


# Масштабирование y
def scale_y(y, yc, ky):
    return yc + ky * (y - yc)


# Изменение координат для масштабирования
def coord_change_scale(alarm, xc, yc, kx, ky):
    temp_alarm = copy.deepcopy(alarm)
    temp_alarm.center_x = scale_x(alarm.center_x, xc, kx)
    temp_alarm.center_y = scale_y(alarm.center_y, yc, ky)

    for i in range(4):
        temp_alarm.hours[i][0] = scale_x(alarm.hours[i][0], xc, kx)
        temp_alarm.hours[i][1] = scale_y(alarm.hours[i][1], yc, ky)
        temp_alarm.hours[i][2] = scale_x(alarm.hours[i][2], xc, kx)
        temp_alarm.hours[i][3] = scale_y(alarm.hours[i][3], yc, ky)

    for i in range(2):
        temp_alarm.arrows[i][0] = scale_x(alarm.arrows[i][0], xc, kx)
        temp_alarm.arrows[i][1] = scale_y(alarm.arrows[i][1], yc, ky)
        temp_alarm.arrows[i][2] = scale_x(alarm.arrows[i][2], xc, kx)
        temp_alarm.arrows[i][3] = scale_y(alarm.arrows[i][3], yc, ky)
        temp_alarm.legs[i][0] = scale_x(alarm.legs[i][0], xc, kx)
        temp_alarm.legs[i][1] = scale_y(alarm.legs[i][1], yc, ky)
        temp_alarm.legs[i][2] = scale_x(alarm.legs[i][2], xc, kx)
        temp_alarm.legs[i][3] = scale_y(alarm.legs[i][3], yc, ky)
        temp_alarm.parts[i][0] = scale_x(alarm.parts[i][0], xc, kx)
        temp_alarm.parts[i][1] = scale_y(alarm.parts[i][1], yc, ky)
        temp_alarm.parts[i][2] = scale_x(alarm.parts[i][2], xc, kx)
        temp_alarm.parts[i][3] = scale_y(alarm.parts[i][3], yc, ky)

    for i in range(alarm.num_points):
        temp_alarm.alarm_points[i][0] = scale_x(alarm.alarm_points[i][0], xc, kx)
        temp_alarm.alarm_points[i][1] = scale_y(alarm.alarm_points[i][1], yc, ky)
        temp_alarm.bell_points[i][0] = scale_x(alarm.bell_points[i][0], xc, kx)
        temp_alarm.bell_points[i][1] = scale_y(alarm.bell_points[i][1], yc, ky)

    for i in range(161):
        temp_alarm.bottom_arc[i][0] = scale_x(alarm.bottom_arc[i][0], xc, kx)
        temp_alarm.bottom_arc[i][1] = scale_y(alarm.bottom_arc[i][1], yc, ky)
        temp_alarm.top_arc[i][0] = scale_x(alarm.top_arc[i][0], xc, kx)
        temp_alarm.top_arc[i][1] = scale_x(alarm.top_arc[i][1], yc, ky)

    temp_alarm.alarm_radius_x *= kx
    temp_alarm.alarm_radius_y *= ky
    temp_alarm.bell_radius_x *= kx
    temp_alarm.bell_radius_y *= ky

    temp_alarm.arc_a *= kx
    temp_alarm.arc_b *= ky
    temp_alarm.bottom_arc_dy *= ky
    temp_alarm.top_arc_dy *= ky

    return temp_alarm


# Поворот координат
def rotate_coord(x, y, xc, yc, t):
    x1 = xc + (x - xc) * cos(radians(t)) - (y - yc) * sin(radians(t))
    y1 = yc + (x - xc) * sin(radians(t)) + (y - yc) * cos(radians(t))
    return x1, y1


# Изменение координат для поворота
def coord_change_rotate(alarm, xc, yc, t):
    temp_alarm = copy.deepcopy(alarm)
    temp_alarm.center_x, temp_alarm.center_y = rotate_coord(alarm.center_x,
                                                            alarm.center_y,
                                                            xc, yc, t)

    for i in range(4):
        temp_alarm.hours[i][0], temp_alarm.hours[i][1] = rotate_coord(alarm.hours[i][0],
                                                                      alarm.hours[i][1],
                                                                      xc, yc, t)
        temp_alarm.hours[i][2], temp_alarm.hours[i][3] = rotate_coord(alarm.hours[i][2],
                                                                      alarm.hours[i][3],
                                                                      xc, yc, t)

    for i in range(2):
        temp_alarm.arrows[i][0], temp_alarm.arrows[i][1] = rotate_coord(alarm.arrows[i][0],
                                                                        alarm.arrows[i][1],
                                                                        xc, yc, t)
        temp_alarm.arrows[i][2], temp_alarm.arrows[i][3] = rotate_coord(alarm.arrows[i][2],
                                                                        alarm.arrows[i][3],
                                                                        xc, yc, t)
        temp_alarm.legs[i][0], temp_alarm.legs[i][1] = rotate_coord(alarm.legs[i][0],
                                                                    alarm.legs[i][1],
                                                                    xc, yc, t)
        temp_alarm.legs[i][2], temp_alarm.legs[i][3] = rotate_coord(alarm.legs[i][2],
                                                                    alarm.legs[i][3],
                                                                    xc, yc, t)
        temp_alarm.parts[i][0], temp_alarm.parts[i][1] = rotate_coord(alarm.parts[i][0],
                                                                      alarm.parts[i][1],
                                                                      xc, yc, t)
        temp_alarm.parts[i][2], temp_alarm.parts[i][3] = rotate_coord(alarm.parts[i][2],
                                                                      alarm.parts[i][3],
                                                                      xc, yc, t)

    for i in range(alarm.num_points):
        temp_alarm.alarm_points[i][0], temp_alarm.alarm_points[i][1] = rotate_coord(alarm.alarm_points[i][0],
                                                                                    alarm.alarm_points[i][1],
                                                                                    xc, yc, t)
        temp_alarm.bell_points[i][0], temp_alarm.bell_points[i][1] = rotate_coord(alarm.bell_points[i][0],
                                                                                  alarm.bell_points[i][1],
                                                                                  xc, yc, t)

    for i in range(161):
        temp_alarm.bottom_arc[i][0], temp_alarm.bottom_arc[i][1] = rotate_coord(alarm.bottom_arc[i][0],
                                                                                alarm.bottom_arc[i][1],
                                                                                xc, yc, t)
        temp_alarm.top_arc[i][0], temp_alarm.top_arc[i][1] = rotate_coord(alarm.top_arc[i][0],
                                                                          alarm.top_arc[i][1],
                                                                          xc, yc, t)
    return temp_alarm
