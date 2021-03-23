import socket
import sys
from json.encoder import JSONEncoder
from json.decoder import JSONDecoder
from blockchain import BlockChain
from block import Block
from transaction import Transaction
from merkleproof import MerkleProof
from time import time
import threading
import uuid
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
PORT = None
ADDRESS_WALLET = uuid.uuid4().hex
transction_tbd = []

def mineBlock(transactions):
    global bc
    global bc_l
    nonce = 1
    print(bc_l)
    if bc_l == 0 :
        print('len = 0')
        while not bc.validProof(None, transactions, nonce, oneblock=True):
            nonce += 1
        bc.addBlock(bc.createBlock(nonce=nonce, previousHash=None, transactions=transactions))
    else :
        if  bc.valid_chain():
            lastBlock = bc.last()
            lastBlockHash = lastBlock.getHash()
            nonce = 0
            print('Previoushash', lastBlockHash)
            while not bc.validProof(lastBlockHash, transactions, nonce):
                nonce += 1
            # Add reward
            #transactions.append(Transaction(time(), 'SYSTEM', ADDRESS_WALLET, 1))
            bc.addBlock(bc.createBlock(nonce=nonce, previousHash=lastBlockHash, transactions=transactions))
            print('Here2')
    for tmp in transactions:
        print('Transaction {} has been added to the block', format(tmp.hash()))
    bc_l += 1

def send_show_blockchain(s, port):
    message = JSON_ENCODER.encode({
        'type': 'show-blockchain',
        'port': 'coucou'
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))
    s.close()

def send_mining_port(s, port):
    message = JSON_ENCODER.encode({
        'type': 'register_miner',
        'port': port
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))
    s.close()


def send_peers_port(s, list_peers):
    message = JSON_ENCODER.encode({
        'type': 'register_peers',
        'port': list_peers
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))
    s.close()

def send_new_peer(s, port):
    message = JSON_ENCODER.encode({
        'type': 'new_peer',
        'port': port
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))
    s.close()


def send_blockchain(s,blockchain):
    message = JSON_ENCODER.encode({
        'type': 'init_bc',
        'blockchain': blockchain
    })
    print('Sending Blockchain {}'.format(message))
    s.send(str.encode(message))
    s.close()


def broadcast_blockchain(s,blockchain,sender_port):
    message = JSON_ENCODER.encode({
        'type': 'broadcast_blockchain',
        'blockchain': blockchain,
        'sender_port':sender_port
    })
    print('Broadcasting Blockchain')

    s.send(str.encode(message))
    s.close()

def broadcast_transaction(s, transaction):
    message = JSON_ENCODER.encode({
        'type': 'broadcast_transaction',
        'transaction': transaction
    })
    print('Broadcasting Transaction')
    s.send(str.encode(message))
    s.close()

def send_transaction_blockchain(s, port, amount, fromWallet, toWallet):
    message = JSON_ENCODER.encode({
        'type': 'broadcast_transaction',
        'port': port,
        'amount': amount,
        'fromWallet': fromWallet,
        'toWallet': toWallet
    })
    print('Sending message {}'.format(message))
    s.send(str.encode(message))

def read_message(c):
    bytes = c.recv(4096)
    return JSON_DECODER.decode(bytes.decode())


