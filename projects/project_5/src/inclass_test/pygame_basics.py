# pygame_basics.py
#
# ICS 32A Fall 2019
# Code Example
#
# Below is a complete version of the example from the PyGame Basics notes.

import pygame


def run() -> None:
    pygame.init()

    surface = pygame.display.set_mode((700, 600))

    running = True
    color_amount = 0
    rect_length = 100
    rect_width = 100
    rect_top = 10

    clock = pygame.time.Clock()

    while running:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        color_amount = 15
        if rect_top < (600 - rect_length):
            rect_top += 2
            print(rect_top)

        surface.fill(pygame.Color(color_amount, color_amount, color_amount))

        test_rect = pygame.Rect(10, rect_top, rect_length, rect_width)

        pygame.draw.rect(
            surface, pygame.Color(255, 255, 0),
            test_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    run()
