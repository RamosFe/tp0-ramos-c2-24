from typing import List

from cli import create_parser
from client_yaml import ClientDefinition
from services_yaml import ServicesDefinition


if __name__ == "__main__":
    parser = create_parser()

    args = parser.parse_args()
    number = args.number
    filename = args.file

    clients: List[str] = []
    for i in range(1, number + 1):
        clients.append(ClientDefinition(i).get_yaml())
    clients_yaml = "".join(clients)

    service = ServicesDefinition()
    with open(filename, 'w') as file:
        file.write(service.get_yaml(clients_yaml))
