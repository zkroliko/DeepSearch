from enum import Enum


class PheromoneMap:
    INITIAL_PHEROMONE = 0.1

    DELETION_THRESHOLD = 0.01

    VAPORISATION_COEFFICIENT = 0.8

    def __init__(self):
        # This is the general level of pheromone
        self.pheromone = {}
        # This is the level of pheromone in one update (one walker pass)
        self.update = {}
        self.update_weight = 1

    # This is all is for just the update

    def add(self, transition, amount=1):
        if transition in self.update:
            # Has pheromone update already
            # self.update[transition] += amount
            return False
        else:
            # Never has been set before
            self.update[transition] = +  amount
            return True

    def update_amount(self, transition):
        if transition in self.update:
            return self.update[transition]
        else:
            return 0

    def apply_update(self):
        for key, value in self.update.items():
            self.__update_pheromone_at(key, value)
        # Deleting the entries in self.update
        self.update.clear()
        self.__evaporate()

    def __evaporate(self):
        for transition, value in list(self.pheromone.items()):
            new_value = value * self.VAPORISATION_COEFFICIENT
            if new_value < self.DELETION_THRESHOLD:
                self.pheromone.pop(transition)
            else:
                self.pheromone[transition] = new_value

    def __update_pheromone_at(self, transition, value):
        if transition in self.pheromone:
            # Had pheromone
            update_amount = value * float(self.update_weight)
            self.pheromone[transition] += update_amount
            return False
        else:
            # No pheromone before
            initial_amount = self.INITIAL_PHEROMONE + value * float(self.update_weight)
            self.pheromone[transition] = initial_amount
            return True

    def set_update_weight(self, weight):
        self.update_weight = weight

    # This is for the general pheromone level

    def pheromone_at(self, transition):
        if transition in self.pheromone:
            return self.pheromone[transition]
        else:
            return self.INITIAL_PHEROMONE
