import socket
import logging

def write_to_socket(socket: socket.socket, msg: bytes):
    """
    Writes bytes to the socket until all data is sent.

    Args:
        socket (socket.socket): The socket to which the data will be sent.
        msg (bytes): The byte data to send.

    Raises:
        OSError: If the connection is closed before all data is sent.
    """
    data_sent = 0
    while data_sent < len(msg):
        bytes_sent = socket.send(msg[data_sent:])
        if bytes_sent == 0:
            raise OSError("connection was closed")

        data_sent += bytes_sent

def read_from_socket(socket: socket.socket, size: int) -> bytes:
    """
    Reads bytes from the socket until the specified amount of data is received.

    Args:
        socket (socket.socket): The socket from which to read data.
        size (int): The number of bytes to read.

    Returns:
        bytes: The data read from the socket.

    Raises:
        OSError: If the connection is closed before the specified amount of data is read.
    """
    buffer = []
    data_read = 0

    while data_read < size:
        expected_size = size - data_read
        data = socket.recv(expected_size)
        if data == b'':
            raise OSError("connection was closed")

        data_read += len(data)
        buffer.append(data)

    return b''.join(buffer)
