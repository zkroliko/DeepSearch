import numpy as np

from model.utils.choiceUtils import weighted_random


class RandomBehaviour:
    distribution = np.random.rand

    def __init__(self):
        pass

    def decide(self,possible_moves,position=None):
        probability = 1.0 / len(possible_moves)
        weighted_moves = [ (m,probability) for m in possible_moves ]
        return weighted_random(weighted_moves)
