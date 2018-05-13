import time

from model.field import Field
from model.move import Move

from model.field import Field
from model.rectangle import Rectangle

start = time.time()

r1 = Rectangle(Field(5, 5), Field(8, 8))
r2 = Rectangle(Field(1, 1), Field(6, 6))

for i in range(0, 50000):
    r1 & r2

end = time.time() - start

print end