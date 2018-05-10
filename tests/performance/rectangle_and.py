import time

from acoAlgorithm.Field import Field
from acoAlgorithm.Move import Move

from acoAlgorithm.Field import Field
from acoAlgorithm.Rectangle import Rectangle

start = time.time()

r1 = Rectangle(Field(5, 5), Field(8, 8))
r2 = Rectangle(Field(1, 1), Field(6, 6))

for i in range(0, 50000):
    r1 & r2

end = time.time() - start

print end