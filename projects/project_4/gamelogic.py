from collections import deque


class Board:
    def __init__(self, rows, cols):
        self.rows = int(rows)
        self.cols = int(cols)
        self.board = create_array(self.rows, self.cols)
        self.game_over = False
        self.current_faller = []
        self.faller_active = False
        self.faller_locations = []
        self.faller_col = -1
        self.freezing_locations = []
        self.freezer_active = True

    def print_board(self):
        for i in range(len(self.board)):
            print('|', end='')
            for j in range(len(self.board[i])):
                if (self.board[i][j] == 0):
                    print('   ', end='')
                elif(self.faller_active and ([i, j] in self.faller_locations)):
                    print('[' + self.board[i][j] + ']', end='')
                elif(self.freezer_active and ([i, j] in self.freezing_locations)):
                    print('|' + self.board[i][j] + '|', end='')
                else:
                    print(' ' + self.board[i][j] + ' ', end='')
            print('|', end='')
            print()
        print(' ', '-' * ((3)*(self.cols)), ' ', sep='')

    def end_game(self):
        self.game_over == True

    def handle_faller_generation(self, col, faller):
        if (not self.faller_active):
            self.faller_active = True
            self.current_faller = list(faller)
            added_zeroes = self.rows-len(self.current_faller)
            for i in range(added_zeroes):
                self.current_faller.insert(0, 0)  # creates [0,'X','Y','Z']
            self.faller_col = col - 1  # Adjusts column to have 0 starting point
            # keeps track of where in the faller you are (starting at last element)
            self.iterator = len(self.current_faller)-1
            self.insert_from_top(
                self.current_faller[self.iterator], self.faller_col)  # insert Z at top

    def handle_blank(self):
        if self.faller_active:
            self.insert_from_top(
                self.current_faller[self.iterator], self.faller_col)
        elif self.freezer_active:
            self.freezer_active = False
            self.freezing_locations = []
            self.faller_locations = []

    def handle_matches(self):
        if (not self.faller_active):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    print(self.board[i][j], end=' ')
                    right_counter = 0
                print()

    def move_right(self):
        if (self.faller_active):
            right_clear = True
            for location in self.faller_locations:
                if (self.board[location[0]][location[1]+1] != 0):
                    right_clear = False
            if right_clear:
                self.faller_col += 1
                for location in self.faller_locations:
                    location[1] += 1
                for location in self.faller_locations:
                    self.board[location[0]][location[1]
                                            ] = self.board[location[0]][location[1]-1]
                    self.board[location[0]][location[1]-1] = 0
        elif (self.freezer_active):
            right_clear = True
            for location in self.freezing_locations:
                if (self.board[location[0]][location[1]+1] != 0):
                    right_clear = False
            if right_clear:
                self.faller_col += 1
                for location in self.freezing_locations:
                    location[1] += 1
                for location in self.freezing_locations:
                    self.board[location[0]][location[1]
                                            ] = self.board[location[0]][location[1]-1]
                    self.board[location[0]][location[1]-1] = 0

    def move_left(self):
        if (self.faller_active):
            left_clear = True
            for location in self.faller_locations:
                if (self.board[location[0]][location[1]-1] != 0):
                    left_clear = False
            if left_clear:  # if nothing left of it, then perform the transposition
                self.faller_col -= 1
                for location in self.faller_locations:
                    location[1] -= 1
                for location in self.faller_locations:
                    self.board[location[0]][location[1]
                                            ] = self.board[location[0]][location[1]+1]
                    self.board[location[0]][location[1]+1] = 0
        elif (self.freezer_active):
            left_clear = True
            for location in self.freezing_locations:
                if (self.board[location[0]][location[1]-1] != 0):
                    left_clear = False
            if left_clear:  # if nothing left of it, then perform the transposition
                self.faller_col -= 1
                for location in self.freezing_locations:
                    location[1] -= 1
                for location in self.freezing_locations:
                    self.board[location[0]][location[1]
                                            ] = self.board[location[0]][location[1]+1]
                    self.board[location[0]][location[1]+1] = 0

    def handle_rotate(self):
        items = deque(self.current_faller[-3:])
        items.rotate(1)
        self.current_faller = self.current_faller[:-3]
        self.current_faller.extend(list(items))
        print(self.current_faller)
        if (self.faller_active):
            print(self.faller_locations)
            for location in self.faller_locations:
                    # location = [0,2]
                self.board[location[0]][location[1]] = self.current_faller[-(
                    len(self.faller_locations))+self.faller_locations.index(location)]
        elif (self.freezer_active):
            for location in self.freezing_locations:
                # location = [0,2]
                self.board[location[0]][location[1]] = self.current_faller[-(
                    len(self.freezing_locations))+self.freezing_locations.index(location)]

    def insert_from_top(self, value, col) -> None:
        # value = 'Z'
        # col = 2
        if (self.board[self.rows-1][col] == 0):
            for i in range(self.rows-1, 0, -1):
                self.board[i][col] = self.board[i-1][col]
                if (self.board[i][col] != 0 and ([i, col] not in self.faller_locations)):
                    self.faller_locations.append([i, col])
                elif (self.board[i][col] == 0 and ([i, col] in self.faller_locations)):
                    self.faller_locations.remove([i, col])
            self.board[0][col] = value
            if (self.board[0][col] != 0 and ([0, col] not in self.faller_locations)):
                self.faller_locations.append([0, col])
            elif (self.board[0][col] == 0 and ([0, col] in self.faller_locations)):
                self.faller_locations.remove([0, col])
            self.iterator -= 1
            if (self.board[self.rows-1][col] != 0):
                self.faller_active = False
                self.freezer_active = True
                self.freezing_locations = self.faller_locations[:]
                self.faller_locations = []
        else:
            pass


def create_array(row, col) -> list:
    list_2d = []
    for i in range(row):
        inner_list = []
        for j in range(col):
            inner_list.append(0)
        list_2d.append(inner_list)
    return list_2d


if __name__ == '__main__':
    board = Board(8, 3)
    board.print_board()
    board.handle_faller_generation(3, ['X', 'Y', 'Z'])
    print(board.current_faller)
    for element in reversed(board.current_faller):
        board.insert_from_top(element, 2)
    board.print_board()
