import sys
import time
from threading import Thread

import _thread
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.settings import SettingsWithTabbedPanel

from model.simulation import Simulation
from model.walker import Walker
from model.tools.Printer import Printer
from examples.Scenario1 import Scenario1
from examples.Scenario2 import Scenario2
from examples.Scenario3 import Scenario3
from examples.Scenario4 import Scenario4

kivy.require('1.10.0')  # replace with your current kivy version !

window_size = Window.size
settings_height = 40


class Map(Widget):
    EMPTY = ' '
    OCCUPIED = 'x'
    VISIBLE = '.'
    START = 'S'
    OWN = '0'
    ENEMY_1 = '1'
    ENEMY_2 = '2'
    ENEMY_3 = '3'

    colors = {
        EMPTY: (1, 1, 1),
        OCCUPIED: (0, 0, 0),
        VISIBLE: (1, 0.945, 0.008),
        START: (0, 1, 0),
        OWN: (1, 0, 0),
        ENEMY_1: (0.900, 0.300, 0.900),
        ENEMY_2: (0.800, 0.800, 0.200),
        ENEMY_3: (0.350, 0.950, 0.930)
    }

    fields = []

    def set_fields(self, fields):
        self.fields = fields

    def draw(self):
        with self.canvas:
            for i in range(len(self.fields)):
                for j in range(len(self.fields[i])):
                    self.draw_field(i, j)

    def clear(self):
        for i in range(len(self.fields)):
            for j in range(len(self.fields[i])):
                    if self.fields[i][j] not in [" ", "x"]:
                        self.fields[i][j] = " "
        self.draw()


    def draw_field(self, i, j):
        # Picking color
        c = self.colors[self.fields[i][j]]
        Color(c[0], c[1], c[2])

        qnt_x = len(self.fields[0])
        qnt_y = len(self.fields)
        win_w = float(window_size[0])
        win_h = float(window_size[1] - settings_height)
        if qnt_x > qnt_y:
            size = (win_w / qnt_x)
            center = (win_h - (size * qnt_y)) / 2
            Rectangle(pos=(j * size, (self.get_top() + 500 - size) - (i * size) - center), size=(size, size))
        elif qnt_x <= qnt_y:
            # scenes width is always greater than height
            size = (win_h / qnt_y)
            center = (win_w - (size * qnt_x)) / 2
            Rectangle(pos=(j * size + center, (self.get_top() + 500 - size) - (i * size)), size=(size, size))


class AppScreen(Widget):
    map = ObjectProperty(None)

    def on_enter(self):
        # we screen comes into view, start the game
        self.map.draw()


class AcoApp(App):
    def build(self):
        self.m = AppScreen()
        self.fields = []
        self.iterations = int(self.config.get('Parameters', 'iterations'))
        self.all_iterations = self.iterations
        self.scenario = str(self.config.get('Parameters', 'scenarios'))
        self.scenarios = {'Scenario1': Scenario1,
                          'Scenario2': Scenario2,
                          'Scenario3': Scenario3,
                          'Scenario4': Scenario4}
        self.generate()
        return self.__generate_graphics()

    # Graphics
    use_kivy_settings = False
    settings_cls = 'SettingsWithTabbedPanel'
    grid = ObjectProperty(None)
    iteration = NumericProperty(0)
    all_iterations = NumericProperty(0)
    path_length = NumericProperty(0)

    def generate(self):
        simulation = Simulation(self.scenarios[self.scenario], n_iterations=1)
        self.fields = simulation.get_fields()
        self.__generate_graphics()
        return simulation

    def train(self):
        simulation = Simulation(self.scenarios[self.scenario], self.training_iteration_finished, self.iterations)
        simulation.start(self)

    def test(self):
        self.__clear_map()
        simulation = Simulation(self.scenarios[self.scenario], self.test_iteration_finished, 1)
        simulation.start(self)

    def result(self, simulation):
        paths = simulation.solution()
        symbols = ["0","1","2","3"]
        last_x, last_y = [0]*len(paths), [0]*len(paths)
        if 0 < len(paths) <= len(symbols):
            for field in range(len(paths[0])):
                for w in range(len(paths)):
                    if field > 0:
                        self.fields[last_x[w]][last_y[w]] = Map.EMPTY
                    last_x[w], last_y[w] = paths[w][field].x, paths[w][field].y
                    self.fields[paths[w][field].x][paths[w][field].y] = symbols[w]
                    last_x[w], last_y[w] = (paths[w][field].x, paths[w][field].y)
                self.__generate_graphics()
                time.sleep(0.5)

    def training_iteration_finished(self, iteration, length):
        self.iteration = iteration + 1
        if length < self.path_length or self.path_length == 0:
            self.path_length = length

    def test_iteration_finished(self, iteration, length):
        if length < self.path_length or self.path_length == 0:
            self.path_length = length

    def run_training(self):
        _thread.start_new_thread(self.train, ())

    def run_test(self):
        _thread.start_new_thread(self.test, ())

    def __clear_map(self):
        self.m.map.clear()

    def __generate_graphics(self):
        self.m.map.set_fields(self.fields)
        self.m.map.draw()
        return self.m

    def build_config(self, config):
        config.setdefaults('Parameters', {
            'iterations': '100'
        })
        config.setdefaults('Parameters', {
            'scenarios': 'Scenario1'
        })

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            self.iteration = 0
            self.path_length = 0
            if token == ('Parameters', 'Iterations'):
                self.iterations = int(value)
                print("Number of iterations has been changed to ", int(value))
                self.all_iterations = self.iterations
            if token == ('Parameters', 'Scenarios'):
                self.scenario = str(value)
                print("Scenario has been changed to ", str(value))
                self.generate()

    def build_settings(self, settings):
        jsondata = """[
            { "type": "title",
              "title": "ACO" },

            { "type": "numeric",
              "title": "Iterations",
              "desc": "Number of iterations",
              "section": "Parameters",
              "key": "Iterations"},

            { "type": "options",
              "title": "Scenarios",
              "desc": "Choose scenario",
              "section": "Parameters",
              "key": "Scenarios",
              "options": ["Scenario1", "Scenario2", "Scenario3", "Scenario4"] }
        ]"""
        settings.add_json_panel('ACO', self.config, data=jsondata)


if __name__ == '__main__':
    AcoApp().run()
