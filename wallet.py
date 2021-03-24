import socket
import sys
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder
from time import time

HOST = "127.0.0.1"
JSON_ENCODER = JSONEncoder()
JSON_DECODER = JSONDecoder()

def send_show_blockchain(s, port):
    message = JSON_ENCODER.encode({
        'type': 'show-blockchain',
        'port': port
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))
    s.close()

def send_transaction_blockchain(s, port, amount, fromWallet, toWallet, timestamp):
    message = JSON_ENCODER.encode({
        'type': 'make-transaction',
        'port': port,
        'amount': amount,
        'fromWallet': fromWallet,
        'toWallet': toWallet,
        'timestamp': timestamp
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))

def  check_transaction_blockchain(s, port, id):
    message = JSON_ENCODER.encode({
        'type': 'check-transaction',
        'id': id
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))

def main():
    if len(sys.argv)!=3:
        print("Usage: python wallet.py port_miner")
    else:
        try:
            while True:
                MINER_PORT = int(sys.argv[1])
                WALLET_ID = int(sys.argv[2])
                cmd = int(input(
                    """
    1. show blockchain
    2. send transaction
    3. check transaction
    4. end
    Choice :
    """
                ))
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, MINER_PORT))
                if cmd == 1:
                    send_show_blockchain(s, MINER_PORT)
                    s.close()
                if cmd == 2:
                    print('Write your amount please : ')
                    amount = input()
                    print('Write the ClientID please : ')
                    toWallet = input()
                    send_transaction_blockchain(s, MINER_PORT, float(amount), int(WALLET_ID), int(toWallet), time())
                if cmd == 3:
                    print('Write the ID please: ')
                    id = input()
                    check_transaction_blockchain(s, MINER_PORT, str(id))
                if cmd == 4:
                    sys.exit()
                else:
                    print('Good bye')

        except KeyboardInterrupt:
            print('Interrupt signal received, closing connections and freeing resources')
            sys.exit()


if __name__ == '__main__':
    main()


