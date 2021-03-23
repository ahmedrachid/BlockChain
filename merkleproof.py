from hashlib import sha256
from merkletools import MerkleTools

class MerkleProof:
    def __init__(self, root: str = None, hashList: list = None, notInTree=False):
        self.root = root
        self.hashList = hashList
        self.notInTree = notInTree

    def inMerkleTree(self, transaction):

        if self.notInTree:
            return False

        return MerkleTools().validate_proof(self.hashList, sha256(str(transaction).encode('utf-8')).hexdigest(), self.root)

    def describe(self):
        return self.__dict__
