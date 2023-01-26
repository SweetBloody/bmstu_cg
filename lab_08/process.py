def get_vector(dot1, dot2):
    return [dot2[0] - dot1[0], dot2[1] - dot1[1]]


def vector_mul(vec1, vec2):
    return vec1[0] * vec2[1] - vec1[1] * vec2[0]


def scalar_mul(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def line_koefs(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return a, b, c


def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1 * b2 - a2 * b1
    opr1 = (-c1) * b2 - b1 * (-c2)
    opr2 = a1 * (-c2) - (-c1) * a2

    if opr == 0:
        return -5, -5  # прямые параллельны

    x = opr1 / opr
    y = opr2 / opr

    return x, y

def is_coord_between(left_coord, right_coord, dot_coord):
    return (min(left_coord, right_coord) <= dot_coord) \
           and (max(left_coord, right_coord) >= dot_coord)


def is_dot_between(dot_left, dot_right, dot_intersec):
    return is_coord_between(dot_left[0], dot_right[0], dot_intersec[0]) \
           and is_coord_between(dot_left[1], dot_right[1], dot_intersec[1])


def are_connected_sides(line1, line2):
    if ((line1[0][0] == line2[0][0]) and (line1[0][1] == line2[0][1])) \
            or ((line1[1][0] == line2[1][0]) and (line1[1][1] == line2[1][1])) \
            or ((line1[0][0] == line2[1][0]) and (line1[0][1] == line2[1][1])) \
            or ((line1[1][0] == line2[0][0]) and (line1[1][1] == line2[0][1])):
        return True

    return False


def get_normal(dot1, dot2, pos):
    f_vect = get_vector(dot1, dot2)
    pos_vect = get_vector(dot2, pos)

    if f_vect[1]:
        normal = [1, -f_vect[0] / f_vect[1]]
    else:
        normal = [0, 1]

    if scalar_mul(pos_vect, normal) < 0:
        normal[0] = -normal[0]
        normal[1] = -normal[1]

    return normal

# определить крайний отсекатель для ундо
def find_rectangle(history):
    for i in range(len(history) - 1, -1, -1):
        if history[i][1] == 'rectangle':
            return history[i][0]

    return []


def cross_otr(x1_1, y1_1, x1_2, y1_2, x2_1, y2_1, x2_2, y2_2):
    A1 = y1_1 - y1_2
    B1 = x1_2 - x1_1
    C1 = x1_1 * y1_2 - x1_2 * y1_1
    A2 = y2_1 - y2_2
    B2 = x2_2 - x2_1
    C2 = x2_1 * y2_2 - x2_2 * y2_1

    if B1 * A2 - B2 * A1 and A1:
        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C1 - B1 * y) / A1
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2):
            return True
    elif B1 * A2 - B2 * A1 and A2:
        y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
        x = (-C2 - B2 * y) / A2
        if min(x1_1, x1_2) <= x <= max(x1_1, x1_2):
            return True


def cross_otrs(clipper_coords):
    for i in range(len(clipper_coords) - 3):
        for i in range(i + 1, len(clipper_coords) - 1):
            if cross_otr(clipper_coords[i][0], clipper_coords[i][1],
                         clipper_coords[i + 1][0], clipper_coords[i + 1][1],
                         clipper_coords[i + 1][0], clipper_coords[i + 1][1],
                         clipper_coords[i + 2][0], clipper_coords[i + 2][1]) == True:
                return True
    return False

