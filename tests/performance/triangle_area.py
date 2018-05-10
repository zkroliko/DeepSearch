import time

from acoAlgorithm.utils.TriangleArea import aprox_triangle_area, triangle_area

triangles = [
    [[0, 0], [5, 0], [0, 5]],
    [[2, 3], [7, 4], [5, 5]],
    [[23, 33], [44, 67], [96, 233]],
    [[0, 200], [3, 5], [5, 233]]
]

start = time.time()

sizes_aprox = {}

for t in triangles:
    sizes_aprox[t.__str__()] = aprox_triangle_area(t[0], t[1], t[2])

for i in range(0, 100000):
    for t in triangles:
        aprox_triangle_area(t[0], t[1], t[2])

end = time.time() - start

print "Aprox time: %s" % end

# --------------- REAL

sizes_real = {}

for t in triangles:
    sizes_real[t.__str__()] = triangle_area(t[0], t[1], t[2])

start = time.time()

for i in range(0, 100000):
    for t in triangles:
        triangle_area(t[0], t[1], t[2])

end = time.time() - start

print "Real time: %s" % end

# Comparison

for t in triangles:
    print "Aprox: %s Real: %s" % (sizes_aprox[t.__str__()],sizes_real[t.__str__()])
