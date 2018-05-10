import time

from mock.mock import self

from model.Field import Field
from model.Point import Point
from model.View import ViewGenerator
from examples.Scenario1 import Scenario1

start = time.time()

for i in range(0, 500000):
    Field(3, 3)

end = time.time() - start

print end
