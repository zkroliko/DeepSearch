import random
import time

from model.Field import Field
from model.LightMap import LightMap
from model.Rectangle import Rectangle

start = time.clock()

for i in range(10000):
    x1, y1 = random.randint(0, 50), random.randint(0, 50)
    x2, y2 = random.randint(0, 50), random.randint(0, 50)
    r = Rectangle(Field(x1,y1),Field(x2,y2))

print("total", time.clock() - start)
