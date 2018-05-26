import json

import numpy as np
import requests

from model.tools.binary_printer import BinaryPrinter
from model.utils.choiceUtils import weighted_random
import urllib


class DeepBehaviour:
    distribution = np.random.rand

    ASK_URL = "localhost:9000/ask"

    ASK_HEADERS = {
        'Authorization': 'XXXXX',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    TELL_URL = "localhost:9000/ask"

    TELL_HEADERS = {
        'Authorization': 'XXXXX',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    def __init__(self, walker, enemies=None):
        self.walker = walker
        self.enemies = enemies
        self.light_map = walker.light_map
        self.printer = BinaryPrinter(walker.area)

    def decide(self, possible_moves, position=None):
        # They correspond to individual moves
        map_images = self._gen_maps(possible_moves)
        try:
            probabilities = self.ask_model(map_images)
        except IOError as e:
            print("Problem with model,loading defaults: {}".format(e))
            default_prob = 1.0 / len(possible_moves)
            probabilities = [default_prob]*len(possible_moves)
        weighted_moves = [(m, p) for m, p in zip(possible_moves, probabilities)]
        return weighted_random(weighted_moves)

    def _gen_maps(self, possible_moves):
        positions = [move.target for move in possible_moves]
        maps = []
        for position in positions:
            sm = self.light_map.shadow_map_with_new_position(position)
            self.printer.set_view(sm)
            for actor in [self.walker]+self.enemies:
                self.printer.set_position(actor.position, actor.symbol)
            self.printer.gen_walls()
            maps.append(self.printer.fields)
        return maps

    def ask_model(self, images):
        content = [image.tolist() for image in images]
        r = requests.get(self.ASK_URL, headers=self.ASK_HEADERS, json=json.dumps(content))
        return json.load(r.text)


