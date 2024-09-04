import socket
import struct
import enum

from server.protocol.identifier import Identifier, ProtocolType
from server.utils.socket import read_from_socket

class FlagType(int, enum.Enum):
    """
    Enum for defining response flag types.

    Attributes:
        OK (int): Represents a successful response.
        ERROR (int): Represents an error response.
        END (int): Represents the end of communication.
        NO_WINNERS (int): Represents that the winners aren't available
    """
    OK = 0
    ERROR = 1
    END = 2
    NO_WINNERS = 3

class ResponseFlag:
    """
    A class representing a response flag with a type.

    Attributes:
        FLAG_TYPE_SIZE (int): Size of the flag type field in bytes.
    """
    FLAG_TYPE_SIZE = 1

    def __init__(self, flag_type: FlagType):
        """
        Initializes a ResponseFlag instance with a given flag type.

        Args:
            flag_type (FlagType): The type of the flag.
        """
        self.identifier = Identifier(ProtocolType.TypeFlag)
        self.flag_type = flag_type

    def to_bytes(self) -> bytes:
        """
        Converts the response flag to a byte representation.

        Returns:
            bytes: The byte representation of the response flag.
        """
        flag_type_bytes = struct.pack('>B', self.flag_type)
        return self.identifier.to_bytes() +  flag_type_bytes

    @classmethod
    def from_socket(cls, socket: socket.socket):
        """
        Creates a ResponseFlag instance by reading data from a socket.

        Args:
            socket (socket.socket): The socket from which to read the flag data.

        Returns:
            ResponseFlag: An instance of ResponseFlag created from the data read from the socket.
        """
        flag_type = read_from_socket(socket, ResponseFlag.FLAG_TYPE_SIZE)

        return cls(FlagType(flag_type[0]))

    @classmethod
    def ok(cls):
        """
        Creates a ResponseFlag instance representing a successful response.

        Returns:
            ResponseFlag: An instance of ResponseFlag with the OK flag type.
        """
        return cls(FlagType.OK)

    @classmethod
    def error(cls):
        """
        Creates a ResponseFlag instance representing an error response.

        Returns:
            ResponseFlag: An instance of ResponseFlag with the ERROR flag type.
        """
        return cls(FlagType.ERROR)
