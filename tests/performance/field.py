import time

from mock.mock import self

from acoAlgorithm.Field import Field
from acoAlgorithm.Point import Point
from acoAlgorithm.View import ViewGenerator
from examples.Scenario1 import Scenario1

start = time.time()

for i in range(0, 500000):
    Field(3, 3)

end = time.time() - start

print end
