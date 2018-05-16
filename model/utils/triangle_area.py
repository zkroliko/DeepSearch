def aprox_triangle_area(a, b, c):
    min_x = min(a[0], b[0], c[0])
    max_x = max(a[0], b[0], c[0])
    min_y = min(a[1], b[1], c[1])
    max_y = max(a[1], b[1], c[1])

    return abs((max_x - min_x) * (max_y - min_y)) / 2.5


import math


def triangle_area(a, b, c):
    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    side_a = distance(a, b)
    side_b = distance(b, c)
    side_c = distance(c, a)
    s = 0.5 * (side_a + side_b + side_c)
    return math.sqrt(abs(s * (s - side_a) * (s - side_b) * (s - side_c)))
