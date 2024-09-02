import socket
import struct
import enum

from server.utils.socket import read_from_socket

class FlagType(int, enum.Enum):
    OK = 0
    ERROR = 1


class ResponseFlag:
    FLAG_TYPE_SIZE = 1

    def __init__(self, flag_type: FlagType):
        self.flag_type = flag_type

    def to_bytes(self) -> bytes:
        flag_type_bytes = struct.pack('>B', self.flag_type)
        return flag_type_bytes

    @classmethod
    def from_socket(cls, socket: socket.socket):
        flag_type = read_from_socket(socket, ResponseFlag.FLAG_TYPE_SIZE)

        return cls(FlagType(flag_type[0]))

    @classmethod
    def ok(cls):
        return cls(FlagType.OK)

    @classmethod
    def error(cls):
        return cls(FlagType.ERROR)