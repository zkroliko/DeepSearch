from collections import Set

from acoAlgorithm.Rectangle import Rectangle
from acoAlgorithm.Field import Field


def load_from_file(filename, area, symbol):
    f = open(filename, 'r')

    dimension = area.height()

    # Primary loading, will load simple 1xn rectangles
    j = 0
    i = 0
    # Ugly imperative programming
    while j <= i:
        start = None
        newline = False
        i = 0
        r = f.read(1)
        while i < dimension and len(r) > 0 and not newline:
            if r == symbol:
                if start is None:
                    start = i
            elif start is not None:
                if i - start > 0:
                    area += Rectangle(Field(start, j), Field(i - 1, j))
                    start = None
            if r == '\n':
                newline = True
            else:
                r = f.read(1)
                i += 1
        j += 1

    optimize_area(area)


def optimize_area(area):
    queue = list(area.all_rectangles())
    if len(queue) > 1:
        tries = 0
        while len(queue) > 1 and tries < len(queue):
            r = queue.pop(0)
            if len(area.get_root().rectangles_in_contact(r.confine())) > 1:
                candidates = area.get_root().rectangles_in_contact(r.confine())
                if len(candidates) > 0:
                    candidates.remove(r)
                    c = candidates.pop()
                    if r.is_joinable(c):
                        result = r.join(c)
                        queue.remove(c)
                        queue.append(result)
                        tries = 0
                    else:
                        queue.append(r)
                        tries += 1
                else:
                    tries -= 1


def sum_n(number):
    acc = 1
    for i in range(2, number):
        acc += i
    return acc
