from gamelogic import Board


def interface():
    #rows = input()
    rows = 4
    #cols = input()
    cols = 3
    #initial = input()
    initial = 'EMPTY'
    board = starting_board(rows, cols, initial)
    board.print_board()
    while (not (board.game_over)):
        action = input()
        # board.print_board()
        if (action.startswith('F')):
            action_arr = action.split()
            key_column = int(action_arr[1])
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


def starting_board(rows, cols, initial):
    if (initial == 'EMPTY'):
        return Board(rows, cols)
    else:
        print('Not valid. Try again.')
        return starting_board(rows, cols, input())


def quit_game(action, board):
    board.game_over = True
    return board


if __name__ == '__main__':
    interface()
