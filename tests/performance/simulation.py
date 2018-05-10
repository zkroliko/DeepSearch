import time

from model.Simulation import Simulation
from examples.Scenario2 import Scenario2

start = time.clock()
class App:
    def iteration_finished(self,a,b):
        pass

print(time.clock() - start)


app = App()
sim = Simulation(Scenario2)
sim.start(app)