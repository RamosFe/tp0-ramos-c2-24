import enum
import socket
import struct

from server.utils.socket import read_from_socket


class ProtocolType(int, enum.Enum):
    TypeMessage = 0
    TypeFlag = 1

class Identifier:
    IDENTIFIER_TYPE_SIZE = 1

    def __init__(self, type: ProtocolType):
        self.type = type

    def to_bytes(self) -> bytes:
        type_bytes = struct.pack('>B', self.type.value)
        return type_bytes

    @classmethod
    def from_socket(cls, socket: socket.socket):
        type_bytes = read_from_socket(socket, Identifier.IDENTIFIER_TYPE_SIZE)

        return cls((ProtocolType(type_bytes[0])))