def handle_message(peers, server_port, message,s_sender):

    global bc
    global PORT
    global transction_tbd
    print('Received message :')
    print(message)
    message_type = message['type']

    if message_type == 'register_miner':
        port = message['port']

        print('Registering miner N° {} with port {}'.format(len(peers.keys()), port))
        #if port in peers:
        #ps = peers[port]

        #else:
        #send infotmation about the network to the new miner
        ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ps.connect((HOST, port))

        send_peers_port(ps, list(peers.keys()))
        ps.close()

        ps2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ps2.connect((HOST, port))
        send_blockchain(ps2,bc.describe())
        peers[port] = ps


        #no need for peer_socket !!! we crreate it each time
        for peer_port, peer_socket in peers.items():
            if peer_port != port and peer_port != server_port:

                pss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                pss.connect((HOST, peer_port))
                send_new_peer(pss, port)

    elif message_type == 'register_peers':
        port = message['port']
        for peer_port in port:
            if peer_port != server_port and peer_port not in peers:

                peers[peer_port]=None

                print(f"Peer {peer_port} added")

    elif message_type == 'new_peer':
        port = message['port']
        peers[port] = None


        print(f"Peer {port} added to peers")

    elif message_type == 'show-blockchain':
        print(bc.toString())

    elif message_type == 'make-transaction':

        amount = message['amount']
        fromWallet = message['fromWallet']
        toWallet = message['toWallet']
        timestamp = message['timestamp']
        transaction_tmp = Transaction(timestamp=timestamp, fromWallet=int(fromWallet), toWallet=int(toWallet), transactionAmount=float(amount))
        transaction_in = False
        for i in transction_tbd:
            if i.hash()== transaction_tmp.hash():
                transaction_in = True
        if transaction_in == False:
            print('transaction in')
            transction_tbd.append(transaction_tmp)
            #we check if we have more than 3 transactions to be done:
            print('length transactions:', transction_tbd)
            if(len(transction_tbd) >= 2 ):
                # maybe we need lock
                mine_list = transction_tbd[-2:]
                transction_tbd = transction_tbd[:-2]
                #threading.Thread(target=mineBlock([Transaction(time(), fromWallet, toWallet, amount)]), ).start()
                mine_list_tmp = []
                print('Mine list', mine_list)
                print('Valid or not ? ')
                for transaction_mine in mine_list:
                    print(bc.validTransaction(transaction_mine))
                    if bc.validTransaction(transaction_mine):
                        mine_list_tmp.append(transaction_mine)
                print('Valid transactions')
                print(mine_list_tmp)
                if (len(mine_list_tmp) > 0):

                    mineBlock(mine_list_tmp)
                    for peer_port, peer_socket in peers.items():
                        if peer_port != server_port:
                            ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            ps.connect((HOST, peer_port))
                            print('Broadcasting our blockchain')
                            print(bc.toString())
                            broadcast_blockchain(ps, bc.describe(),server_port)
            ## we add the transaction
    elif message_type == "init_bc":
        received_bc = message["blockchain"]
        bc = BlockChain(chain=received_bc['chain'])
        print(bc.toString())


    elif message_type == 'broadcast_blockchain':
        sender_port = message["sender_port"]
        received_bc = message['blockchain']
        received_bc = BlockChain(chain=[Block(index=block['index'], nonce=block['nonce'], hash=block['hash'], previousHash=block['previousHash'], transactions=[Transaction(timestamp=transaction['timestamp'], fromWallet=transaction['fromWallet'], toWallet=transaction['toWallet'], transactionAmount=transaction['transactionAmount']) for transaction in block['transactions']]) for block in received_bc['chain']])
        if(received_bc.hash() !=bc.hash()):

            print('Valid chain?:', received_bc.valid_chain())
            print('Length received:', len(received_bc.chain))
            print('Length actual:', len(bc.chain))
            print('Received chain:\n', received_bc.toString())
            if received_bc.valid_chain() and len(received_bc.chain) > len(bc.chain):
                print('New blockchain')
                print(received_bc.toString())
                bc = received_bc
                for peer_port, peer_socket in peers.items():
                    if peer_port != server_port and peer_port!= sender_port:
                        print("Broadcast to : ",peer_port)
                        pss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        pss.connect((HOST, peer_port))
                        broadcast_blockchain(pss, bc.describe(),server_port)
        else:
            print("Blockchain already updated")

    elif message_type == 'check-transaction':
        id_transaction = message['id']
        #transaction_tmp = Transaction(timestamp=timestamp, fromWallet=int(fromWallet), toWallet=int(toWallet), transactionAmount=float(amount))
        block = bc.getBlock(id_transaction)
        block.calculateMerkleRoot()
        print(block)
        if block is None:
            proof = MerkleProof(not_found=True)
        else:
            print(block.describe())
            transaction_position = block.transactionIndex(id_transaction)
            proof = MerkleProof(root=block.merkleRoot,  hashList=block.merkleTree().get_proof(transaction_position))

        print('Proof:', proof.describe())
        print(proof.inMerkleTree(transaction_position))


#self.channel_manager.answer_message(channel, response_message)

def main():

    global bc
    global PORT

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
            s.bind((HOST, PORT))

            ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # We do have a parent node, establish connection
            if PARENT_PORT != PORT :
                print('Connecting to parent node with port {}'.format(PARENT_PORT))

                ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ps.connect((HOST, PARENT_PORT))

                send_mining_port(ps, PORT)
                PEERS[PARENT_PORT] = ps



            print('Waiting for incoming connections from child miners')
            c = 1
            s.listen(5)

            while True:
                conn, addr = s.accept()
                #import pdb;pdb.set_trace()
                message = read_message(conn)
                #handle_message(PEERS, PORT, message)
                threading.Thread(target=handle_message(PEERS, PORT, message,conn))
                c = c + 1

        except KeyboardInterrupt:
            print('Interrupt signal received, closing connections and freeing resources')
            s.close()
            if ps is not None:
                ps.close()
            sys.exit()

if __name__ == '__main__':
    main()