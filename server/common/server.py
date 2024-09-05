import socket
import logging
import signal
from typing import List

from server.common.processes import StateManager, ClientProcess


class Server:
    def __init__(self, port, listen_backlog):
        # State
        self._shutdown: bool = False
        self._state = StateManager()
        self._list_of_processes: List[ClientProcess] = []

        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        # Define signal handlers
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

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

        self._terminate_client_processes()
        self._state.terminate()

    def _terminate_client_processes(self):
        for process in self._list_of_processes:
            process.terminate()
            process.join()


    def run(self):
        """Run the server loop to accept and handle client connections."""
        while not self._shutdown:
            try:
                client_sock = self.__accept_new_connection()
                new_client_process = ClientProcess(client_sock, self._state.lottery_state)
                new_client_process.start()
                self._list_of_processes.append(new_client_process)
            except OSError as e:
                if self._shutdown:
                    logging.info(f'action: receive_sigterm | result: success | msg: breaking server loop')
                else:
                    logging.error(f'action: accept_connection | result: fail | error: {e}')

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
