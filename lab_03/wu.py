from porcess import sign, get_rgb_intensivity
from math import fabs, ceil, radians, cos, sin, floor


def test_vu(ps, pf):
    x1 = ps[0]
    x2 = pf[0]
    y1 = ps[1]
    y2 = pf[1]
    I = 100
    stairs = []
    if x1 == x2 and y1 == y2:
        flag = 1

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
    ypx1 = int(yend)
    y = yend + tg

    xend = int(x2 + 0.5)
    yend = y2 + tg * (xend - x2)
    xpx2 = xend

    if steep:
        for x in range(xpx1, xpx2):

            y += tg
    else:
        for x in range(xpx1, xpx2):
            y += tg

def draw_line_vu(canvas, ps, pf, fill):
    x1 = ps[0]
    x2 = pf[0]
    y1 = ps[1]
    y2 = pf[1]
    I = 100
    stairs = []
    fills = get_rgb_intensivity(canvas, fill, "white", I)
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
                               fill = fills[round((I - 1) * (abs(1 - y + floor(y))))])
            canvas.create_line(x + 1, int(y) + 1, x + 2, int(y) + 2,
                               fill = fills[round((I - 1) * (abs(y - floor(y))))])

            if (abs(int(x) - int(x + 1)) >= 1 and tg > 1) or \
                    (not 1 > abs(int(y) - int(y + tg)) >= tg):
                stairs.append(st)
                st = 0
            else:
                st += 1
            y += tg
    return stairs
