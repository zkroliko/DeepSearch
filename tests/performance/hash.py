import time

from model.field import Field
from model.move import Move

start = time.time()

f = Move(Field(4, 4), Field(5, 5))

for i in range(0, 1000000):
    f.__hash__()

end = time.time() - start

print end

