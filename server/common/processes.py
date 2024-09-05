import socket
import logging
import signal
from multiprocessing import Process
from multiprocessing.managers import SyncManager

from server.common.state import EXPECTED_AGENCIES, LotteryState
from server.common.bet import Bet
from server.common.winners import AskWinner, Winners

from server.protocol.identifier import Identifier, ProtocolType
from server.protocol.message import Message, MessageType
from server.protocol.flag import ResponseFlag, FlagType

from server.utils.socket import write_to_socket



class CustomServerProcessManager(SyncManager):
    pass

class StateManager:
    def __init__(self, expected_agencies: int = EXPECTED_AGENCIES):
        CustomServerProcessManager.register('LotteryState', LotteryState)

        self.manager = CustomServerProcessManager()
        self.manager.start()
        self.lottery_state = self.manager.LotteryState(expected_agencies)

    def terminate(self):
        self.manager.shutdown()
        self.manager.join()



class ClientProcess(Process):
    def __init__(self, client_socket: socket.socket, lottery_state: LotteryState):
        super().__init__()
        self.client_socket = client_socket
        self.lottery_state = lottery_state

        self.addr = self.client_socket.getpeername()[0]


    def _handle_signal(self, signum, stack):
        """Handle termination signals to shut down the client process.

        Args:
            signum (int): The signal number.
            stack (object): The stack frame where the signal was received.
        """
        self.client_socket.close()

    def run(self):
        # Define signal handlers
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

        try:
            while True:
                identifier = Identifier.from_socket(self.client_socket)

                if identifier.type == ProtocolType.TypeMessage:
                    finish_connection = self._handle_message()
                    if finish_connection:
                        break
                elif identifier.type == ProtocolType.TypeFlag:
                    flag = ResponseFlag.from_socket(self.client_socket)
                    if flag.flag_type == FlagType.END:
                        self.lottery_state.agency_finished()
                        logging.info(f'action: receive_end | result: success | ip: {self.addr}')
                        if self.lottery_state.has_winners():
                            logging.info(f'action: sorteo | result: success')
                        break
                else:
                    logging.error(f"action: receive_message | result: fail | error: unexpected type {identifier} | ip: {self.addr}")
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e} | ip: {self.addr}")
        finally:
            self.client_socket.close()

    def _handle_message(self) -> bool:
        msg = Message.from_socket(self.client_socket)
        if msg.msg_type == MessageType.SEND_BET:
            self._handle_bet(msg)
            return False
        elif msg.msg_type == MessageType.ASK_WINNERS:
            self._handle_ask_winners(msg)
            return True


    def _handle_bet(self, msg: Message):
        """Process a bet message from the client.

        Args:
            msg (Message): The message containing the bet data.
        """
        try:
            bets = Bet.from_multiple_str(msg.payload.decode('utf-8'))
            logging.info(f'action: apuesta_recibida | result: success | cantidad: {len(bets)} | ip: {self.addr}')

            self.lottery_state.store_bets(bets)
            write_to_socket(self.client_socket, ResponseFlag.ok().to_bytes())
        except Exception as e:
            # Respond with an error flag
            write_to_socket(self.client_socket, ResponseFlag.error().to_bytes())
            logging.error(f'action: apuesta_procesada | result: fail | error: {e} | ip: {self.addr}')
            raise e

    def _handle_ask_winners(self, msg: Message):
        """Handle a request for winners and send the appropriate response.

        Args:
            msg (Message): The message containing the request data.
        """
        try:
            ask_winners = AskWinner.from_bytes(msg.payload)
            agency_id = ask_winners.agency_id

            if self.lottery_state.has_winners():
                winners_by_agency = self.lottery_state.get_winners_by_agency(agency_id)
                winners_documents = [bet.document for bet in winners_by_agency]
                winners_bytes = Winners(winners_documents).to_bytes()

                msg = Message(MessageType.SEND_WINNERS, len(winners_bytes), winners_bytes)
                write_to_socket(self.client_socket, msg.to_bytes())
                logging.info(f'action: send_winner | result: success | agency {agency_id} | ip: {self.addr}')
            else:
                msg = ResponseFlag(FlagType.NO_WINNERS)
                write_to_socket(self.client_socket, msg.to_bytes())
                logging.info(f'action: send_winner | result: not-available | agency {agency_id} | ip: {self.addr}')
        except Exception as e:
            logging.error(f'action: ask_winner | result: fail | error {e} | ip: {self.addr}')
            raise e
