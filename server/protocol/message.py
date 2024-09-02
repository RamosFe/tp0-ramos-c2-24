import socket
import struct
import enum
from typing import Literal

from server.utils.socket import read_from_socket


class MessageType(int, enum.Enum):
    SEND_BET = 0

class Message:
    MSG_TYPE_SIZE = 1
    HEADER_SIZE = 2
    ENDIAN: Literal["little", "big"] = "big"

    def __init__(self, msg_type: MessageType, size: int, payload: bytes):
        self.msg_type = msg_type
        self.size = size
        self.payload = payload

    def to_bytes(self) -> bytes:
        msg_type_bytes = struct.pack('>B', self.msg_type.value)
        header_bytes = struct.pack('>H', self.size)
        return msg_type_bytes + header_bytes + self.payload

    @classmethod
    def from_socket(cls, socket: socket.socket):
        msg_type = read_from_socket(socket, Message.MSG_TYPE_SIZE)
        payload_size = read_from_socket(socket, Message.HEADER_SIZE)
        payload_size_int = int.from_bytes(payload_size, Message.ENDIAN)
        payload = read_from_socket(socket, payload_size_int)

        return cls(MessageType(msg_type[0]), payload_size_int, payload)
