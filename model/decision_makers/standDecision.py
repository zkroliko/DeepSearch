import numpy as np

from model.utils.choiceUtils import weighted_random


class RandomDecision:
    distribution = np.random.rand

    def __init__(self):
        pass

    def decide(self, possible_moves):
        return 0, 0
