import numpy as np

from model.decision_makers.target_behaviour import TargetBehaviour


class CircleLeftBehaviour(TargetBehaviour):

    TRANSFORM_VECTOR = np.array([[0, -1], [1, 0]])

