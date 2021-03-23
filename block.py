import hashlib
from transaction import Transaction
from time import time
from merkletools import MerkleTools
class Block:

    def __init__(self, index, nonce, previousHash,transactions=[],  hash=None):

        self.index = index
        self.nonce = nonce
        self.timestamp = time()
        self.transactions = transactions
        self.previousHash = previousHash
        if hash is None:
            self.hash = self.getHash()
        else:
            self.hash = hash
    def getHash(self):
        blockProperties = str(self.index) \
                          + str([i.toString() for i in self.transactions]) \
                          + str(self.timestamp) \
                          + str(self.nonce) \
                          + str(self.previousHash)
        return hashlib.sha256(blockProperties.encode('utf-8')).hexdigest()

    def getCurrentHash(self):
        return self.hash

    def addTransaction(self, timestamp, fromWallet, toWallet, transactionAmount):
        self.transactions.append(Transaction(timestamp, fromWallet, toWallet, transactionAmount))

    # Check block's validity
    def isValid(self, oldBlock,difficulty):
        return  oldBlock.hash == self.prevHash \
                and  self.hash()[:difficulty] == "0" * difficulty

    def transactionsList(self, fromWallet=None, toWallet=None):
        if fromWallet is not None:
            return [transaction for transaction in self.transactions if transaction.fromWallet == fromWallet]
        elif toWallet is not None:
            return [transaction for transaction in self.transactions if transaction.toWallet == toWallet]
        else:
            return self.transactions

    def toString(self):
        return '\n\t\t index: \t\t'+ str(self.index)+ '\n'+ '\t\ttransaction: \t\t'+ str([i.toString() for i in self.transactions])+ '\n'+'\t\tpreviousHash: \t\t'+ str(self.previousHash)+ '\n'+'\t\tcurrentHash: \t\t'+ str(self.hash)

    def describe(self):
        return {
            'transactions': [transactions.describe() for transactions in self.transactions],
            'index': self.index,
            'nonce': self.nonce,
            'previousHash': self.previousHash,
            'hash': self.hash
        }

    def merkleTree(self):
        tree = MerkleTools(hash_type="SHA256")
        tree.add_leaf([transaction.hash() for transaction in self.transactions], True)
        tree.make_tree()
        return tree

    def calculateMerkleRoot(self):
        self.merkleRoot = self.merkleTree().get_merkle_root()

    def transactionIndex(self, transaction):

        for index, tmp in enumerate(self.transactions):
            if transaction == tmp.hash():
                return index