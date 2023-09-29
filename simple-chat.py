import sys
from server import Server
from client import Client

DEFAULT_HOST = "127.0.0.1"
PORT = 8080


def main():
    argument = sys.argv[1] if len(sys.argv) >= 2 else ''

    if argument == "-c" or argument == "--client":
        execute_client(parse_host(sys.argv))
    elif argument == "-s" or argument == "--server":
        execute_server()
    else:
        print_usage()


def parse_host(arguments: list[str]) -> str:
    if len(arguments) == 3:
        return arguments[2]
    else:
        return DEFAULT_HOST


def execute_server():
    server = Server(PORT)
    try:
        server.listen()
        server.shutdown()
    except KeyboardInterrupt:
        server.shutdown()
    except Exception as error:
        server.shutdown()
        print(f"Error occured: {error}")


def execute_client(host: str):
    client = Client(host, PORT)
    try:
        client.connect()
        client.shutdown()
    except KeyboardInterrupt:
        client.shutdown()
    except Exception as error:
        client.shutdown()
        print(f"Error occured: {error}")


def print_usage():
    print(
        """simple-chat [Option]
                --server, -s
                --client, -c [IP-Adress]"""
    )


if __name__ == "__main__":
    main()
