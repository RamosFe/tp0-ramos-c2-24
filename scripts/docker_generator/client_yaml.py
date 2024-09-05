class ClientDefinition:
    """
    A class to define and generate YAML configurations for a client service.
    """

    def __init__(self, client_number: int, log_level: str = "DEBUG"):
        """
        Initializes the ClientDefinition with a client number and logging level.

        Args:
            client_number (int): The unique identifier for the client.
            log_level (str): The logging level for the client. Defaults to "DEBUG".
        """
        self._number = client_number
        self._log_level = log_level

    def get_client_name(self) -> str:
        """
        Generates the client name based on the client number.

        Returns:
            str: The name of the client.
        """
        return f"client{self._number}"

    def get_yaml(self) -> str:
        """
        Generates the YAML configuration for the client service.

        Returns:
            str: The YAML configuration for the client service.
        """
        client_name = self.get_client_name()
        return (
            f"  {client_name}:\n"
            f"    container_name: {client_name}\n"
            f"    image: client:latest\n"
            f"    entrypoint: /client\n"
            f"    environment:\n"
            f"      - CLI_ID={self._number}\n"
            f"    networks:\n"
            f"      - testing_net\n"
            f"    depends_on:\n"
            f"      - server\n\n"
            f"    volumes:\n"
            f"      - ./client/config.yaml:/config.yaml\n"
        )
