from math import sqrt, pi


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Радиус вписанной окружности
def circle_radius(a, b, c):
    p = (a + b + c) / 2
    return sqrt((p - a) * (p - b) * (p - c) / p)


# Площадь круга
def circle_square(a, b, c):
    r = circle_radius(a, b, c)
    return pi * r * r


# Функция нахождения длины отрезка
def length(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Нахождение длин сторон треугольника
def triangle_lengths(point1, point2, point3):
    a = length(point1.x, point1.y, point2.x, point2.y)
    b = length(point2.x, point2.y, point3.x, point3.y)
    c = length(point1.x, point1.y, point3.x, point3.y)
    return a, b, c


# Функция нахождения площади треугольника
def triangle_square(a, b, c):
    p = (a + b + c) / 2
    return sqrt(p * (p - a) * (p - b) * (p - c))


# Проверка треугольника на существование
def triangle_exists(a, b, c):
    eps = 0.00000001
    if a + b > c + eps and a + c > b + eps and b + c > a + eps:
        return 1
    else:
        return 0


# Координаты центра вписанной окружности
def circle_coords(point_1, point_2, point_3):
    a, b, c = triangle_lengths(point_1, point_2, point_3)
    k = c / a
    x1 = (point_3.x + k * point_2.x) / (1 + k)
    y1 = (point_3.y + k * point_2.y) / (1 + k)
    k = b / a
    x2 = (point_3.x + k * point_1.x) / (1 + k)
    y2 = (point_3.y + k * point_1.y) / (1 + k)
    if point_1.x == x1:
        x0 = x1
        k2 = (y2 - point_2.y) / (x2 - point_2.x)
        b2 = (x2 * point_2.y - point_2.x * y2) / (x2 - point_2.x)
        y0 = k2 * x0 + b2
    elif point_2.x == x2:
        x0 = x2
        k1 = (y1 - point_1.y) / (x1 - point_1.x)
        b1 = (x1 * point_1.y - point_1.x * y1) / (x1 - point_1.x)
        y0 = k1 * x0 + b1
    else:
        k1 = (y1 - point_1.y) / (x1 - point_1.x)
        b1 = (x1 * point_1.y - point_1.x * y1) / (x1 - point_1.x)
        k2 = (y2 - point_2.y) / (x2 - point_2.x)
        b2 = (x2 * point_2.y - point_2.x * y2) / (x2 - point_2.x)
        x0 = (b1 - b2) / (k2 - k1)
        y0 = (k2 * b1 - k1 * b2) / (k2 - k1)
    return x0, y0
