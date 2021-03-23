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

def main():
    if len(sys.argv)!=2:
        print("Usage: python wallet.py port_miner")
    else:
        try:
           

            while True:
                MINER_PORT = int(sys.argv[1])

                print('Write your command please : ')
                command = input()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, MINER_PORT))
                if command == 'show':
                    send_show_blockchain(s, MINER_PORT)
                    s.close()
                if command == 'transaction':    
                    print('Write your amount please : ')
                    amount = input()
                    print('Write your WalletID please : ')
                    fromWallet = input()
                    print('Write the ClientID please : ')
                    toWallet = input()
                    send_transaction_blockchain(s, MINER_PORT, amount, fromWallet, toWallet, time())
                if command == 'end':
                    sys.exit()  
                

        except KeyboardInterrupt:
            print('Interrupt signal received, closing connections and freeing resources')
            sys.exit()


if __name__ == '__main__':
    main()


