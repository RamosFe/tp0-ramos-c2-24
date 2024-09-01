import textwrap

class ServicesDefinition:
    def __init__(self, log_level: str = "DEBUG"):
        self._log_level = log_level

    def get_server_definition(self) -> str:
        return (
            f"  server:\n"
            f"    container_name: server\n"
            f"    image: server:latest\n"
            f"    entrypoint: python3 /main.py\n"
            f"    environment:\n"
            f"      - PYTHONUNBUFFERED=1\n"
            f"      - LOGGING_LEVEL={self._log_level}\n"
            f"    networks:\n"
            f"      - testing_net\n"
        )

    def get_networks_definition(self) -> str:
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
        yaml_content = (
            "name: tp0\n"
            "services:\n"
        )

        full_yaml = (f"{yaml_content}"
                     f"{self.get_server_definition()}\n"
                     f"{content}"
                     f"{self.get_networks_definition()}")
        return full_yaml