from model.area import Area
from model.field import Field, FieldType
from model.rectangle import Rectangle


class Scenario3:
    @staticmethod
    def start():
        return Field(0, 0)

    @staticmethod
    def area():
        a = Area.of_size(16)

        rectangles = [
            Rectangle(Field(3, 3), Field(12, 3), type=FieldType.inaccessible),
            Rectangle(Field(3, 12), Field(12, 12), type=FieldType.inaccessible),
            Rectangle(Field(7, 6), Field(8, 9), type=FieldType.inaccessible),
        ]
        a += rectangles
        return a

    @staticmethod
    def name():
        return "Scenario3"
