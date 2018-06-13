import json
import random

import math
import numpy as np
import requests

from model.tools.binary_printer import BinaryPrinter
from model.utils.choiceUtils import weighted_random
import urllib


class DeepBehaviourState:

    EPSILON_START = 0.8
    EPSILON_SCALING = 0.999

    def __init__(self):
        self.epsilon = self.EPSILON_START