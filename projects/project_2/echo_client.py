# echo_client.py
#
# ICS 32A Fall 2019
# Code Example
#
# As we saw in lecture, we can ask a socket object to give us a
# "pseudo-file object," an object that behaves just like a file
# object, except that it reads or writes to the socket's underlying
# streams, instead of to a file.  We end up needing two of them: one that
# reads from the socket's input stream and another that writes to its
# output stream.  Once we have them, we can treat our socket a lot like
# a text file, using techniques we already know.
#
# On the other hand, this leaves us with three separate objects to manage:
# the socket, the pseudo-file object for reading, and the pseudo-file
# object for writing.  Our best move is to collect these into one data
# structure, which we can pass around wherever we need it.  We opted for
# a tuple in lecture (and in this example), but we'll see in the next
# example that a better tool -- called a "namedtuple" -- would actually
# be a much better choice.

import socket



# The first few functions are centered around interacting with the user:
# asking for input and printing output in a clean form.  We keep these
# functions separate from the others, so that other functions become much
# simpler and more straightforward.


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



def read_message() -> str:
    '''
    Asks the user what message they'd like to send to the echo server.
    Any message is legitimate, including the empty string, so no validation
    is done, but this function still serves the purpose of encapsulating
    our decision about how to prompt the user.
    '''

    return input('Message: ')



def print_response(response: str) -> None:
    '''
    Prints the response sent back from the echo server, along with an
    appropriate prompt.
    '''

    print('Response: ' + response)



# The next few functions handle the conversation between our program and
# the echo server.  The goal is for other parts of our program to be
# completely insulated from the details of how these functions work.
# So when we connect, we return a "connection" object -- which is really a
# tuple consisting of a socket and two pseudo-file objects, but no code
# outside of these functions ever needs to know about that; as far as other
# functions are concerned, a connection is simply an opaque object that
# represents a connection to an echo serve.r


def connect(host: str, port: int) -> 'connection':
    '''
    Connects to the echo server, which is assumed to be running on the
    given host and listening on the given port.  If successful, a
    connection object is returned; if unsuccessful, an exception is
    raised.
    '''

    # Our first order of business is to create a socket and connect it
    # to the echo server.
    echo_socket = socket.socket()
    echo_socket.connect((host, port))

    # Next, because we know we plan to read and write text through our
    # socket, we create pseudo-file objects -- one for reading and one
    # for writing -- so we can read and write text through our socket
    # using the same basic interface we already learned for reading and
    # writing to text files.
    echo_socket_input = echo_socket.makefile('r')
    echo_socket_output = echo_socket.makefile('w')

    return echo_socket, echo_socket_input, echo_socket_output



def close(connection: 'connection') -> None:
    '''
    Closes a connection
    '''

    # Since a connection object is really a tuple, it's handy for us
    # to assign the tuple's values into three variables, so that the
    # variables can have meaningful names (as opposed to using an
    # unclear notation like connection[0], connection[1], and connection[2]).
    # Sequence assignment makes for a nice way to "unpack" the tuple and
    # name its elements.
    #
    # If this seems sort of silly to you, we'll clean this up in the next
    # example when we use a namedtuple for this instead, which will give
    # us what we want (a meaningful name for each object within the
    # connection object) without us having to do this every time.
    echo_socket, echo_socket_input, echo_socket_output = connection

    # Closing a connection requires closing the pseudo-file objects and
    # then closing the socket, so we'll do all of that here.
    echo_socket_input.close()
    echo_socket_output.close()
    echo_socket.close()



def send_message(connection: 'connection', message: str) -> None:
    '''
    Sends a message to the echo server via a connection that is already
    assumed to have been opened (and not yet closed).
    '''

    echo_socket, echo_socket_input, echo_socket_output = connection

    # There are a couple of details that we're handling here, so we
    # never have to remember to do them anywhere else
    #
    # (1) We're being sure to put the correct newline sequence on the
    #     end of the message.  This is the right place to do that, since
    #     this is the function that is in charge of sending messages to
    #     the server (so it's the natural place to handle the details of
    #     exactly how the server wants it to look).
    #
    # (2) We have to remember to "flush".  File objects do something called
    #     "buffering".  When you write to them, they store data in memory
    #     temporarily and then write it once in a while when the buffer
    #     runs out of space.  This is mainly done because the act of actually
    #     writing the data -- especially when you're talking about files on a
    #     hard disk, but even when you're using a socket -- is much slower
    #     than storing it in memory, so only writing data once in a while can
    #     dramatically reduce that cost.  But when you're talking to another
    #     program vi a socket, it's usually important that a message is sent
    #     *now*, because the other program won't know what to do until it is
    #     received.  So it becomes important to tell the file object "Take
    #     whatever is in your buffer and send it now!  Don't wait until a
    #     opportune time!"  That's what flush() does.
    echo_socket_output.write(message + '\r\n')
    echo_socket_output.flush()



def receive_response(connection: 'connection') -> None:
    '''
    Receives a response from the echo server via a connection that is
    already assumed to have been opened (and not yet closed).
    '''

    echo_socket, echo_socket_input, echo_socket_output = connection

    # When we call readline() on any file object (including a pseudo-file
    # object), we get back a newline character on the end of the line.
    # Here, we strip that newline off the end of the string using list
    # slicing, since this is a detail of how we interact with the echo
    # server, but not something that the rest of the program needs to be
    # concerned with.  Functions that have to do with interacting with the
    # server are the natural place to implement the details of how that
    # interaction works.
    return echo_socket_input.readline()[:-1]



# Finally, the main user interface of our program is implemented in the
# user_interface function below.  Notice that this function is a little
# bit longer, but that it's mainly in the business of calling other
# functions that we've already written.  So this functions reads a lot more
# like a high-level English description of what our program does, as opposed
# to overwhelming us with every detail.
#
# Our user interface asks the user to specify a host and a port, then asks
# the user repeatedly to specify a message to be sent, prints the response
# sent back by the echo server, and continues until the user enters an
# empty message.


def user_interface() -> None:
    host = read_host()
    port = read_port()

    print('Connecting to {} (port {})...'.format(host, port))
    connection = connect(host, port)
    print('Connected!')

    while True:
        message = read_message()

        if message == '':
            break
        else:
            send_message(connection, message)
            response = receive_response(connection)
            print_response(response)

    print('Closing connection...')
    close(connection)
    print('Closed!')



# When we run this module, it calls our user interface.

if __name__ == '__main__':
    user_interface()
