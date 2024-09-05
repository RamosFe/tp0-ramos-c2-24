from typing import List, Optional

from server.common.bet import Bet, load_bets, has_won, store_bets

EXPECTED_AGENCIES = 5



class LotteryState:
    def __init__(self, expected_agencies: int = EXPECTED_AGENCIES):
        """Initialize the LotteryState with the expected number of agencies.

        Args:
            expected_agencies (int): The expected number of agencies. Defaults to EXPECTED_AGENCIES.
        """
        self.expected_agencies = expected_agencies
        self.agencies_finished = 0
        self.lottery_results: Optional[List[Bet]] = None

    def store_bets(self, bets: List[Bet]):
        store_bets(bets)

    def agency_finished(self):
        """Increment the count of finished agencies and check if all agencies have finished.
        If all agencies have finished, set the winners.
        """
        self.agencies_finished += 1

        if self.check_all_finished():
            self.set_winners()

    def check_all_finished(self) -> bool:
        """Check if all expected agencies have finished.

        Returns:
            bool: True if all agencies have finished, False otherwise.
        """
        return self.expected_agencies == self.agencies_finished

    def has_winners(self) -> bool:
        """Check if there are winners available.

        Returns:
            bool: True if there are winners, False otherwise.
        """
        return self.lottery_results is not None

    def set_winners(self):
        """Determine winners from the loaded bets and store the results."""
        winners = []
        bets = load_bets()

        for bet in bets:
            if has_won(bet):
                winners.append(bet)

        self.lottery_results = winners

    def get_winners_by_agency(self, agency_id: int) -> List[Bet]:
        """Get a list of winners for a specific agency.

        Args:
            agency_id (int): The ID of the agency to get winners for.

        Returns:
            List[Bet]: A list of Bet objects for the specified agency. Empty if no winners.
        """
        if self.has_winners():
            return [bet for bet in self.lottery_results if bet.agency == agency_id]
        else:
            return []
