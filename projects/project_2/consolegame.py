import connectfour
from connectfour_functions import print_game_state, handle_drop_pop


def run_program() -> None:
    '''runs the user interface'''
    currentState = connectfour.new_game()
    print('Welcome to Connect Four! Type DROP or POP then the column number to begin.')
    while (connectfour.winner(currentState) == connectfour.NONE):
        action = input()
        currentState = handle_drop_pop(currentState,action)
        print_game_state(currentState)
        #print(currentState.board)
    if (connectfour.winner(currentState) == 1):
        print('Red won!')
    if (connectfour.winner(currentState) == 2):
        print('Yellow won!')

if __name__ == '__main__':
    run_program()
    
    
