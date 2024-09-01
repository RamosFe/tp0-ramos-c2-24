import textwrap

class ClientDefinition:
    def __init__(self, client_number: int, log_level: str = "DEBUG"):
        self._number = client_number
        self._log_level = log_level


    def get_client_name(self) -> str:
        return f"client{self._number}"

    def get_yaml(self) -> str:
        client_name = self.get_client_name()
        return (
            f"  {client_name}:\n"
            f"    container_name: {client_name}\n"
            f"    image: client:latest\n"
            f"    entrypoint: /client\n"
            f"    environment:\n"
            f"      - CLI_ID={self._number}\n"
            f"      - CLI_LOG_LEVEL={self._log_level}\n"
            f"    networks:\n"
            f"      - testing_net\n"
            f"    depends_on:\n"
            f"      - server\n\n"
        )
