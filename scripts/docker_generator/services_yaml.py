import textwrap

class ServicesDefinition:
    """
    A class to define and generate YAML configurations for services.
    """

    def __init__(self, log_level: str = "DEBUG"):
        """
        Initializes the ServicesDefinition with a specified logging level.

        Args:
            log_level (str): The logging level for the service. Defaults to "DEBUG".
        """
        self._log_level = log_level

    def get_server_definition(self) -> str:
        """
        Generates the YAML configuration for the server service.

        Returns:
            str: The YAML configuration for the server service.
        """
        return (
            f"  server:\n"
            f"    container_name: server\n"
            f"    image: server:latest\n"
            f"    entrypoint: python3 /main.py\n"
            f"    environment:\n"
            f"      - PYTHONUNBUFFERED=1\n"
            f"    networks:\n"
            f"      - testing_net\n"
            f"    volumes:\n"
            f"      - ./server/config.ini:/config.ini\n"
        )

    def get_networks_definition(self) -> str:
        """
        Generates the YAML configuration for the networks.

        Returns:
            str: The YAML configuration for the networks.
        """
        networks_definition = textwrap.dedent(f"""
            networks:
              testing_net:
                ipam:
                  driver: default
                  config:
                    - subnet: 172.25.125.0/24
        """)

        return networks_definition

    def get_yaml(self, content: str) -> str:
        """
        Generates the complete YAML configuration including services and networks.

        Args:
            content (str): Additional YAML content to be included.

        Returns:
            str: The complete YAML configuration.
        """
        yaml_content = (
            "name: tp0\n"
            "services:\n"
        )

        full_yaml = (f"{yaml_content}"
                     f"{self.get_server_definition()}\n"
                     f"{content}"
                     f"{self.get_networks_definition()}")
        return full_yaml
