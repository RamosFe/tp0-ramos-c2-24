import socket


def write_to_socket(socket: socket.socket, msg: bytes):
    data_sent = 0
    while data_sent < len(msg):
        bytes_sent = socket.send(msg[data_sent:])
        if bytes_sent == 0:
            raise OSError("connection was closed")

        data_sent += bytes_sent

def read_from_socket(socket: socket.socket, size: int) -> bytes:
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