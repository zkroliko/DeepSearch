from model.Area import Area
from model.Field import Field, FieldType
from model.Rectangle import Rectangle


class Scenario2:
    @staticmethod
    def start():
        return Field(1, 0)

    @staticmethod
    def area():
        a = Area.of_size(8)

        rectangles = [
            Rectangle(Field(0, 0), Field(0, 5), type=FieldType.inaccessible),
            Rectangle(Field(3, 0), Field(3, 5), type=FieldType.inaccessible),
            Rectangle(Field(4, 5), Field(6, 5), type=FieldType.inaccessible),
            Rectangle(Field(6, 3), Field(7, 3), type=FieldType.inaccessible)
        ]
        a += rectangles
        return a

    @staticmethod
    def name():
        return "Scenario2"
