from socket import socket
from socket import AF_INET
from socket import SOCK_STREAM
from socket import MSG_DONTWAIT
from socket import MSG_PEEK
from concurrent.futures import ThreadPoolExecutor


class Server:
    def __init__(self, port):
        self.is_running = True
        self.port = port
        self.connections = []
        self.socket = socket(AF_INET, SOCK_STREAM)

    def listen(self) -> None:
        self.socket.bind(("0.0.0.0", self.port))
        self.socket.listen()

        executor = ThreadPoolExecutor()
        while self.is_running:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            executor.submit(self.client_connection, connection, address)
        executor.shutdown()

    def receive_message(self, socket: socket) -> str:
        return socket.recv(1024).decode("utf-8")

    def send_message(self, socket: socket, msg: str) -> None:
        socket.send(msg.encode())

    def broadcast(self, message: str) -> None:
        for connection in self.connections:
            self.send_message(connection, message)

    def client_connection(self, connection: socket, address: str) -> None:
        username = self.get_username_from_client(connection)
        print(f"{username} connected by {address}")
        self.handle_client_messages(connection, username)
        self.shutdown_connection(connection)
        self.broadcast(f"{username} left the chat!")
        print(f"{username} disconnected with address: {address}")

    def get_username_from_client(self, connection: socket) -> str:
        self.send_message(connection, "Please enter a username:")
        username = self.receive_message(connection)
        print(username + " connected!")
        self.broadcast(username + " joined the chat!")
        return username

    def handle_client_messages(self, connection: socket, name: str) -> None:
        while self.is_connection_up(connection) and self.is_running:
            client_message = self.receive_message(connection)
            if client_message.startswith("/username "):
                name = self.change_name(
                    client_message,
                    name,
                    connection
                )
            elif client_message == "/quit":
                break
            else:
                self.broadcast(name + ": " + client_message)

    def change_name(self, message: str, username: str, client: socket) -> str:
        command_words = message.split(sep=" ", maxsplit=2)
        if len(command_words) == 2:
            new_username = command_words[1]
            self.send_message(
                client,
                "Succesfully changed username to " + new_username + "!"
            )
            self.broadcast(
                "user \"" + new_username + "\" changed username to \""
                + new_username + "\"!"
            )
            return new_username
        else:
            self.send_message(
                client,
                "Couldnt change username, invalid argumnets!"
            )
            return username

    def shutdown_connection(self, connection: socket) -> None:
        self.connections.remove(connection)
        connection.close()

    def shutdown(self) -> None:
        self.is_running = False
        for connection in self.connections:
            self.shutdown_connection(connection)

    def is_connection_up(self, connection: socket) -> bool:
        try:
            data = connection.recv(16, MSG_DONTWAIT | MSG_PEEK)
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
