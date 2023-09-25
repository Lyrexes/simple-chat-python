import socket
import concurrent.futures as e

class Server:
    def __init__(self, host, port):
        self.is_running = True
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        executor = e.ThreadPoolExecutor()
        while self.is_running:
            conn, addr = self.socket.accept()
            future = executor.submit(self.client_connection, conn, addr)
            print(future.result())

    def client_connection(self, connection_socket, address):
        print(f"Connected by {address}")


"""with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)"""


