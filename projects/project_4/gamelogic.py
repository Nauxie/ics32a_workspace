from collections import deque


class Board:
    def __init__(self, rows: str, cols: str):
        '''constructor'''
        self.rows = int(rows)
        self.cols = int(cols)
        self.board = create_array(self.rows, self.cols)
        self.game_over = False
        self.current_faller = []
        self.faller_active = False
        self.faller_locations = []
        self.faller_col = -1
        self.freezing_locations = []
        self.freezer_active = False
        self.matching_locations = []
        self.matching_active = False
        self.iterator = 0
        self.early_game_over = False

    def idle_drop(self) -> None:
        '''converts a gamestate with holes into one where the jewels have dropped'''
        all_not_fallen = True
        while (all_not_fallen):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    try:
                        if (self.board[i][j] != 0 and self.board[i+1][j] == 0):
                            self.board[i+1][j] = self.board[i][j]
                            self.board[i][j] = 0
                    except(IndexError):
                        pass
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    try:
                        if (self.board[i][j] != 0 and self.board[i+1][j] == 0):
                            all_not_fallen = True
                            break
                    except (IndexError):
                        pass
                else:
                    continue
                break
            else:
                all_not_fallen = False
        if (not self.matching_active):
            self.handle_matches()

    def modify(self, initial_jewels: list) -> None:
        '''allows for the board to start with specified jewels'''
        for i in range(len(initial_jewels)):
            for j in range(len(initial_jewels[i])):
                if (initial_jewels[i][j] == ' '):
                    self.board[i][j] = 0
                else:
                    self.board[i][j] = initial_jewels[i][j]
        self.idle_drop()

    def print_board(self) -> None:
        '''prints current board'''
        for i in range(len(self.board)):
            print('|', end='')
            for j in range(len(self.board[i])):
                if (self.board[i][j] == 0):
                    print('   ', end='')
                elif(self.faller_active and ([i, j] in self.faller_locations)):
                    print('[' + self.board[i][j] + ']', end='')
                elif(self.freezer_active and ([i, j] in self.freezing_locations)):
                    print('|' + self.board[i][j] + '|', end='')
                elif([i, j] in self.matching_locations):
                    print('*' + self.board[i][j] + '*', end='')
                else:
                    print(' ' + self.board[i][j] + ' ', end='')
            print('|', end='')
            print()
        print(' ', '-' * ((3)*(self.cols)), ' ', sep='')

    def end_game(self) -> None:
        '''sets game over status to true'''
        self.game_over == True

    def handle_faller_generation(self, col: int, faller: list) -> None:
        '''takes in a faller and drops the first jewel'''
        if (not self.faller_active and not self.freezer_active):
            self.faller_active = True
            self.current_faller = list(faller)
            added_zeroes = self.rows-len(self.current_faller)+1
            for i in range(added_zeroes):
                self.current_faller.insert(0, 0)  # creates [0,'X','Y','Z']
            self.faller_col = col - 1  # Adjusts column to have 0 starting point
            # keeps track of where in the faller you are (starting at last element)
            self.iterator = len(self.current_faller)-1
            self.insert_from_top(
                self.current_faller[self.iterator], self.faller_col)  # insert Z at top

    def handle_blank(self) -> None:
        '''handles the blank input'''
        if self.faller_active:
            self.insert_from_top(
                self.current_faller[self.iterator], self.faller_col)
        elif self.freezer_active:
            self.freezer_active = False
            self.freezing_locations = []
            self.faller_locations = []
            self.handle_matches()
            try:
                if (self.current_faller[self.iterator] != 0):
                    self.handle_matches()
                    if (self.current_faller[self.iterator] != 0):
                        self.game_over = True
            except (IndexError):
                pass
        elif (self.matching_active):
            self.handle_matches()

    def handle_matches(self) -> None:
        '''handles matches if they exist'''
        if (not self.faller_active and not self.matching_active):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    individual_matches = []
                    try:
                        # horizontal sequence
                        checker = 1

                        while (self.board[i][j] != 0 and (self.board[i][j] == self.board[i][j+checker])):
                            if ([i, j] not in individual_matches):
                                individual_matches.append([i, j])
                            if ([i, j+checker] not in individual_matches):
                                individual_matches.append([i, j+checker])
                            checker += 1
                    except (IndexError):
                        pass
                    if (individual_matches != [] and len(individual_matches) > 2):
                        self.matching_locations.extend(individual_matches)
                        self.matching_locations = set(
                            tuple(element) for element in self.matching_locations)
                        self.matching_locations = [list(t) for t in set(
                            tuple(element) for element in self.matching_locations)]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    individual_matches = []
                    try:
                        # vertical sequence
                        checker = 1
                        while (self.board[i][j] != 0 and (self.board[i][j] == self.board[i+checker][j])):
                            if ([i, j] not in individual_matches):
                                individual_matches.append([i, j])
                            if ([i+checker, j] not in individual_matches):
                                individual_matches.append([i+checker, j])
                            checker += 1
                    except (IndexError):
                        pass
                    if (individual_matches != [] and len(individual_matches) > 2):
                        self.matching_locations.extend(individual_matches)
                        self.matching_locations = set(
                            tuple(element) for element in self.matching_locations)
                        self.matching_locations = [list(t) for t in set(
                            tuple(element) for element in self.matching_locations)]
            self.check_diagonals()  # all four diagonals sequence
            if (self.matching_locations != []):
                self.matching_active = True
        elif (self.matching_active == True):
            for location in self.matching_locations:
                self.board[location[0]][location[1]] = 0
                self.matching_locations = []
                self.matching_active = False
            self.idle_drop()

    def check_diagonals(self) -> None:
        '''checks for matches on all four diagonals'''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                individual_matches = []
                try:
                    checker = 1
                    while (self.board[i][j] != 0 and (self.board[i][j] == self.board[i+checker][j+checker])):
                        if ([i, j] not in individual_matches):
                            individual_matches.append([i, j])
                        if ([i+checker, j+checker] not in individual_matches):
                            individual_matches.append(
                                [i+checker, j+checker])
                        checker += 1
                except (IndexError):
                    pass
                if (individual_matches != [] and len(individual_matches) > 2):
                    self.matching_locations.extend(individual_matches)
                    self.matching_locations = set(
                        tuple(element) for element in self.matching_locations)
                    self.matching_locations = [list(t) for t in set(
                        tuple(element) for element in self.matching_locations)]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                individual_matches = []
                try:
                    checker = 1
                    while (self.board[i][j] != 0 and (self.board[i][j] == self.board[i-checker][j-checker])):
                        if ([i, j] not in individual_matches):
                            individual_matches.append([i, j])
                        if ([i-checker, j-checker] not in individual_matches):
                            individual_matches.append(
                                [i-checker, j-checker])
                        checker += 1
                except (IndexError):
                    pass
                if (individual_matches != [] and len(individual_matches) > 2):
                    self.matching_locations.extend(individual_matches)
                    self.matching_locations = set(
                        tuple(element) for element in self.matching_locations)
                    self.matching_locations = [list(t) for t in set(
                        tuple(element) for element in self.matching_locations)]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                individual_matches = []
                try:
                    checker = 1
                    while (self.board[i][j] != 0 and (self.board[i][j] == self.board[i-checker][j+checker])):
                        if ([i, j] not in individual_matches):
                            individual_matches.append([i, j])
                        if ([i-checker, j+checker] not in individual_matches):
                            individual_matches.append(
                                [i-checker, j+checker])
                        checker += 1
                except (IndexError):
                    pass
                if (individual_matches != [] and len(individual_matches) > 2):
                    self.matching_locations.extend(individual_matches)
                    self.matching_locations = set(
                        tuple(element) for element in self.matching_locations)
                    self.matching_locations = [list(t) for t in set(
                        tuple(element) for element in self.matching_locations)]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                individual_matches = []
                try:
                    checker = 1
                    while (self.board[i][j] != 0 and (self.board[i][j] == self.board[i+checker][j-checker])):
                        if ([i, j] not in individual_matches):
                            individual_matches.append([i, j])
                        if ([i+checker, j-checker] not in individual_matches):
                            individual_matches.append(
                                [i+checker, j-checker])
                        checker += 1
                except (IndexError):
                    pass
                if (individual_matches != [] and len(individual_matches) > 2):
                    self.matching_locations.extend(individual_matches)
                    self.matching_locations = set(
                        tuple(element) for element in self.matching_locations)
                    self.matching_locations = [list(t) for t in set(
                        tuple(element) for element in self.matching_locations)]

    def move_right(self) -> None:
        '''moves the faller right'''
        if (self.faller_active):
            right_clear = True
            for location in self.faller_locations:
                if ((location[1]+1 == self.cols) or self.board[location[0]][location[1]+1] != 0):
                    right_clear = False
            if right_clear:
                self.faller_col += 1
                for location in self.faller_locations:
                    location[1] += 1
                for location in self.faller_locations:
                    self.board[location[0]][location[1]
                                            ] = self.board[location[0]][location[1]-1]
                    self.board[location[0]][location[1]-1] = 0
                down_space = 0
                try:
                    down_space = self.board[self.faller_locations[-1]
                                            [0]+1][self.faller_locations[-1][1]]
                except(IndexError):
                    pass
                if (down_space != 0):
                    self.faller_active = False
                    self.freezer_active = True
                    self.freezing_locations = self.faller_locations[:]
                    self.faller_locations = []
        elif (self.freezer_active):
            right_clear = True
            for location in self.freezing_locations:
                if ((location[1]+1 == self.cols) or self.board[location[0]][location[1]+1] != 0):
                    right_clear = False
            if right_clear:
                self.faller_col += 1
                for location in self.freezing_locations:
                    location[1] += 1
                for location in self.freezing_locations:
                    self.board[location[0]][location[1]
                                            ] = self.board[location[0]][location[1]-1]
                    self.board[location[0]][location[1]-1] = 0
                down_space = 1
                try:
                    down_space = self.board[self.freezing_locations[-1]
                                            [0]+1][self.freezing_locations[-1][1]]
                except(IndexError):
                    pass
                if (down_space == 0):
                    self.freezer_active = False
                    self.faller_active = True
                    self.faller_locations = self.freezing_locations[:]
                    self.freezing_locations = []

    def move_left(self) -> None:
        'moves the faller left'
        if (self.faller_active):
            left_clear = True
            for location in self.faller_locations:
                if ((location[1]-1 < 0) or self.board[location[0]][location[1]-1] != 0):
                    left_clear = False
            if left_clear:  # if nothing left of it, then perform the transposition
                self.faller_col -= 1
                for location in self.faller_locations:
                    location[1] -= 1
                for location in self.faller_locations:
                    self.board[location[0]][location[1]
                                            ] = self.board[location[0]][location[1]+1]
                    self.board[location[0]][location[1]+1] = 0
                3
                down_space = 0
                try:
                    down_space = self.board[self.faller_locations[-1]
                                            [0]+1][self.faller_locations[-1][1]]
                except(IndexError):
                    pass
                if (down_space != 0):
                    self.faller_active = False
                    self.freezer_active = True
                    self.freezing_locations = self.faller_locations[:]
                    self.faller_locations = []
        elif (self.freezer_active):
            left_clear = True
            for location in self.freezing_locations:
                if ((location[1]-1 < 0) or self.board[location[0]][location[1]-1] != 0):
                    left_clear = False
            if left_clear:  # if nothing left of it, then perform the transposition
                self.faller_col -= 1
                for location in self.freezing_locations:
                    location[1] -= 1
                for location in self.freezing_locations:
                    self.board[location[0]][location[1]
                                            ] = self.board[location[0]][location[1]+1]
                    self.board[location[0]][location[1]+1] = 0
                down_space = 1
                try:
                    down_space = self.board[self.freezing_locations[-1]
                                            [0]+1][self.freezing_locations[-1][1]]
                except(IndexError):
                    pass
                if (down_space == 0):
                    self.freezer_active = False
                    self.faller_active = True
                    self.faller_locations = self.freezing_locations[:]
                    self.freezing_locations = []

    def handle_rotate(self) -> None:
        '''rotates the faller'''
        items = deque(self.current_faller[-3:])
        items.rotate(1)
        self.current_faller = self.current_faller[: -3]
        self.current_faller.extend(list(items))
        if (self.faller_active):
            for location in self.faller_locations:
                    # location = [0,2]
                self.board[location[0]][location[1]] = self.current_faller[-(
                    len(self.faller_locations))+self.faller_locations.index(location)]
        elif (self.freezer_active):
            for location in self.freezing_locations:
                # location = [0,2]
                self.board[location[0]][location[1]] = self.current_faller[-(
                    len(self.freezing_locations))+self.freezing_locations.index(location)]

    def insert_from_top(self, value: str, col: int) -> None:
        '''inserts a specified value into the specified column from the top'''
        # value = 'Z'
        # col = 2
        lowest_zero_row = 0
        for i in range(self.rows):
            if (self.board[i][col] == 0):
                lowest_zero_row = i
        if (self.board[lowest_zero_row][col] == 0):
            for i in range(lowest_zero_row, 0, -1):
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
            if (self.iterator > 0):
                self.iterator -= 1
            if (self.board[lowest_zero_row][col] != 0):
                self.faller_active = False
                self.freezer_active = True
                self.freezing_locations = self.faller_locations[:]
                self.faller_locations = []
        else:
            pass


def create_array(row: int, col: int) -> list:
    '''takes in a number of rows and columns and returns a 2d list of zeroes'''
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
