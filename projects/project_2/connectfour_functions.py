import connectfour


def print_game_state(state : connectfour.GameState) -> None:
    '''prints the current game state for the user to view'''
    for i in range(1,8):
        print(i, end='  ')
    print()   
    for i in range(connectfour.BOARD_ROWS):
        for j in range(connectfour.BOARD_COLUMNS):
            
            if (state.board[j][i] == connectfour.NONE):
                print('.',end='  ')
            elif (state.board[j][i] == connectfour.RED):
                print('R',end='  ')
            elif (state.board[j][i] == connectfour.YELLOW):
                print('Y',end='  ')

        print()

def handle_drop_pop(state: connectfour.GameState, action: str) -> connectfour.GameState:
    '''is called by the server and consolegame, and performs either the pop or drop action and returns the new gamestate'''
    action_split = action.split()
    if len(action_split) == 1:
        print('Wrong input format. Try again.')
        return handle_drop_pop(state,input())
    elif action_split[0] == 'DROP':
        try:
            state = connectfour.drop(state,int(action_split[1])-1)
            return state
        except (connectfour.InvalidMoveError, ValueError) as e:
            print('Invalid move. Try again.')
            return handle_drop_pop(state,input())
    elif action_split[0] == 'POP':
        try:
            state = connectfour.pop(state,int(action_split[1])-1)
            return state
        except (connectfour.InvalidMoveError, ValueError) as e:    
            print('Invalid move. Try again.')
            return handle_drop_pop(state,input())
    else:
        print('Wrong input format. Try again.')
        return handle_drop_pop(state,input())
