import json
import random

import numpy as np
import requests

from model.tools.binary_printer import BinaryPrinter
from model.utils.choiceUtils import weighted_random
import urllib


class DeepBehaviour:
    distribution = np.random.rand

    ASK_URL = "http://localhost:5000/ask"

    ALPHA = 0.1
    EPSILON = 0.7
    GAMMA = 0.4

    ASK_HEADERS = {
        'Authorization': 'XXXXX',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    TELL_URL = "http://localhost:5000/tell"

    TELL_HEADERS = {
        'Authorization': 'XXXXX',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    def __init__(self, walker, model, enemies=None):
        self.walker = walker
        self.enemies = enemies
        self.light_map = walker.light_map
        self.printer = BinaryPrinter(walker.area)
        self.model = model
        self.past_experiences = []

    def decide(self, possible_moves, position=None):
        # They correspond to individual moves
        map_images = self._gen_maps(possible_moves)
        if random.random() < self.EPSILON:
            # Experiment
            default_prob = 1.0 / len(possible_moves)
            values = [default_prob] * len(possible_moves)
            weighted_moves = [(m, p) for m, p in zip(possible_moves, values)]
        else:
            try:
                values = self.model.value_maps(map_images)
                print(values)
            except IOError as e:
                print("Problem with model, loading defaults: {}".format(e))
                default_prob = 1.0 / len(possible_moves)
                values = [default_prob] * len(possible_moves)
            weighted_moves = [(m, p) for m, p in zip(possible_moves, values)]
        return weighted_random(weighted_moves)


    def _gen_maps(self, possible_moves):
        positions = [move.target for move in possible_moves]
        maps = []
        for position in positions:
            sm = self.light_map.shadow_map_with_new_position(position)
            maps.append(self._gen_map(sm, position))
        return maps

    def _gen_map(self, sm, new_position):
        self.printer = BinaryPrinter(self.walker.area)
        self.printer.set_view(sm)
        self.printer.set_position(new_position, self.walker.symbol)
        for actor in self.enemies:
            self.printer.set_position(actor.position, actor.symbol)
        self.printer.gen_walls()
        return self.printer.fields

    def consume_learning_data(self):
        sm = self.light_map.to_discover
        self.past_experiences.append(self._gen_map(sm,self.walker.position))

    def commit_learning_data(self, reward):
        try:
            labeled_images = ([e for e in self.past_experiences],
                              [reward] * len(self.past_experiences))
            self.model.train(labeled_images)
        except IOError as e:
            print("Couldn't communicate learning data to model: ", e)
