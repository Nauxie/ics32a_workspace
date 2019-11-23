from gamelogic import Board

jewel_list = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']


def interface() -> None:
    '''runs main interface'''
    rows = input()
    #rows = 4
    cols = input()
    #cols = 3
    initial = input()
    #initial = 'EMPTY'
    board = starting_board(rows, cols, initial)
    board.print_board()
    while (not (board.game_over) and not (board.early_game_over)):
        action = input()
        # board.print_board()
        if (action.startswith('F')):
            action_arr = action.split()
            key_column = int(action_arr[1])
            if (action_arr[2] in jewel_list and action_arr[3] in jewel_list and action_arr[4] in jewel_list):
                faller_tuple = (action_arr[2], action_arr[3], action_arr[4])
                board.handle_faller_generation(key_column, faller_tuple)
                board.print_board()
        elif (action == ''):
            board.handle_blank()
            board.print_board()
        elif (action.strip() == '>'):
            board.move_right()
            board.print_board()
        elif (action.strip() == '<'):
            board.move_left()
            board.print_board()
        elif (action == 'R'):
            board.handle_rotate()
            board.print_board()
        elif (action == 'M'):
            board.handle_matches()
            board.print_board()
        elif (action.startswith('Q')):
            board = quit_game(action, board)
    if (board.game_over):
        print('GAME OVER')


def starting_board(rows: str, cols: str, initial: str) -> Board:
    '''takes in a number of rows and cols and an initial phrase to return the initial board'''
    if (initial == 'EMPTY'):
        return Board(rows, cols)
    elif (initial == 'CONTENTS'):
        initial_jewels = []
        for i in range(int(rows)):
            initial_jewels.append(input())
        board = Board(rows, cols)
        board.modify(initial_jewels)
        return board

    else:
        print('Not valid. Try again.')
        return starting_board(rows, cols, input())


def quit_game(action: str, board: Board) -> Board:
    '''quits the game with action Q, returns board with game over'''
    board.early_game_over = True
    return board


if __name__ == '__main__':
    interface()
