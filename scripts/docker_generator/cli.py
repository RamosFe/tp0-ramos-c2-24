import argparse

def check_number(value: str) -> int:
    int_to_check = int(value)
    if int_to_check <= 0:
        raise argparse.ArgumentTypeError(f"Invalid number: {value}. The number must be greater than 0.")
    return int_to_check

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Creates a docker-compose file with N clients")

    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="File name of the output file."
    )

    parser.add_argument(
        "-n", "--number",
        type=check_number,
        required=True,
        help="The number of clients to create for the docker-compose file."
    )

    return parser
