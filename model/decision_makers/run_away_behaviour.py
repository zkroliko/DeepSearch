import numpy as np

from model.decision_makers.target_behaviour import TargetBehaviour
from model.utils.choiceUtils import weighted_random


class RunAwayBehaviour(TargetBehaviour):

    TRANSFORM_VECTOR = np.array([[-1, -1], [0, 0]])
