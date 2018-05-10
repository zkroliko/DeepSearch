import random
import time

from acoAlgorithm.Field import Field
from acoAlgorithm.Move import Move

start = time.clock()

def build_move():
    x, y = random.randint(1, 50), random.randint(1, 50)
    dx, dy = random.randint(-1, 1), random.randint(-1, 1)
    return Move(Field(x,y),Field(x+dx,y+dy))

for i in range(1000):
    m1 = build_move()
    for j in range(100):
        m2 = build_move()
        if m1 == m2:
            pass

print("total", time.clock() - start)