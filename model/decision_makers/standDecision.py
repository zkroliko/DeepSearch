import numpy as np

from model.utils.choiceUtils import weighted_random


class StandDecision:
    distribution = np.random.rand

    def __init__(self):
        pass

    def decide(self, possible_moves):
        standing = [move for move in possible_moves if move.source == move.target]
        return standing[0]
