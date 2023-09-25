import sys

def main():
    argument = sys.argv[1] if len(sys.argv) == 2 else ''
    if argument == "-c" or argument == "--client":
        execute_client()
    elif argument == "-s" or argument == "--server":
        execute_server()
    else:
        print_usage()


def execute_server():
    pass

def execute_client():
    pass

def print_usage():
    print(
        """SimpleChat [Option]
                --server, -s
                --client, -c [IP-Adress]"""
    )


if __name__ == "__main__":
    main()
