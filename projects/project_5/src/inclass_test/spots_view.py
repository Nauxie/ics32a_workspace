# spots_game.py
#
# ICS 32A Fall 2019
# Code Example
#
# This module implements the "view" for our Spots game.  The job of a
# view is to focus on how the game looks and feels -- how it's drawn and
# how the user interacts with it -- while ignoring the details about the
# game's mechanics.  It's not uncommon for the view to hold a reference
# back to the model, which we're doing here.  As the user does things,
# they'll generate events in the view, which will then be sent to the
# model as higher-level operations that affect the game's mechanics.
#
# Note, too, that we've taken a keener eye toward the design of this
# example, by doing a couple of additional things:
#
# * We implemented our game in a class, rather than in a function.  This
#   gives us a natural way to break it up into many functions, while
#   still preserving their ability to share the important information
#   between them (in the form of the "self" parameter that they all
#   share).
#
# * We broke up our game loop into calls to methods in this class.  This
#   took what would have been a long, complex method and made it much
#   shorter.  By giving names to these "helper" methods, we've made
#   clearer the pattern that shows up in our design.  Going forward,
#   if we were to add new features, they would have a place where they
#   belong.  For example, new user inputs would be dealt with in
#   _handle_events; changes to how things are drawn would be dealt with
#   in _redraw; and so on.

import pygame
import spots


class SpotsGame:
    def __init__(self):
        self._running = True
        self._state = spots.SpotsState()

    def run(self) -> None:
        pygame.init()

        self._resize_surface((600, 600))

        clock = pygame.time.Clock()

        while self._running:
            clock.tick(30)
            self._handle_events()
            self._redraw()

        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_button(event.pos)

        self._move_spots()

    def _redraw(self) -> None:
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(255, 255, 0))
        self._draw_spots()

        pygame.display.flip()

    def _draw_spots(self) -> None:
        for spot in self._state.all_spots():
            self._draw_spot(spot)

    def _draw_spot(self, spot: spots.Spot) -> None:
        frac_x, frac_y = spot.center()

        topleft_frac_x = frac_x - spot.radius()
        topleft_frac_y = frac_y - spot.radius()

        frac_width = spot.radius() * 2
        frac_height = spot.radius() * 2

        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()

        topleft_pixel_x = topleft_frac_x * width
        topleft_pixel_y = topleft_frac_y * height

        pixel_width = frac_width * width
        pixel_height = frac_height * height

        pygame.draw.ellipse(
            surface, pygame.Color(0, 0, 0),
            pygame.Rect(
                topleft_pixel_x, topleft_pixel_y,
                pixel_width, pixel_height))

    def _end_game(self) -> None:
        self._running = False

    def _resize_surface(self, size: (int, int)) -> None:
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def _on_mouse_button(self, pos: (int, int)) -> None:
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()

        pixel_x, pixel_y = pos

        frac_x = pixel_x / width
        frac_y = pixel_y / height

        self._state.handle_click((frac_x, frac_y))

    def _move_spots(self) -> None:
        self._state.move_all_spots()


if __name__ == '__main__':
    SpotsGame().run()
