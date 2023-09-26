from time import sleep
from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from concurrent.futures import ThreadPoolExecutor


class Server:
    def __init__(self, host, port):
        self.is_running = True
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        executor = ThreadPoolExecutor()
        while self.is_running:
            conn, addr = self.socket.accept()
            executor.submit(self.client_connection, conn, addr)
        executor.shutdown()

    def client_connection(self, connection: socket, address: str):
        print(f"Connected by {address}")
        message = self.receive_message(connection)
        if message == "ping":
            i = 0
            while True:
                self.send_message(connection, "pong" + str(i))
                sleep(2)
                i += 1

    def receive_message(self, socket: socket):
        return socket.recv(1024).decode("utf-8")

    def send_message(self, socket: socket, msg: str):
        socket.send(msg.encode())
