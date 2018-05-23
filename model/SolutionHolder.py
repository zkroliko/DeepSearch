import sys

class SolutionHolder:

    DEATH_PUNISHMENT = -1

    def __init__(self):
        self.path = None
        self.bast_reward = sys.maxsize

    def assess_solution(self, walker):
        new_length = self.calc_length(walker.path)
        reward = 1.0 / new_length if not walker.dead else self.DEATH_PUNISHMENT
        if reward < self.bast_reward:
            self.path = walker.path
            self.bast_reward = reward
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
