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
    circle_center_x = 350
    circle_center_y = 300
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        color_amount = (color_amount + 1) % 256
        circle_center_x -= 1
        circle_center_y += 1
        
        surface.fill(pygame.Color(color_amount, color_amount, color_amount))

        pygame.draw.circle(
            surface, pygame.Color(255, 255, 0),
            (circle_center_x, circle_center_y), 100)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    run()
