from collections import namedtuple
import socket
PollingConnection = namedtuple('PollingConnection','socket input output')

class ProtocolError(Exception):
    pass


def read_host() -> str:
    '''
    Asks the user to specify what host they'd like to connect to,
    continuing to ask until a valid answer is given.  An answer is
    considered valid when it consists of something other than just
    spaces.
    '''

    while True:
        host = input('Host: ').strip()

        if host == '':
            print('Please specify a host (either a name or an IP address)')
        else:
            return host



def read_port() -> int:
    '''
    Asks the user to specify what port they'd like to connect to,
    continuing to ask until a valid answer is given.  A port must be an
    integer between 0 and 65535.
    '''

    while True:
        try:
            port = int(input('Port: ').strip())

            if port < 0 or port > 65535:
                print('Ports must be an integer between 0 and 65535')
            else:
                return port

        except ValueError:
            print('Ports must be an integer between 0 and 65535')

def connect(host: str, port: int) -> PollingConnection:
    '''
    Connects to the echo server, which is assumed to be running on the
    given host and listening on the given port.  If successful, a
    connection object is returned; if unsuccessful, an exception is
    raised.
    '''
    server_socket = socket.socket()
    server_socket.connect((host, port))
    socket_input = server_socket.makefile('r')
    socket_output = server_socket.makefile('w')

    return PollingConnection(server_socket,socket_input,socket_output)

def send_message(connection: PollingConnection, msg: str) -> None:
    '''general function to write to the output of a connection and then flush'''
    connection.output.write(msg + '\r\n')
    connection.output.flush()


def send_first_message(connection: PollingConnection) -> None:
    '''sends the first polling message to the server'''
    hello_msg = 'I32CFSP_HELLO'
    username = input('Please enter username: ').strip()
    msg = hello_msg + ' ' + username
    send_message(connection,msg)

def receive_response(connection: PollingConnection) -> str:
    '''general function to read the input of a connection'''
    return connection.input.readline()[:-1]

def close_connection(connection: PollingConnection) -> None:
    '''
    Closes a connection
    '''
    connection.input.close()
    connection.output.close()
    connection.socket.close()



#circinus-32.ics.uci.edu