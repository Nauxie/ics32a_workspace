import pygame
from gamelogic import Board
import random


BACKGROUND_COLOR = pygame.Color(209, 223, 232)
ROWS = 13
COLS = 6


class Game:
    def __init__(self):
        '''constructor'''
        self._running = True
        self.jewel_list = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']
        self.color_list = [(155, 55, 137), (41, 239, 205), (208, 149, 60),
                           (77, 146, 80), (169, 46, 17), (186, 236, 69), (129, 185, 224)]
        self.board = self._create_board()
        self.grid = self.board.board

    def run(self) -> None:
        '''runs game interface'''
        pygame.init()
        try:
            self._resize_surface((300, 650))  # 300 = 6 * 50, 650 = 6 * 50
            clock1 = pygame.time.Clock()
            counter = 0
            while self._running:
                clock1.tick(30)
                self._handle_events()
                self._redraw()
                if (counter % 10 == 0):
                    if (not self.board.faller_active and not self.board.freezer_active and not self.board.matching_active and not self.board.game_over):
                        self.board.handle_faller_generation(
                            random.randint(1, 6), self._create_random_faller())
                    elif (self.board.faller_active or self.board.freezer_active or self.board.matching_active and not self.board.game_over):
                        self.board.handle_blank()
                counter += 1
        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        '''get list of events (inputs) and handles them'''
        for event in pygame.event.get():
            self._handle_event(event)

    def _resize_surface(self, size: (int, int)) -> None:
        '''allows window to be resizable'''
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def _handle_event(self, event: pygame.event) -> None:
        '''takes a pygame event and handles it with the appropriate ingame action'''
        if (event.type) == pygame.QUIT:
            self._running = False
        elif event.type == pygame.VIDEORESIZE:
            self._resize_surface(event.size)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.board.move_left()
            if event.key == pygame.K_RIGHT:
                self.board.move_right()
            if event.key == pygame.K_SPACE:
                self.board.handle_rotate()

    def _redraw(self) -> None:
        '''redraws the surface by adding to the surface display object'''
        surface = pygame.display.get_surface()

        surface.fill(pygame.Color(255, 255, 255))
        self._draw_board()
        pygame.display.flip()

    def _draw_board(self) -> None:
        '''draws the rect elements on the board'''
        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        block_width = width / COLS
        block_height = height / ROWS
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                # x,y coordinates  = (i, j)
                if ([i, j] in self.board.matching_locations):
                    test_rect = pygame.Rect(
                        block_width*j, block_height*i, block_width, block_height)
                    if (self.grid[i][j] in self.jewel_list):
                        color = self.color_list[self.jewel_list.index(
                            self.grid[i][j])]
                        pygame.draw.rect(
                            surface, pygame.Color(
                                255, 255, 0),
                            test_rect, 5)
                elif ([i, j] in self.board.freezing_locations):
                    test_rect = pygame.Rect(
                        block_width*j, block_height*i, block_width, block_height)
                    if (self.grid[i][j] in self.jewel_list):
                        color = self.color_list[self.jewel_list.index(
                            self.grid[i][j])]
                        pygame.draw.rect(
                            surface, pygame.Color(
                                0, 0, 0),
                            test_rect, 5)
                else:
                    test_rect = pygame.Rect(
                        block_width*j, block_height*i, block_width, block_height)
                    if (self.grid[i][j] in self.jewel_list):
                        color = self.color_list[self.jewel_list.index(
                            self.grid[i][j])]
                        pygame.draw.rect(
                            surface, pygame.Color(
                                color[0], color[1], color[2]),
                            test_rect)

    def _create_board(self) -> Board:
        '''creates the board with the global rows and cols variable'''
        return Board(ROWS, COLS)

    def _create_random_faller(self) -> [str]:
        '''creates a list of three random letters (jewels)'''
        jewel_list_length = len(self.jewel_list)
        faller = []
        for i in range(3):
            faller.append(
                self.jewel_list[(random.randint(0, jewel_list_length-1))])
        return faller


if __name__ == '__main__':
    Game().run()
