import csv
import datetime


""" Bets storage location. """
STORAGE_FILEPATH = "./bets.csv"
""" Simulated winner number in the lottery contest. """
LOTTERY_WINNER_NUMBER = 7574


""" A lottery bet registry. """
class Bet:
    def __init__(self, agency: str, first_name: str, last_name: str, document: str, birthdate: str, number: str):
        """
        agency must be passed with integer format.
        birthdate must be passed with format: 'YYYY-MM-DD'.
        number must be passed with integer format.
        """
        self.agency = int(agency)
        self.first_name = first_name
        self.last_name = last_name
        self.document = document
        self.birthdate = datetime.date.fromisoformat(birthdate)
        self.number = int(number)


    @staticmethod
    def from_str(data: str):
        """
        Creates a Bet instance from a comma-separated string.

        Args:
            data (str): A comma-separated string with the format:
                'first_name,last_name,document,birthdate,number,agency'

        Returns:
            Bet: An instance of Bet created from the string data.

        Raises:
            ValueError: If the input string does not contain exactly 6 comma-separated values.
        """
        separated_str = data.split(',')
        if len(separated_str) != 6:
            raise ValueError(f'Invalid message: {data}')

        return Bet(
            first_name=separated_str[0],
            last_name=separated_str[1],
            document=separated_str[2],
            birthdate=separated_str[3],
            number=separated_str[4],
            agency=separated_str[5]
        )

    @classmethod
    def from_multiple_str(cls, data:str):
        list_of_bets = []
        separate_bets = data.split('\n')

        for value in separate_bets:
            list_of_bets.append(Bet.from_str(value))

        return list_of_bets

""" Checks whether a bet won the prize or not. """
def has_won(bet: Bet) -> bool:
    return bet.number == LOTTERY_WINNER_NUMBER

"""
Persist the information of each bet in the STORAGE_FILEPATH file.
Not thread-safe/process-safe.
"""
def store_bets(bets: list[Bet]) -> None:
    with open(STORAGE_FILEPATH, 'a+') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        for bet in bets:
            writer.writerow([bet.agency, bet.first_name, bet.last_name,
                             bet.document, bet.birthdate, bet.number])

"""
Loads the information all the bets in the STORAGE_FILEPATH file.
Not thread-safe/process-safe.
"""
def load_bets() -> list[Bet]:
    with open(STORAGE_FILEPATH, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            yield Bet(row[0], row[1], row[2], row[3], row[4], row[5])

