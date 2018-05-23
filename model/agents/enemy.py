from model.agents.agent import Agent


class Enemy(Agent):
    def __init__(self, area, start, decision_maker, contact_effect=None, symbol="e"):
        super().__init__(area, start, decision_maker, symbol)
        self.contact_effect = contact_effect

    def step(self, target=None):
        super().step(target)

    def check_effect(self, walker):
        if self.contact_effect and walker.position == self.position:
            self.contact_effect.apply(walker)
