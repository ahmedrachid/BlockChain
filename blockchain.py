from block import Block
from transaction import Transaction

class BlockChain:

    def __init__(self):
        self.chain = []
        self.NUMBER_TRANSACTIONS = 10

    # Get length of blockchain
    def len(self):
        return len(self.chain)

    # Add block to last of the chain
    def addBlock(self, block):
        self.chain.append(block)
        return block

    def replaceIfNeeded(self, otherBlockchain):
        if otherBlockchain.len() > self.len():
            self.chain = otherBlockchain.chain

    # Get first block or None
    def first(self):
        return self.chain[0] if self.len() > 0 else None

    # Get last block or None
    def last(self):
        return self.chain[self.len() - 1] if self.len() > 0 else None

    # Check if the chain is valid or not
    def valid_chain(self, chain):
        last_block = self.first()
        current_index = 1
        while current_index < self.len():
            block = chain[current_index]
            if block.previousHash != last_block.getHash():
                return False
            last_block = block
            current_index += 1

        return True

    # Add Transaction to the Last Block
    def addTransaction(self, timestamp, fromWallet, toWallet, transactionAmount):

        lastBlock = self.last()
        if len(lastBlock.transactions) == self.NUMBER_TRANSACTIONS:
            self.mineBlcok(lastBlock)
            self.addTransaction(timestamp, fromWallet, toWallet, transactionAmount)
        else:
            lastBlock.transactions.append(Transaction(timestamp, fromWallet, toWallet, transactionAmount))
            if len(lastBlock.transactions) == self.NUMBER_TRANSACTIONS:
                self.mineBlcok(lastBlock)

    # Mine the block
    def mineBlcok(self, block):
        if self.valid_chain(block):
            previousHash = self.last().getHash()
            nonce = 0
            s = f"{previousHash}{block.transactions}{nonce}"
            m = sha256()
            m.update(s)
            res = m.digest()[2:-1]
            while not res.startswith("0000"):
                nonce += 1
                s = f"{previousHash}{block.transactions}{nonce}"
                m = sha256()
                m.update(s)
                res = m.digest()[2:-1]
            print("Nonce : " + nonce)
            block.index = self.len()
            block.previousHash = previousHash
            self.blocks.append(block)

    def toString(self):
        blocks = []
        for block in self.chain:
            blocks.append(block.toString())
        return blocks