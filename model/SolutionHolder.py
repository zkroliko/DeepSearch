import sys

class SolutionHolder:
    def __init__(self):
        self.path = None
        self.length = sys.maxsize

    def record_solution(self, walker):
        new_length = self.calc_length(walker.path)
        if new_length < self.length:
            self.path = walker.path
            self.length = new_length

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
