# spots.py
#
# ICS 32A Fall 2019
# Code Example
#
# This module implements the "model" for our Spots game.  The job of a
# model is to encompass the details of how the game works, without
# regard to specifically what it looks like or specifically how the
# user will interact with it.  The overall "world" in our Spots game
# was a collection of spots that could be created and would move in
# random directions on their own.  We're implementing that concept
# here with two classes:
#
# * Spot, which encapsulates the idea of a single spot.  Each spot
#   knows what its center point, radius, and velocity is, where the
#   velocity is tracked as a "delta" (rate of change) in both the
#   x- and y-coordinates.
#
# * SpotsState, which encapsulates the entire state of the Spots
#   game.  Fundamentally, the state of our game is a list of the
#   spots that are currently displayed.  Additionally, SpotsState
#   can do things: add new spots or remove existing spots when
#   clicks happen, move all spots when we change from one frame
#   of animation to the next.

import math
import random


class Spot:
    def __init__(self, center: (float, float), radius: float):
        self._center = center
        self._radius = radius

        # random.random() returns a random float value between 0 and 1,
        # with an equal change of any particular value being returned.
        # By multiplying it by 0.01 and subtracting 0.005, we're changing
        # the range of possible results from -0.005 to 0.005 instead.
        # This has the effect of giving every spot a random direction
        # and speed.
        self._delta_x = (random.random() * 0.01) - 0.005
        self._delta_y = (random.random() * 0.01) - 0.005

    def center(self) -> (float, float):
        return self._center

    def radius(self) -> float:
        return self._radius

    def move(self) -> None:
        x, y = self._center
        self._center = (x + self._delta_x, y + self._delta_y)

    def contains(self, point: (float, float)) -> bool:
        # We can tell if a spot contains a point by seeing how far that
        # point is from the center of the spot.  If the distance is no more
        # than the radius, the point is inside the spot; otherwise, it's not.
        px, py = point
        cx, cy = self._center

        return math.sqrt((px - cx) * (px - cx) + (py - cy) * (py - cy)) <= self._radius


class SpotsState:
    def __init__(self):
        self._spots = []

    def all_spots(self) -> [Spot]:
        return self._spots

    def handle_click(self, click_point: (float, float)) -> None:
        # By writing the code to check if a spot contains a point inside the
        # Spot class, look how simple this loop becomes.  It reads almost
        # like English; that's no accident.
        #
        # The reason we're looping through the spots backward is because
        # we want to eliminate the most-recently-added match first, so
        # if two spots overlap, the one that disappears is the one on
        # top.
        for spot in reversed(self._spots):
            if spot.contains(click_point):
                self._spots.remove(spot)
                return

        self._spots.append(Spot(click_point, 0.05))

    def move_all_spots(self) -> None:
        for spot in self._spots:
            spot.move()
