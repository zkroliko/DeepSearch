from enum import Enum


# This map is indented to affect walkers decision
# so to prevent loop-like behaviour and backstepping
class AntiLoopMap:
    def __init__(self):
        self.pheromone = {}

    def add(self, transition, amount=1):
        if transition in self.pheromone:
            # Has pheromone update already
            self.pheromone[transition] += amount
            return False
        else:
            # Never has been set before
            self.pheromone[transition] = amount
            return True

    def transition_count(self, transition):
        if transition in self.pheromone:
            return self.pheromone[transition]
        else:
            return 0