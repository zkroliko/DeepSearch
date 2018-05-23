from model.agents.agent import Agent
from model.empty_view import EmptyView
from model.view import ViewGenerator


class Walker(Agent):
    def __init__(self, area, start, decision_maker, shadow_map=None, symbol="W"):
        if shadow_map:
            self.view = ViewGenerator(area, shadow_map)
        else:
            self.view = EmptyView(area)
        super().__init__(area, start, decision_maker, symbol)
        self.dead = False
        self.won_unexpectedly = False


    def finished(self):
        return self.view.finished() or self.dead or self.won_unexpectedly

    def react_to_new_place(self):
        self.view.react_to_new_place(self.position)

    def step(self, target=None):
        super().step(target)

