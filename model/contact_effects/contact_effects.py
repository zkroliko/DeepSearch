from model.utils.positioningUtil import random_field


class DestroyEffect:
    def __init(self, position_generator):
        self.generator = position_generator

    def apply(self, walker):
        walker.alive = False


class WinEffect:
    def __init(self, position_generator):
        self.generator = position_generator

    def apply(self, walker):
        walker.won_unexpectedly = True


class TransportEffect:
    def __init(self, position_generator):
        self.generator = position_generator

    def apply(self, walker):
        walker.position = self.generator()
