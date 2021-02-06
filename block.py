import hashlib
from transaction import Transaction
import time

class Block:

    def __init__(self, index, transaction, previousHash):

        self.index = index
        self.transaction = transaction
        self.previousHash = previousHash
        self.hash = self.getHash()

    def getHash(self):
        blockProperties = str(self.index) \
                          + str(self.timestamp) \
                          + self.transaction.toString() \
                          + str(self.prevHash)

        return hashlib.sha256(blockProperties.encode('utf-8')).hexdigest()

    def generateNewBlock(self, fromWallet, toWallet, transactionAmount):
        return Block(self.index + 1,
                     Transaction(str(time.calendar.timegm(time.gmtime())), fromWallet, toWallet, transactionAmount),
                     self.hash)

    def toString(self):
        return {
            'index': self.index,
            'transaction': self.transaction.toString(),
            'previousHash': self.previousHash,
            'currentHash': self.hash
        }