import enum
import struct
import socket
from typing import Literal

from server.utils.socket import read_from_socket

class MessageType(int, enum.Enum):
    """
    Enum for defining message types.

    Attributes:
        SEND_BET: Message type representing a send bet action.
    """
    SEND_BET = 0

class Message:
    """
    A class representing a message with a type, size, and payload.

    Attributes:
        MSG_TYPE_SIZE (int): Size of the message type field in bytes.
        HEADER_SIZE (int): Size of the header field in bytes.
        ENDIAN (Literal["little", "big"]): Byte order used for encoding/decoding data.
    """
    MSG_TYPE_SIZE = 1
    HEADER_SIZE = 2
    ENDIAN: Literal["little", "big"] = "big"

    def __init__(self, msg_type: MessageType, size: int, payload: bytes):
        """
        Initializes a Message instance with a given type, size, and payload.

        Args:
            msg_type (MessageType): The type of the message.
            size (int): The size of the payload in bytes.
            payload (bytes): The payload data.
        """
        self.msg_type = msg_type
        self.size = size
        self.payload = payload

    def to_bytes(self) -> bytes:
        """
        Converts the message to a byte representation.

        Returns:
            bytes: The byte representation of the message, including the type, size, and payload.
        """
        msg_type_bytes = struct.pack('>B', self.msg_type.value)
        header_bytes = struct.pack('>H', self.size)
        return msg_type_bytes + header_bytes + self.payload

    @classmethod
    def from_socket(cls, socket: socket.socket):
        """
        Creates a Message instance by reading data from a socket.

        Args:
            socket (socket.socket): The socket from which to read the message data.

        Returns:
            Message: An instance of Message created from the data read from the socket.
        """
        msg_type = read_from_socket(socket, Message.MSG_TYPE_SIZE)
        payload_size = read_from_socket(socket, Message.HEADER_SIZE)
        payload_size_int = int.from_bytes(payload_size, Message.ENDIAN)
        payload = read_from_socket(socket, payload_size_int)

        return cls(MessageType(msg_type[0]), payload_size_int, payload)
