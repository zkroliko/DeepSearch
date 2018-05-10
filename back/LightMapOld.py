from enum import Enum


class LightMapOld:
    def __init__(self, area, shadow_map=None):
        # Total area
        total_area = area.main.size()
        # Filtering out the occupied
        occupied = []
        for item in area.all_rectangles():
            if item.type:
                occupied.append(item)
        # Mapping to sizes
        sizes = map(lambda x: x.size(), occupied)
        occupied_area = sum(sizes)
        # Now for the actual thing - the difference
        self.area_to_discover = total_area - occupied_area

        # TODO: Make this right -> don't do n^2

        # Checking out occupied area
        self.occupied = set()
        for rect in occupied:
            for coordinates in rect.all_fields_raw():
                self.occupied.add(coordinates)

        # Making a dict representing the seen area, main attribute
        # it will contain a count of how many times given coordinates
        # has been seen, not used in algorithm per se but useful for
        # quantifying it's performance
        self.seen = set()

    def check(self, coordinates):
        if coordinates in self.seen:
            # Has already been seen
            return False
        if coordinates in self.occupied:
            return False
        else:
            # Never had been seen before
            self.seen.add(coordinates)
            self.area_to_discover -= 1
            return True

    def remains_to_be_checked(self, coordinates):
        return False if coordinates in self.seen else coordinates not in self.occupied

    def is_checked(self, coordinates):
        return coordinates in self.seen

    def finished(self):
        return self.area_to_discover <= 0
        # Zero just in case

    def how_many_left(self):
        return self.area_to_discover
