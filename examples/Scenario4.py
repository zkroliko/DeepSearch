from model.Area import Area
from model.Field import Field, FieldType
from model.Rectangle import Rectangle


class Scenario4:
    @staticmethod
    def start():
        return Field(0, 0)

    @staticmethod
    def area():
        a = Area.of_size(64)

        rectangles = [
            Rectangle(Field(50, 0), Field(40, 50), type=FieldType.inaccessible),
        ]
        a += rectangles
        return a
