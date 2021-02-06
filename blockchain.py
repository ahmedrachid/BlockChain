from block import Block

class BlockChain:

    def __init__(self):
        self.chain = []

    # Get length of blockchain
    def len(self):
        return len(self.chain)
    # Add block to last of the chain
    def addBlock(self, block):
        self.chain.append(block)
        return block

    # Get first block or None
    def first(self):
        return self.chain[0] if self.len() > 0 else None

    # Get last block or None
    def last(self):
        return self.chain[self.len() - 1] if self.len() > 0 else None

    def toString(self):
        blocks = []
        for block in self.chain:
            blocks.append(block.toString())
        return blocks