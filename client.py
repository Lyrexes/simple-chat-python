from socket import socket


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket()

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.send_message("ping")
        while True:
            message = self.receive_message()
            print(message + "\n")

    def send_message(self, message: str):
        self.socket.send(message.encode())

    def receive_message(self):
        return self.socket.recv(1024).decode()
