from multiprocessing.managers import SyncManager

from server.common.state import EXPECTED_AGENCIES, LotteryState

class CustomServerProcessManager(SyncManager):
    pass

class StateManager:
    def __init__(self, expected_agencies: int = EXPECTED_AGENCIES):
        CustomServerProcessManager.register('LotteryState', LotteryState)

        self.manager = CustomServerProcessManager()
        self.manager.start()
        self.lottery_state = self.manager.LotteryState(expected_agencies)
