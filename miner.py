import socket
import sys
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder
from blockchain import BlockChain
from block import Block
from transaction import Transaction
from transaction import Transaction
from time import time
import threading
import pickle
# Passer les params de creation de process : Port, Parent Node (Port nullable)

# If Parent Node != null

# Create websocket connection with parent

# Start to listen and send events with parent / children


JSON_ENCODER = JSONEncoder()
JSON_DECODER = JSONDecoder()

HOST = "127.0.0.1"
lock = threading.Lock()
bc = BlockChain()
bc_l = 0


def mineBlock( transactions):
    global bc
    global bc_l
    nonce = 1
    if bc_l == 0 :
        while not bc.validProof(None, transactions, nonce, oneblock=True):
            nonce += 1
        bc.addBlock(bc.createBlock(nonce, None, transactions))

        print('Nonce:', nonce)
    else :
        if  bc.valid_chain():
            lastBlock = bc.last()
            lastBlockHash = lastBlock.getHash()
            nonce = 0
            while not bc.validProof(lastBlockHash, transactions, nonce):
                nonce += 1
            # Add reward
            print('Nonce:', nonce)
            bc.addBlock(bc.createBlock(nonce, lastBlockHash, transactions))
    bc_l += 1
    print(bc.describe())
    print('Block', bc.chain[0].toString())



def send_mining_port(s, port):
    message = JSON_ENCODER.encode({
        'type': 'register_miner',
        'port': port
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))

def send_peers_port(s, list_peers):
    message = JSON_ENCODER.encode({
        'type': 'register_peers',
        'port': list_peers
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))

def send_new_peer(s, port):
    message = JSON_ENCODER.encode({
        'type': 'new_peer',
        'port': port
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))


def send_blockchain(s,blockchain):
    message = JSON_ENCODER.encode({
        'type': 'init_bc',
        'blockchain': blockchain
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))


def broadcast_blockchain(s,blockchain):
    message = JSON_ENCODER.encode({
        'type': 'broadcast_blockchain',
        'blockchain': blockchain
    })
    print('Broadcasting blockchain {} with {}'.format(s, message))
    s.send(str.encode(message))



def read_message(c):
    bytes = c.recv(1024)
    return JSON_DECODER.decode(bytes.decode())




def handle_message(peers, server_port, message):

    global bc
    print('Received message :')
    print(message)
    message_type = message['type']

    if message_type == 'register_miner':
        port = message['port']

        print('Registering miner N° {} with port {}'.format(len(peers.keys()), port))
        if port in peers:
            ps = peers[port]

        else:
            ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ps.connect((HOST, port))

            send_peers_port(ps, list(peers.keys()))
            ps2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ps2.connect((HOST, port))
            send_blockchain(ps2,bc.describe())
            peers[port] = ps

        for peer_port, peer_socket in peers.items():
            if peer_port != port and peer_port != server_port:
                send_new_peer(peer_socket, port)

    elif message_type == 'register_peers':
        port = message['port']
        for peer_port in port:
            if peer_port != server_port and peer_port not in peers:
                ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ps.connect((HOST,peer_port))

                peers[peer_port]=ps

                print(f"Peer {peer_port} added")

    elif message_type == 'new_peer':
        port = message['port']
        ps=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ps.connect((HOST, port))
        peers[port]=ps

        print(f"Peer {port} added to peers")

    elif message_type == 'make-transaction':
        amount = message['amount']
        fromWallet = message['fromWallet']
        toWallet = message['toWallet']
        print(message_type)
        #threading.Thread(target=mineBlock([Transaction(time(), fromWallet, toWallet, amount)]), ).start()
        mineBlock([Transaction(time(), fromWallet, toWallet, amount)])
        for peer_port, peer_socket in peers.items():
            if peer_port != server_port:
                ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ps.connect((HOST, peer_port))
                broadcast_blockchain(ps, bc.describe())

        ## we add the transaction
    elif message_type == "init_bc":
        received_bc = message["blockchain"]
        print(received_bc)
        bc = BlockChain(chain=received_bc['chain'])
        print(bc.describe())

    elif message_type == 'broadcast_blockchain':
        received_bc = message['blockchain']
        received_bc = BlockChain(chain=[Block(index=block['index'], nonce=block['nonce'], hash=block['hash'], previousHash=block['previousHash'], transactions=[Transaction(timestamp=transaction['timestamp'], fromWallet=transaction['fromWallet'], toWallet=transaction['toWallet'], transactionAmount=transaction['transactionAmount']) for transaction in block['transactions']]) for block in received_bc['chain']])
        print(received_bc.describe())
        print('Valid or no?: ', received_bc.valid_chain())
        print('Length received:', len(received_bc.chain))
        print('Length actual:', len(bc.chain))
        if received_bc.valid_chain() and len(received_bc.chain) > len(bc.chain):
            print('New blockchain')
            bc = received_bc


def main():

    global bc

    if len(sys.argv)!=3:
        print("Usage: python miner.py port miner_port")

    else:
        try:
            bc = BlockChain()
            print("blockcain",bc)

            PORT = int(sys.argv[1])
            PARENT_PORT = int(sys.argv[2])
            PEERS = {PORT:None}


            print('Launching miner node with port {}'.format(PORT))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.bind((HOST, PORT))

            # We do have a parent node, establish connection
            if PARENT_PORT != PORT :
                print('Connecting to parent node with port {}'.format(PARENT_PORT))

                ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ps.connect((HOST, PARENT_PORT))

                send_mining_port(ps, PORT)
                PEERS[PARENT_PORT] = ps



            print('Waiting for incoming connections from child miners')
            while True:
                print('List of peers:', PEERS)
                s.listen(5)
                conn, addr = s.accept()
                message = read_message(conn)
                handle_message(PEERS, PORT, message)

        except KeyboardInterrupt:
            print('Interrupt signal received, closing connections and freeing resources')
            s.close()
            if ps is not None:
                ps.close()
            sys.exit()

if __name__ == '__main__':
    main()