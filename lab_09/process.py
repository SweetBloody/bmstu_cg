from itertools import combinations

X_DOT = 0
Y_DOT = 1


def get_vector(dot1, dot2):
    return [dot2[X_DOT] - dot1[X_DOT], dot2[Y_DOT] - dot1[Y_DOT]]


def vector_mul(vec1, vec2):
    return (vec1[0] * vec2[1] - vec1[1] * vec2[0])


def scalar_mul(vec1, vec2):
    return (vec1[0] * vec2[0] + vec1[1] * vec2[1])


def line_koefs(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1
    return a, b, c


def solve_lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1 * b2 - a2 * b1
    opr1 = (-c1) * b2 - b1 * (-c2)
    opr2 = a1 * (-c2) - (-c1) * a2

    if (opr == 0):
        return -5, -5  # прямые параллельны

    x = opr1 / opr
    y = opr2 / opr

    return x, y


def is_coord_between(left_coord, right_coord, dot_coord):
    return (min(left_coord, right_coord) <= dot_coord) \
           and (max(left_coord, right_coord) >= dot_coord)


def is_dot_between(dot_left, dot_right, dot_intersec):
    return is_coord_between(dot_left[X_DOT], dot_right[X_DOT], dot_intersec[X_DOT]) \
           and is_coord_between(dot_left[Y_DOT], dot_right[Y_DOT], dot_intersec[Y_DOT])


def are_connected_sides(line1, line2):
    if ((line1[0][X_DOT] == line2[0][X_DOT]) and (line1[0][Y_DOT] == line2[0][Y_DOT])) \
            or ((line1[1][X_DOT] == line2[1][X_DOT]) and (line1[1][Y_DOT] == line2[1][Y_DOT])) \
            or ((line1[0][X_DOT] == line2[1][X_DOT]) and (line1[0][Y_DOT] == line2[1][Y_DOT])) \
            or ((line1[1][X_DOT] == line2[0][X_DOT]) and (line1[1][Y_DOT] == line2[0][Y_DOT])):
        return True

    return False


def extra_check(object):  # чтобы не было пересечений

    lines = []

    for i in range(len(object) - 1):
        lines.append([object[i], object[i + 1]])  # разбиваю многоугольник на линии

    combs_lines = list(combinations(lines, 2))  # все возможные комбинации сторон

    for i in range(len(combs_lines)):
        line1 = combs_lines[i][0]
        line2 = combs_lines[i][1]

        if are_connected_sides(line1, line2):
            continue

        a1, b1, c1 = line_koefs(line1[0][X_DOT], line1[0][Y_DOT], line1[1][X_DOT], line1[1][Y_DOT])
        a2, b2, c2 = line_koefs(line2[0][X_DOT], line2[0][Y_DOT], line2[1][X_DOT], line2[1][Y_DOT])

        dot_intersec = solve_lines_intersection(a1, b1, c1, a2, b2, c2)

        if (is_dot_between(line1[0], line1[1], dot_intersec)) \
                and (is_dot_between(line2[0], line2[1], dot_intersec)):
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


def is_visible(dot, f_dot, s_dot):
    vec1 = get_vector(f_dot, s_dot)
    vec2 = get_vector(f_dot, dot)

    if vector_mul(vec1, vec2) <= 0:
        return True
    else:
        return False


def get_lines_parametric_intersec(line1, line2, normal):
    d = get_vector(line1[0], line1[1])
    w = get_vector(line2[0], line1[0])

    d_scalar = scalar_mul(d, normal)
    w_scalar = scalar_mul(w, normal)

    t = -w_scalar / d_scalar

    dot_intersec = [line1[0][X_DOT] + d[0] * t, line1[0][Y_DOT] + d[1] * t]

    return dot_intersec


def sutherland_hodgman_algorythm(cutter_line, position, prev_result):
    cur_result = []

    dot1 = cutter_line[0]
    dot2 = cutter_line[1]

    normal = get_normal(dot1, dot2, position)

    prev_vision = is_visible(prev_result[-2], dot1, dot2)

    for cur_dot_index in range(-1, len(prev_result)):
        cur_vision = is_visible(prev_result[cur_dot_index], dot1, dot2)

        if prev_vision:
            if cur_vision:
                cur_result.append(prev_result[cur_dot_index])
            else:
                figure_line = [prev_result[cur_dot_index - 1], prev_result[cur_dot_index]]

                cur_result.append(get_lines_parametric_intersec(figure_line, cutter_line, normal))
        else:
            if cur_vision:
                figure_line = [prev_result[cur_dot_index - 1], prev_result[cur_dot_index]]

                cur_result.append(get_lines_parametric_intersec(figure_line, cutter_line, normal))

                cur_result.append(prev_result[cur_dot_index])

        prev_vision = cur_vision

    return cur_result


def make_unique(sides):

    for side in sides:
        side.sort()

    return list(filter(lambda x: (sides.count(x) % 2) == 1, sides))


def is_dot_in_side(dot, side):
    if abs(vector_mul(get_vector(dot, side[0]), get_vector(side[1], side[0]))) <= 1e-6:
        if side[0] < dot < side[1] or side[1] < dot < side[0]:
            return True
    return False


def get_sides(side, rest_dots):
    dots_list = [side[0], side[1]]

    for dot in rest_dots:
        if is_dot_in_side(dot, side):
            dots_list.append(dot)

    dots_list.sort()

    sections_list = list()

    for i in range(len(dots_list) - 1):
        sections_list.append([dots_list[i], dots_list[i + 1]])

    return sections_list


def remove_odd_sides(figure_dots):
    all_sides = list()
    rest_dots = figure_dots[2:]

    for i in range(len(figure_dots)):
        cur_side = [figure_dots[i], figure_dots[(i + 1) % len(figure_dots)]]

        all_sides.extend(get_sides(cur_side, rest_dots))

        rest_dots.pop(0)
        rest_dots.append(figure_dots[i])

    return make_unique(all_sides)