import socket
import logging
import signal
from typing import List

from server.common.winners import Winners, AskWinner
from server.common.bet import Bet
from server.common.processes import StateManager

from server.protocol.flag import ResponseFlag, FlagType
from server.protocol.identifier import Identifier, ProtocolType
from server.protocol.message import Message, MessageType
from server.utils.socket import write_to_socket


class Server:
    def __init__(self, port, listen_backlog):
        # State
        self._shutdown: bool = False
        self._state = StateManager()
        # TODO - Delete when handling multiprocesses
        self._active_sockets: List[socket] = []

        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        # Define signal handlers
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _close_all_active_sockets(self):
        """Close all active client sockets and log the action."""
        # TODO - Delete this when handling multiprocessing
        for client_socket in self._active_sockets:
            addr = client_socket.getpeername()
            logging.info(f'action: close client socket | result: success | ip: {addr[0]}')
            client_socket.close()

    def _handle_signal(self, signum, stack):
        """Handle termination signals to shut down the server.

        Args:
            signum (int): The signal number.
            stack (object): The stack frame where the signal was received.
        """
        logging.info(f'action: signal_handler | result: success | signal: {signum}')
        self._shutdown = True

        self._server_socket.close()
        logging.debug(f'action: close server socket | result: success')

        self._close_all_active_sockets()

    def run(self):
        """Run the server loop to accept and handle client connections."""
        while not self._shutdown:
            try:
                client_sock = self.__accept_new_connection()
                # TODO - Delete when handling multiprocessing
                self._active_sockets.append(client_sock)
                self.__handle_client_connection(client_sock)
                # TODO - Delete when handling multiprocessing
                self._active_sockets.remove(client_sock)
            except OSError as e:
                if self._shutdown:
                    logging.info(f'action: receive_sigterm | result: success | msg: breaking server loop')
                else:
                    logging.error(f'action: accept_connection | result: fail | error: {e}')

    def __handle_client_connection(self, client_sock):
        """Read messages from a client socket and close the socket when done.

        Args:
            client_sock (socket.socket): The client socket to handle.
        """
        try:
            addr = client_sock.getpeername()
            while True:
                identifier = Identifier.from_socket(client_sock)

                if identifier.type == ProtocolType.TypeMessage:
                    finish_connection = self._handle_message(client_sock)
                    if finish_connection:
                        break
                elif identifier.type == ProtocolType.TypeFlag:
                    flag = ResponseFlag.from_socket(client_sock)
                    if flag.flag_type == FlagType.END:
                        self._state.lottery_state.agency_finished()
                        logging.info(f'action: receive_end | result: success | ip: {addr[0]}')
                        if self._state.lottery_state.has_winners():
                            logging.info(f'action: sorteo | result: success')
                        break
                else:
                    logging.error(f"action: receive_message | result: fail | error: unexpected type {identifier}")
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            client_sock.close()

    def _handle_message(self, client_sock: socket.socket) -> bool:
        """ Handle a message from the client and determine if the connection should be finished.

        Args:
            client_sock (socket.socket): The client socket to handle.

        Returns:
            bool: True if the connection should be finished, False otherwise.
        """
        msg = Message.from_socket(client_sock)
        if msg.msg_type == MessageType.SEND_BET:
            self._handle_bet(client_sock, msg)
            return False
        elif msg.msg_type == MessageType.ASK_WINNERS:
            self._handle_ask_winners(client_sock, msg)
            return True

    def _handle_bet(self, client_sock: socket.socket, msg: Message):
        """Process a bet message from the client.

        Args:
            client_sock (socket.socket): The client socket that sent the message.
            msg (Message): The message containing the bet data.
        """
        try:
            bets = Bet.from_multiple_str(msg.payload.decode('utf-8'))
            logging.info(f'action: apuesta_recibida | result: success | cantidad: {len(bets)}')

            self._state.lottery_state.store_bets(bets)
            write_to_socket(client_sock, ResponseFlag.ok().to_bytes())
        except Exception as e:
            # Respond with an error flag
            write_to_socket(client_sock, ResponseFlag.error().to_bytes())
            logging.error(f'action: apuesta_procesada | result: fail | error: {e}')
            raise e

    def _handle_ask_winners(self, client_sock: socket.socket, msg: Message):
        """Handle a request for winners and send the appropriate response.

        Args:
            client_sock (socket.socket): The client socket that sent the request.
            msg (Message): The message containing the request data.
        """
        try:
            ask_winners = AskWinner.from_bytes(msg.payload)
            agency_id = ask_winners.agency_id

            if self._state.lottery_state.has_winners():
                winners_by_agency = self._state.lottery_state.get_winners_by_agency(agency_id)
                winners_documents = [bet.document for bet in winners_by_agency]
                winners_bytes = Winners(winners_documents).to_bytes()

                msg = Message(MessageType.SEND_WINNERS, len(winners_bytes), winners_bytes)
                write_to_socket(client_sock, msg.to_bytes())
                logging.info(f'action: send_winner | result: success | agency {agency_id}')
            else:
                msg = ResponseFlag(FlagType.NO_WINNERS)
                write_to_socket(client_sock, msg.to_bytes())
                logging.info(f'action: send_winner | result: not-available | agency {agency_id}')
        except Exception as e:
            logging.error(f'action: ask_winner | result: fail | error {e}')
            raise e

    def __accept_new_connection(self):
        """Accept a new connection from a client.

        Returns:
            socket.socket: The accepted client socket.
        """
        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c
