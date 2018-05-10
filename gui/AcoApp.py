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

from acoAlgorithm.PheromoneMap import PheromoneMap
from acoAlgorithm.Simulation import Simulation
from acoAlgorithm.Walker import Walker
from acoAlgorithm.tools.Printer import Printer
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
    POSITION = 'P'

    colors = {
        EMPTY: (1, 1, 1),
        OCCUPIED: (0, 0, 0),
        VISIBLE: (1, 0.945, 0.008),
        START: (0, 1, 0),
        POSITION: (1, 0, 0)
    }

    fields = []

    def set_fields(self, fields):
        self.fields = fields

    def draw(self):
        with self.canvas:
            for i in range(len(self.fields)):
                for j in range(len(self.fields[i])):
                    self.draw_field(i, j)

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
        simulation = Simulation(self.scenarios[self.scenario],self.iterations)
        self.fields = simulation.get_fields()
        self.__generate_graphics()
        return simulation

    def simulate(self):
        simulation = self.generate()
        simulation.start(self)

    def result(self, simulation):
        path = simulation.best_solution()
        for field in path:
            self.fields[field.x][field.y] = Map.POSITION
            self.__generate_graphics()
            time.sleep(0.5)

    def iteration_finished(self, iteration, length):
        self.iteration = iteration+1
        if length < self.path_length or self.path_length == 0:
            self.path_length = length

    def run_simulation(self):
        _thread.start_new_thread(self.simulate, ())


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
