from block import Block
from transaction import Transaction
from hashlib import sha256
from time import time
class BlockChain:
    def __init__(self):
        self.chain = []
        self.NUMBER_TRANSACTIONS = 10
        self.HASHING_DIFFICULTY = 2
        #self.addBlock(Block(1,0, '00', []))

    # Get length of blockchain
    def len(self):
        return len(self.chain)

    # Add block to last of the chain
    def addBlock(self, block):
        self.chain.append(block)
        return block

    # Create New Block using Nonce and PreviousHash
    def createBlock(self, nonce, previousHash, transactions):
        return Block(self.len()+1, nonce, previousHash, transactions)

    def replaceIfNeeded(self, otherBlockchain):
        if otherBlockchain.len() > self.len():
            self.chain = otherBlockchain.chain

    # Get first block or None
    def first(self):
        return self.chain[0] if self.len() > 0 else None

    # Get last block or None
    def last(self):
        return self.chain[self.len() - 1] if self.len() > 0 else None

    # Valid proof
    def validProof(self, previousHash, transactions, nonce ,oneblock=False):
        if oneblock == True:
            hashing = str(transactions) \
                      + str(nonce)
        else :
            hashing = str(previousHash) \
                      + str(transactions) \
                      + str(nonce)
        hashing = sha256(hashing.encode('utf-8')).hexdigest()
        return hashing[:self.HASHING_DIFFICULTY] == '0' * self.HASHING_DIFFICULTY

    # Check if the chain is valid or not
    def valid_chain(self):
        last_block = self.first()
        if not validProof(self, previousHash, transactions, nonce ,oneblock=True):
            return False

        current_index = 1
        while current_index < self.len():
            block = self.chain[current_index]
            if block.previousHash != last_block.getHash():
                return False

            transactions = block.transactions
            nonce = block.nonce
            previousHash = block.previousHash
            if not self.validProof(previousHash, transactions, nonce):
                return False
            print(last_block.toString())
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

    # Get Reward : make a special transaction as a reward when we find a new block
    # def getReward(self, fromWallet, toWallet, transactionAmount):
    #    self.last().addTransaction(time(), fromWallet, toWallet, transactionAmount)

    # Mine the block

    def toString(self):
        blocks = []
        for block in self.chain:
            blocks.append(block.toString())
        return blocks

    def describe(self):
        return self.__dict__
