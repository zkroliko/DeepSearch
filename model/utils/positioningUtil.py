import random

from model.field import Field


def random_field(area, start):
    x, y = random.randint(0, area.width() - 1), random.randint(0, area.height() - 1)
    potential_field = Field(x, y)
    while not (area.is_field_accessible(potential_field) and potential_field != start):
        potential_field = Field(x, y)
        x, y = random.randint(0, area.width() - 1), random.randint(0, area.height() - 1)
    return potential_field
