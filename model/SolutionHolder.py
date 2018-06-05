import sys


class SolutionHolder:
    DEATH_PUNISHMENT = 0

    def __init__(self):
        self.path = None
        self.rewards = []
        self.best_reward = -sys.maxsize

    def assess_solution(self, walker, maxed=False):
        new_length = self.calc_length(walker.path)
        reward = (1.0 / (new_length - 1)) if not (walker.dead or maxed) else self.DEATH_PUNISHMENT
        self.rewards.append(reward)
        if reward > self.best_reward:
            self.path = walker.path
            self.best_reward = reward
        return reward

    def calc_length(self, path):
        return len(path)

    def path_to_str(self):
        str = ""
        for field in self.path:
            str += field.__str__()
            str += ", "
        return str

    def path_to_csv(self):
        str = ""
        for field in self.path:
            str += "{},{}".format(field.x, field.y)
            str += "\n"
            return str
