from block import Block
from transaction import Transaction
from hashlib import sha256
from time import time
class BlockChain:
    def __init__(self, chain=[]):
        if chain is None:

            self.chain = []
        else:
            self.chain = chain
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
            hashing = str([t.describe() for t in transactions]) \
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
        if not self.validProof(last_block.previousHash, last_block.transactions, last_block.nonce ,oneblock=True):

            return False

        current_index = 1
        while current_index < self.len():
            block = self.chain[current_index]
            #import pdb;pdb.set_trace()

            if block.previousHash != last_block.getCurrentHash():
                return False

            transactions = block.transactions
            nonce = block.nonce
            previousHash = block.previousHash
            # verify if the current hash was calculated with actual nonce,transactions
            #
            hashing = str(previousHash) \
                      + str(transactions) \
                      + str(nonce)
            hashing = sha256(hashing.encode('utf-8')).hexdigest()
            if not (hashing[:self.HASHING_DIFFICULTY] == '0' * self.HASHING_DIFFICULTY or hashing != block.getCurrentHash()):
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

    # Get Reward : make a special transaction as a reward when we find a new block
    # def getReward(self, fromWallet, toWallet, transactionAmount):
    #    self.last().addTransaction(time(), fromWallet, toWallet, transactionAmount)

    # Mine the block

    def validTransaction(self, transaction: Transaction):
        if transaction.transactionAmount <= 0:
            return False
        if transaction.fromWallet == 1 and transaction.transactionAmount > 0:
            return True
        credit = 0
        for block in self.chain:
            for receivedTransaction in block.transactionsList(fromWallet=transaction.fromWallet):
                credit -= receivedTransaction.transactionAmount
            for sendingTransaction in block.transactionsList(toWallet=transaction.fromWallet):
                credit += sendingTransaction.transactionAmount
        return credit > transaction.transactionAmount

    def toString(self):
        s = 'Blockchain: \n'
        for block in self.chain:
            s+='\t Block: '+str(block.toString())+'\n'
        return s

    def describe(self):
        try:
            return {
                'chain': [chain.describe() for chain in self.chain]
            }
        except:
            return {
                'chain': []
            }
    def hash(self):
        return sha256(str(self.describe()).encode('utf-8')).hexdigest()

    def getBlock(self, transaction):
        for block in self.chain:
            for tmp in block.transactionsList():
                if tmp.hash() == transaction:
                    return block
        return None