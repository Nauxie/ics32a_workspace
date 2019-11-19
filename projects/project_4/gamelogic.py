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

    def print_board(self):
        for i in range(len(self.board)):
            print('|', end='')
            for j in range(len(self.board[i])):
                if (self.board[i][j] == 0):
                    print('   ', end='')
                elif(self.faller_active and ([i, j] in self.faller_locations)):
                    print('[' + self.board[i][j] + ']', end='')
                else:
                    print(' ' + self.board[i][j] + ' ', end='')
            print('|', end='')
            print()
        print(' ', '-' * ((3)*(self.cols)), ' ', sep='')

    def end_game(self):
        self.game_over == True

    def handle_faller_generation(self, col, faller):
        self.faller_active = True
        self.current_faller = list(faller)
        added_zeroes = self.rows-len(self.current_faller)
        for i in range(added_zeroes):
            self.current_faller.insert(0, 0)
        self.faller_col = col - 1
        self.insert_from_top(self.current_faller[-1], self.faller_col)
        self.iterator = len(self.current_faller)-2
        print(self.current_faller)

    def handle_blank(self):
        if self.faller_active:
            self.insert_from_top(
                self.current_faller[self.iterator], self.faller_col)
            self.iterator -= 1

    def insert_from_top(self, value, col):
        if (self.board[self.rows-1][col] == 0):
            for i in range(self.rows-1, 0, -1):
                self.board[i][col] = self.board[i-1][col]
                if (self.board[i][col] != 0):
                    self.faller_locations.append([i, col])
            self.board[0][col] = value
        else:
            self.faller_active = False
            self.faller_locations = []


def create_array(row, col):
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
