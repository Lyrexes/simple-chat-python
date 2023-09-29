from socket import socket
from socket import MSG_DONTWAIT
from socket import MSG_PEEK
from threading import Thread


class Client:
    def __init__(self, host: str, port: int):
        self.is_running = True
        self.host = host
        self.port = port
        self.connection = socket()

    def connect(self) -> None:
        self.connection.connect((self.host, self.port))
        self.start_keyboard_input_thread()
        while self.is_connection_up() and self.is_running:
            message = self.receive_message()
            print(message)

    def start_keyboard_input_thread(self) -> None:
        keyboard_input_thread = Thread(target=self.keyboard_input, daemon=True)
        keyboard_input_thread.start()

    def keyboard_input(self) -> None:
        while self.is_connection_up() and self.is_running:
            message = input()
            self.send_message(message)

    def send_message(self, message: str) -> None:
        self.connection.send(message.encode())

    def receive_message(self) -> str:
        return self.connection.recv(1024).decode("utf-8")

    def shutdown(self) -> None:
        self.is_running = False
        self.connection.close()

    def is_connection_up(self) -> bool:
        try:
            data = self.connection.recv(16, MSG_DONTWAIT | MSG_PEEK)
            if len(data) == 0:
                return False
        except BlockingIOError:
            return True
        except ConnectionResetError:
            return False
        except Exception as e:
            print(f"unexpected exception when checking socket is closed: {e}")
            return True
        return True
