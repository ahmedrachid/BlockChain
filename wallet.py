import socket
import sys

HOST = "127.0.0.1"


def main():
    if len(sys.argv)!=2:
        print("Usage: python wallet.py port_miner")

    else:
        try:
            MINER_PORT = int(sys.argv[1])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, MINER_PORT))

            while True:
                print('Write your command please : ')
                command = input()
                if command == 'show':
                    message = 'show'
                    s.send(message.encode())

                if command == 'end':
                    sys.exit()

        except KeyboardInterrupt:
            print('Interrupt signal received, closing connections and freeing resources')
            sys.exit()


if __name__ == '__main__':
    main()


