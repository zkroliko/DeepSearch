from model.agents.agent import Agent
from model.lightMap import LightMap


class Walker(Agent):
    def __init__(self, area, start, decision_maker, shadow_map=None, symbol="W"):
        self.light_map = LightMap(area, shadow_map)
        super().__init__(area, start, decision_maker, symbol)
        self.dead = False
        self.won_unexpectedly = False

    def finished(self):
        return self.light_map.finished() or self.dead or self.won_unexpectedly

    def react_to_new_place(self):
        self.light_map.look_around_at(self.position)

    def step(self, target=None):
        super().step(target)

