import socket
import sys
import re

HOST = "127.0.0.1"
PORT = 8000
PEERS = set()
RECEIVED_MESSAGES = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, int(sys.argv[1])))
if len(sys.argv) == 3:
    MY_USER = sys.argv[2].encode()
if len(sys.argv) > 3:
    s.connect((HOST, int(sys.argv[2])))
    s.send(sys.argv[3].encode())

s.listen()
conn, addr = s.accept()
with conn:
    while True:
        message = conn.recv(1024)
        message = message.decode()
        print(message)
        regexp = re.compile('[0-9]*')

        if regexp.search(message) :
            PEERS.add(message)
            print(PEERS)

        elif message=="show":
            print(PEERS)

        elif message == "":
            continue
        else:
            RECEIVED_MESSAGES.append(message)

            #s.close()



            regexp = re.compile('[0-9]*')
    if regexp.search(message) :
        PEERS.add(message)
        print(PEERS)
    elif message=="show":
        print(PEERS)
    elif message == "":
        continue
    else:
        RECEIVED_MESSAGES.append(message)