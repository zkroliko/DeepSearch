from acoAlgorithm.Area import Area
from acoAlgorithm.Field import Field, FieldType
from acoAlgorithm.Rectangle import Rectangle


class Scenario1:
    @staticmethod
    def start():
        return Field(4, 4)

    @staticmethod
    def area():
        a = Area.of_size(8)

        rectangles = [
            Rectangle(Field(2, 2), Field(3, 3), type=FieldType.inaccessible),
            Rectangle(Field(2, 5), Field(3, 6), type=FieldType.inaccessible),
            Rectangle(Field(5, 2), Field(6, 3), type=FieldType.inaccessible),
            Rectangle(Field(5, 5), Field(6, 6), type=FieldType.inaccessible)
        ]
        a += rectangles
        return a