from hashlib import sha256

class Transaction:

    def __init__(self, timestamp, fromWallet, toWallet, transactionAmount):
        self.timestamp = timestamp
        self.fromWallet = fromWallet
        self.toWallet = toWallet
        self.transactionAmount = transactionAmount

    def toString(self):
        return str({
            'timestamp': self.timestamp,
            'fromWallet': self.fromWallet,
            'toWallet': self.toWallet,
            'transactionAmount': self.transactionAmount,
        })

    def describe(self):
        return self.__dict__

    def hash(self):
        return sha256(str(self.describe()).encode('utf-8')).hexdigest()

