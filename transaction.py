class Transaction:

    def __init__(self, timestamp, fromWallet, toWallet, transactionAmount):
        self.timestamp = timestamp
        self.fromWallet = fromWallet
        self.toWallet = toWallet
        self.transactionAmount = transactionAmount

    def toString(self):
        return {
            'timestamp': self.timestamp,
            'fromWallet': self.fromWallet,
            'toWallet': self.toWallet,
            'transactionAmount': self.transactionAmount,
        }

    def describe(self):
        return self.__dict__
