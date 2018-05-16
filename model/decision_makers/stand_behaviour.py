import numpy as np

from model.utils.choiceUtils import weighted_random


class StandBehaviour:
    distribution = np.random.rand

    def __init__(self):
        pass

    def decide(self, possible_moves,position=None):
        standing = [move for move in possible_moves if move.source == move.target]
        return standing[0]
