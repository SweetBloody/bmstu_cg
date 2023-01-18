can_width = 1080
can_height = 720

def sign(diff):
    if diff < 0:
        return -1
    elif diff == 0:
        return 0
    else:
        return 1

# коэффициенты прямой
def line_koefs(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return a, b, c

# точка пересечения прямых
def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1 * b2 - a2 * b1
    opr1 = (-c1) * b2 - b1 * (-c2)
    opr2 = a1 * (-c2) - (-c1) * a2

    x = opr1 / opr
    y = opr2 / opr

    return x, y

# определение границ исследуемой области
def get_edges(dots):
    x_max = 0
    x_min = can_width

    y_max = can_height
    y_min = 0

    for figure in dots:
        for dot in figure:
            if dot[0] > x_max:
                x_max = dot[0]

            if dot[0] < x_min:
                x_min = dot[0]

            if dot[1] < y_max:
                y_max = dot[1]

            if dot[1] > y_min:
                y_min = dot[1]

    block_edges = (x_min, y_min, x_max, y_max)

    return block_edges

# метод брезенхема для построения отрезка
def bresenham_int(p1, p2, color, step_count=False):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        return [[x1, y1, color]]

    x = x1
    y = y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    s1 = sign(x2 - x1)
    s2 = sign(y2 - y1)

    swaped = 0
    if dy > dx:
        tmp = dx
        dx = dy
        dy = tmp
        swaped = 1

    e = 2 * dy - dx
    i = 1
    dots = []
    steps = 0

    while i <= dx + 1:
        dot = [x, y, color]
        dots.append(dot)

        x_buf = x
        y_buf = y

        while e > 0:
            if swaped:
                x = x + s1
            else:
                y = y + s2

            e = e - 2 * dx

        if swaped:
            y = y + s2
        else:
            x = x + s1

        e = e + 2 * dy

        if step_count:
            if (x_buf != x) and (y_buf != y):
                steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return dots