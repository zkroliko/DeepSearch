import sys
import time

import math

from model.LightMap import LightMap
from model.Walker import Walker
from model.decision_makers import randomDecision
from model.tools.Printer import Printer
from examples.Scenario1 import Scenario1

class Simulation:

    DEFAULT_SCENARIO = Scenario1
    DEFAULT_N_ITERATIONS = 400

    DEFAULT_RESULTS_FILE = "iteration_results.csv"
    DEFAULT_OPTIMIZED_FILE = "best_path.csv"


    # Algorithm specific

    def __init__(self,scenario=DEFAULT_SCENARIO,n_iterations=DEFAULT_N_ITERATIONS):
        self.scenario = scenario
        self.n_iterations = n_iterations
        self.iteration = 0
        self.result_file = self.DEFAULT_RESULTS_FILE
        self.path_file = self.DEFAULT_OPTIMIZED_FILE
        self.sh = self.SolutionHolder()

    def get_fields(self):
        printer = Printer(self.scenario.area())
        printer.set_start(self.scenario.start())
        return printer.fields



    def start(self, app):
        # For saving results
        with open(self.result_file, 'w') as result_file:
            print("Building the shadow map")
            # shadow_map = {}
            shadow_map = LightMap.build_shadow_map(self.scenario.area())
            print("Shadow map built")
            for iteration in range(self.n_iterations):
                start = time.time()
                w = Walker(self.scenario.area(), self.scenario.start(), randomDecision.RandomDecision(), shadow_map)
                while not w.finished():
                    w.step()
                length = self.sh.calc_length(w.path)
                # Recording data
                self.sh.propose_solution(w)
                data = "%s, %s" % (length, time.time() - start)
                result_file.write(data + "\n")
                print(data)
                app.iteration_finished(iteration, length)


            printer = Printer(self.scenario.area())
            printer.set_start(self.scenario.start())

            app.result(self)
            print("# Best solution's length is %s" % self.sh.length)
            print("# Best solution is %s" % self.sh.path_to_str())
            print("Iteration progress saved in {}".format(self.result_file))

            with open(self.path_file, 'w') as path_file:
                path_file.write(self.sh.path_to_csv())
                print("Best solution saved in {}".format(self.path_file))


    def best_solution(self):
        return self.sh.path

    class SolutionHolder:
        def __init__(self):
            self.path = None
            self.length = sys.maxsize

        def propose_solution(self, walker):
            new_length = self.calc_length(walker.path)
            if new_length < self.length:
                self.path = walker.path
                self.length = new_length

        def calc_length(self, path):
            # lx, ly = 0, 0
            # len = 0
            # for e in path:
            #     dx, dy = abs(e.x - lx), abs(e.y - ly)
            #     len += 1.4142 if dx + dy > 1 else 1.0
            #     lx, ly = e.x, e.y
            return len(path)

        def path_to_str(self):
            str = ""
            for field in self.path:
                str += field.__str__()
                str += ", "
            return str

        def path_to_csv(self):
            str = ""
            for field in self.path:
                str += "{},{}".format(field.x,field.y)
                str += "\n"
            return str

