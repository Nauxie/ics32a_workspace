import connectfour
import connectfour_functions
import socket
from collections import namedtuple
from server_functions import read_host,read_port,connect,send_message,send_first_message,receive_response, close_connection, PollingConnection, ProtocolError



def user_interface() -> None:
    '''function that is run to print out the user interface'''
    host = read_host()
    #host = 'circinus-32.ics.uci.edu'
    port = read_port()
    #port = 4444
    print('Connecting to {} (port {})...'.format(host, port))
    try:
        poll_connection = connect(host, port)
        print('Connected!')
        send_first_message(poll_connection)
        print(receive_response(poll_connection))
        game_select = 'AI_GAME'
        send_message(poll_connection,game_select)
        print(receive_response(poll_connection))
        game = connectfour.new_game()
        while (connectfour.winner(game) == connectfour.NONE):
            while (game.turn == connectfour.RED):
                action = input()
                action_split = action.split() 
                if (len(action_split) == 1 or action_split[0] != 'DROP' and action_split[0] != 'POP'):
                    print('Wrong input format. Try again.')
                elif (int(action_split[1]) > 7 or int(action_split[1]) < 1):
                    send_message(poll_connection,action)
                    print(receive_response(poll_connection))
                    print(receive_response(poll_connection))
                else:
                    send_message(poll_connection,action)
                    game = connectfour_functions.handle_drop_pop(game,action)
                    connectfour_functions.print_game_state(game)

            while (game.turn == connectfour.YELLOW):
                okay = receive_response(poll_connection)
                if (okay == 'OKAY'):
                    print(okay)
                else:
                    raise ProtocolError
                
                action = receive_response(poll_connection)
                print(action)
                print(receive_response(poll_connection))
                game = connectfour_functions.handle_drop_pop(game,action)
                connectfour_functions.print_game_state(game)
        close_connection(poll_connection)
    except OSError:
        print('There was an OSError')
    except ProtocolError:
        close_connection(poll_connection)
        print('The server sent invalid input.')
                
                


if __name__ == '__main__':
    user_interface()


#circinus-32.ics.uci.edu