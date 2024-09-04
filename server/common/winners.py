from typing import List

class Winners:
    def __init__(self, documents: List[str]):
        """Initialize the Winners with a list of document strings.

        Args:
            documents (List[str]): List of document strings.
        """
        self._documents = documents

    def to_bytes(self) -> bytes:
        """Convert the Winners instance to a bytes representation.

        Returns:
            bytes: Byte representation of the Winners, including the count and documents.
        """
        size = len(self._documents)
        joined = f'{size}' + ','.join(self._documents)
        return joined.encode('utf-8')

class AskWinner:
    AGENCY_ID_SIZE = 1

    def __init__(self, agency_id: int):
        """Initialize the AskWinner with an agency ID.

        Args:
            agency_id (int): The ID of the agency.
        """
        self.agency_id = agency_id

    @classmethod
    def from_bytes(cls, data: bytes):
        """Create an AskWinner instance from bytes data.

        Args:
            data (bytes): Byte data to decode into an AskWinner instance.

        Returns:
            AskWinner: An instance of AskWinner.

        Raises:
            ValueError: If the data length is invalid.
        """
        if len(data) != 1:
            raise ValueError("Invalid data length for AskWinner")
        agency_id = data[0]
        return cls(agency_id)
