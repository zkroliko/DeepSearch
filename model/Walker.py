import numpy as np

from model.field import Field
from model.move import Move
from model.view import ViewGenerator
from model.empty_view import EmptyView


class Walker:
    # Moves we can make
    MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (0, 0)]

    def __init__(self, area, start, decision_maker, shadow_map=None):
        self.area = area
        self.checker = Walker.StepChecker(area)
        self.decider = decision_maker
        self.alive = True
        self.won_unexpectedly = False
        if shadow_map:
            self.view = ViewGenerator(area, shadow_map)
        else:
            self.view = EmptyView(area)
        # Setting the start position
        if area.is_field_accessible(start):
            self.position = start
            self.path = [start]
        else:
            raise Exception("Cannot place walker on the given field")

    def can_step(self, target):
        return self.checker.can_make(Move(self.position, target))

    def finished(self):
        return self.view.finished() and self.alive and not self.won_unexpectedly

    def step(self, target=None):
        possible = []
        for i, j in self.MOVES:
            if self.position.x + i >= 0 and self.position.y + j >= 0:
                candidate_move = Move(self.position, Field(self.position.x + i, self.position.y + j))
                if self.checker.can_make(candidate_move):
                    possible.append(candidate_move)
        # Check if we are not blocked
        if possible.__len__() == 0:
            raise Exception("Walker cannot make any moves from field %s" % (self.position))
        # We can initially update out light map based on possible moves - but a max of 9
        self.view.react_to_new_place(possible)
        # Asking the decision maker for move
        next_move = self.decider.decide(possible,self.position)
        # Making the move
        self.change_position(next_move.target)

        return self.position

    def change_position(self, target):
        if self.can_step(target):
            self.position = target
            self.path.append(self.position)
        else:
            raise Exception("Cannot step on the given field")

    # Inner class
    class StepChecker:

        def __init__(self, area):
            self.area = area

        def can_make(self, move):
            return move.valid(self.area)
