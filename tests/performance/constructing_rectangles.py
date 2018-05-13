import random
import time

from model.field import Field
from model.lightMap import LightMap
from model.rectangle import Rectangle

start = time.clock()

for i in range(10000):
    x1, y1 = random.randint(0, 50), random.randint(0, 50)
    x2, y2 = random.randint(0, 50), random.randint(0, 50)
    r = Rectangle(Field(x1,y1),Field(x2,y2))

print("total", time.clock() - start)
