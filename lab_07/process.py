def get_dot_bits(clipper, dot):
    bits = 0b0000

    if dot[0] < clipper[0]:
        bits += 0b0001

    if dot[0] > clipper[1]:
        bits += 0b0010

    if dot[1] < clipper[2]:
        bits += 0b0100

    if dot[1] > clipper[3]:
        bits += 0b1000

    return bits


def check_visible(dot1_bits, dot2_bits):
    vision = 0  # частично видимый
    if dot1_bits == 0 and dot2_bits == 0:
        vision = 1  # видим
    elif dot1_bits & dot2_bits:
        vision = -1  # не видим

    return vision


def get_bit(dot_bits, i):
    return (dot_bits >> i) & 1


def are_bits_equal(dot1_bits, dot2_bits, i):
    if get_bit(dot1_bits, i) == get_bit(dot2_bits, i):
        return True

    return False

# определить крайний отсекатель для undo
def find_rectangle(history):
    for i in range(len(history) - 1, -1, -1):
        if history[i][2] == 'rectangle':
            return history[0:2]

    return []