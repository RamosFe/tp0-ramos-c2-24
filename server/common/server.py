import socket
import logging
import signal
from typing import List

from server.protocol.flag import ResponseFlag
from server.protocol.message import Message
from server.utils.socket import write_to_socket
from server.common.bet import Bet, store_bets


class Server:
    def __init__(self, port, listen_backlog):
        self._active_clients: List[socket.socket] = []
        self._shutdown: bool = False

        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        # Define signal handlers
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)


    def _add_active_socket(self, client_socket: socket.socket):
        self._active_clients.append(client_socket)

    def _remove_active_socket(self, client_socket: socket.socket):
        self._active_clients.remove(client_socket)

    def _close_all_active_sockets(self):
        for client_socket in self._active_clients:
            addr = client_socket.getpeername()
            logging.info(f'action: close client socket | result: success | ip: {addr[0]}')
            client_socket.close()


    def _handle_signal(self, signum, stack):
        logging.info(f'action: signal_handler | result: success | signal: {signum}')
        self._shutdown = True

        self._server_socket.close()
        logging.debug(f'action: close server socket | result: success')

        self._close_all_active_sockets()

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        # TODO: Modify this program to handle signal to graceful shutdown
        # the server
        while not self._shutdown:
            try:
                client_sock = self.__accept_new_connection()
                self._add_active_socket(client_sock)
                self.__handle_client_connection(client_sock)
                self._remove_active_socket(client_sock)
            except OSError as e:
                if self._shutdown:
                    logging.info(f'action: receive_sigterm | result: success | msg: breaking server loop')
                else:
                    logging.error(f'action: accept_connection | result: fail | error: {e}')

    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            msg = Message.from_socket(client_sock)
            bet = Bet.from_str(msg.payload.decode('utf-8'))
            addr = client_sock.getpeername()
            logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {str(msg.payload)}')
            store_bets([bet])
            write_to_socket(client_sock, ResponseFlag.ok().to_bytes())
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            client_sock.close()

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c
