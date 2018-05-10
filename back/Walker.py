import numpy as np

from acoAlgorithm.AntiLoopMap import AntiLoopMap
from acoAlgorithm.Field import Field
from acoAlgorithm.LightMap import LightMap
from acoAlgorithm.Move import Move
from acoAlgorithm.View import ViewGenerator
from acoAlgorithm.utils.Cache import LRUCache, MoveCache


class Walker:
    # Moves we can make
    MOVES = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, area, start, pheromone_map, shadow_map=None):
        self.area = area
        self.pherm_map = pheromone_map
        self.anti_loop_map = AntiLoopMap()
        self.checker = Walker.StepChecker(area)
        self.decider = Walker.DecisionMaker(self, pheromone_map, self.anti_loop_map)
        self.view = ViewGenerator(area, shadow_map)
        # Setting the start position
        if area.is_field_accessible(start):
            self.position = start
            self.path = [start]
            # self.view.shine_from(self.position)
        else:
            raise Exception("Cannot place walker on the given field")

    def can_step(self, target):
        return self.checker.can_make(Move(self.position, target))

    def finished(self):
        return self.view.lm.finished()

    def step(self, target=None):
        possible = []
        for i, j in self.MOVES:
            if not (self.position.x + i < 0 or self.position.y + j < 0):
                candidate_move = Move(self.position, Field(self.position.x + i, self.position.y + j))
                if self.checker.can_make(candidate_move):
                    possible.append(candidate_move)
        # Check if we are not blocked
        if possible.__len__() == 0:
            raise Exception("Walker cannot make any moves from field %s" % (self.position))
        # We can initially update out light map based on possible moves - but a max of 9
        self.view.react_to_new_place(possible)
        # Asking the decision maker for move
        next_move = self.decider.decide(possible)
        # Adding the transition to pheromone map
        self.pherm_map.add(next_move)
        # and anti-loop map
        self.anti_loop_map.add(next_move)
        # Making the move
        self.change_position(next_move.target)

        return self.position

    def change_position(self, target):
        if self.can_step(target):
            self.position = target
            self.path.append(self.position)
            # self.view.shine_from(self.position)
        else:
            raise Exception("Cannot step on the given field")

    class DecisionMaker:

        ANTI_LOOP_COEFF = 100

        distribution = np.random.rand

        def __init__(self, walker, pheromone_map, anti_loop):
            self.walker = walker
            self.pheromone_map = pheromone_map
            self.anti_loop = anti_loop

        def decide(self, possible_moves):
            pheromone_levels = [self.pheromone_map.pheromone_at(move) for move in possible_moves]
            total_pheromone = sum(pheromone_levels)

            past_moves = map(lambda transition: self.anti_loop.transition_count(transition), possible_moves)
            total_past_moves = sum(past_moves)

            random_sample = self.distribution(1, 1)

            # Will be levels for the categorization of the sample
            levels = {}

            last_level = 0

            # Determining the categorisation levels
            for idx, move in enumerate(possible_moves):
                # Calculating the weight
                transitions_to_possibility = self.anti_loop.transition_count(move)
                if transitions_to_possibility == 0:
                    anti_loop_weight = total_past_moves + 1
                else:
                    anti_loop_weight = total_past_moves + 1 / transitions_to_possibility
                # Coefficient for anti loop weight
                anti_loop_weight *= self.ANTI_LOOP_COEFF
                # For the case if total_pheromone is 0
                if total_pheromone == 0:
                    probability = float(1) / len(possible_moves)
                else:
                    probability = pheromone_levels[idx] / float(total_pheromone)
                # Adding weight to probability
                probability *= anti_loop_weight
                levels[(last_level, last_level + probability)] = move
                last_level += probability

            # Now we will determine the max categorization level
            max_level_bound = max(map(lambda interval: interval[1], levels.keys()))
            # Scaling the sample to max bound
            random_sample *= max_level_bound
            for interval, move in levels.items():
                if interval[0] <= random_sample < interval[1]:
                    return move

    # Inner class
    class StepChecker:

        def __init__(self, area):
            self.area = area
            # self.cache = LRUCache(50)

        def can_make(self, move):
            # # # Cache check
            # if self.cache.has(move.target):
            #     return self.cache.get(move.target)
            # # Cache miss
            # move_valid = move.valid(self.area)
            # # Add to cache
            # self.cache.set(move.target, move_valid)
            # return move_valid

            return move.valid(self.area)
