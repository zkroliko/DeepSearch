import time

from multiprocessing import freeze_support

from acoAlgorithm.Point import Point
from acoAlgorithm.View import ViewGenerator
from examples.Scenario1 import Scenario1
from examples.Scenario2 import Scenario2
from examples.Scenario3 import Scenario3
from examples.Scenario4 import Scenario4

a = Scenario3.area()

for k in range(1):

    start = time.clock()

    for L in range(1):
        v = ViewGenerator(a)
        for i in range(a.main.start.x,a.main.end.x):
            for j in range(a.main.start.y,a.main.end.y):
                v.shine_from(Point(i,j))
                # print (i,j)

    end = time.clock() - start

    print(end)



