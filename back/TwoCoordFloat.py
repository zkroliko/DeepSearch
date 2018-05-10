from acoAlgorithm.TwoCoordinate import TwoCoordinate
from acoAlgorithm.utils.FloatUtils import is_close


class TwoCoordFloat(TwoCoordinate):

    def __eq__(self, other):
        # This has a floating point comparison
        return is_close(self.x, other.x) and is_close(self.y, other.y)

