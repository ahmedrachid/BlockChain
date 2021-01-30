import socket
import sys
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder


# Passer les params de creation de process : Port, Parent Node (Port nullable)

# If Parent Node != null

# Create websocket connection with parent

# Start to listen and send events with parent / children


JSON_ENCODER = JSONEncoder()
JSON_DECODER = JSONDecoder()

HOST = "127.0.0.1"
PEERS = []

def send_mining_port(s, port):
    message = JSON_ENCODER.encode({
        'type': 'register_miner',
        'port': port
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))

def send_peers_port(s, port):
    message = JSON_ENCODER.encode({
        'type': 'register_peers',
        'port': port
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))


def read_message(c):
    bytes = c.recv(1024)
    return JSON_DECODER.decode(bytes.decode())


def handle_message(conn, message):
    print('Received message :')
    print(message)
    message_type = message['type']

    if message_type == 'register_miner':
        port = message['port']
        print('Registering miner N° {} with port {}'.format(len(PEERS), port))
        send_peers(conn, PEERS, port)
        PEERS.append(port)

    elif message_type == 'register_peers':
        port = message['port']
        print('Registering node N° {} with port {}'.format(len(PEERS), port))
        PEERS.append(port)

    else:
        print('Unrecognized message type {}'.format(message_type))


def send_peers(conn, peers, port):
    print('Sending peers {} to node with port {}'.format(peers, port))
    for peer in peers:
#        if peer != port:
        send_peers_port(conn, peer)


if __name__ == '__main__':
    PORT = int(sys.argv[1])
    PEERS.append(PORT)
    print('Launching miner node with port {}'.format(PORT))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ps = None

    s.bind((HOST, PORT))
    s.listen()

    # We do have a parent node, establish connection
    if len(sys.argv) > 2:
        PARENT_PORT = int(sys.argv[2])

        print('Connecting to parent node with port {}'.format(PARENT_PORT))

        ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ps.connect((HOST, PARENT_PORT))

        send_mining_port(ps, PORT)

    try:
        print('Waiting for incoming connections from child miners')
        while True:
            conn, addr = s.accept()
            message = read_message(conn)
            handle_message(conn, message)

    except KeyboardInterrupt:
        print('Interrupt signal received, closing connections and freeing resources')
        s.close()
        if ps is not None:
            ps.close()
        sys.exit(0)
