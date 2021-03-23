import hashlib
from transaction import Transaction
from time import time

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

    def addTransaction(self, timestamp, fromWallet, toWallet, transactionAmount):
        self.transactions.append(Transaction(timestamp, fromWallet, toWallet, transactionAmount))

    # Check block's validity
    def isValid(self, oldBlock,difficulty):
        return  oldBlock.hash == self.prevHash \
                and  self.hash()[:difficulty] == "0" * difficulty

    def toString(self):
        return {
            'index': self.index,
            'transaction': [i.toString() for i in self.transactions],
            'previousHash': self.previousHash,
            'currentHash': self.hash
        }
    def describe(self):
        return {
            'transactions': [transactions.describe() for transactions in self.transactions],
            'index': self.index,
            'nonce': self.nonce,
            'previousHash': self.previousHash,
            'hash': self.hash
        }
