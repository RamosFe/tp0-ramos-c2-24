import argparse

def check_number(value: str) -> int:
    """
    Validates and converts a string input to an integer.

    Args:
        value (str): The string representation of the number to check.

    Returns:
        int: The integer value if it is greater than 0.

    Raises:
        argparse.ArgumentTypeError: If the value is not a valid integer or is less than or equal to 0.
    """
    int_to_check = int(value)
    if int_to_check < 0:
        raise argparse.ArgumentTypeError(f"Invalid number: {value}. The number must be greater than 0 or equal.")
    return int_to_check

def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for generating a docker-compose file with a specified number of clients.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
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
