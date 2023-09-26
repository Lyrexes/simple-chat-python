import sys
from server import Server
from client import Client

HOST = "127.0.0.1"
PORT = 8080


def main():
    argument = sys.argv[1] if len(sys.argv) == 2 else ''
    if argument == "-c" or argument == "--client":
        execute_client()
    elif argument == "-s" or argument == "--server":
        execute_server()
    else:
        print_usage()


def execute_server():
    server = Server(HOST, PORT)
    server.listen()


def execute_client():
    client = Client(HOST, PORT)
    client.connect()


def print_usage():
    print(
        """SimpleChat [Option]
                --server, -s
                --client, -c [IP-Adress]"""
    )


if __name__ == "__main__":
    main()
