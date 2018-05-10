import time

import acoAlgorithm.utils.TriangleRasterization as tr
import numpy as np

start = time.time()


for i in range(0, 10000):
    triangleA = np.array([[0,0],[45,0],[0,5]])
    tr.rasterize_triangle(triangleA)

end = time.time() - start

print end