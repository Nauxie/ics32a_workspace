# spots_model.py


class Spot:
    def __init__(self, center: (float, float), radius: float):
        self._center_x, self._center_y = center
        self._radius = radius

    def center(self) -> (float, float):
        return(self._center_x, self._center_y)

    def radius(self) -> float:
        return self._radius


class SpotsState:
    def __init__(self):
        self._spots = []

    def all_spots(self) -> [Spot]:
        return self._spots
