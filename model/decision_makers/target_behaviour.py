import numpy as np

from model.utils.choiceUtils import weighted_random


class TargetBehaviour:
    distribution = np.random.rand

    RANDOM_COEFF = 3

    TRANSFORM_VECTOR = None

    def __init__(self, target=None):
        self.target = target

    def _vector_to_target(self, position):
        return [self.target.position.x-position.x, self.target.position.y-position.y]

    def decide(self, possible_moves, position=None):
        tv = self._vector_to_target(position)
        dot_products = [np.dot(list(move.vector @ self.TRANSFORM_VECTOR), tv) for move in possible_moves]
        # We want to introduce some noise
        dot_products += (np.random.rand(len(dot_products))*2-1.0)*self.RANDOM_COEFF
        dot_products = list(dot_products)
        return possible_moves[dot_products.index(max(dot_products))]
