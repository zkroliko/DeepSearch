class Effect:
    def __init__(self, position_generator):
        self.generator = position_generator


class KillEffect(Effect):
    def __init__(self, position_generator):
        super().__init__(position_generator)

    def apply(self, walker):
        walker.dead = True


class WinEffect(Effect):
    def __init__(self, position_generator):
        super().__init__(position_generator)

    def apply(self, walker):
        walker.won_unexpectedly = True


class TransportEffect(Effect):
    def __init__(self, position_generator):
        super().__init__(position_generator)

    def apply(self, walker):
        walker.change_position(self.generator(walker.area, walker.position), no_checks=True)
