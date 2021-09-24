from hashlib import sha256
import json
import time
from json import JSONEncoder

"""
from flask import Flask, request
import requests
"""

class Transaction:
    # constructor for the transaction class.
    def __init__(self,fromAddress,toAddress,amount,timestamp):
        self.fromAddress = fromAddress
        self.toAddress = toAddress
        self.amount = amount
        self.timestamp = timestamp
    
    def compute_hash(self):
        """
        A function that returns the hash of the transaction contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class BlockEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class Block:
    """
    constructor for the block class.
    """
    def __init__(self, index, transactions, timestamp, previous_hash,nonce = 0):
        self.index = index
        self.transactions = transactions 
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        
    def compute_hash(self):
        """
        A function that returns the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys = True,indent=4, cls=BlockEncoder)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    # difficulty of our PoW algorithm.
    difficulty = 2

    # constructor for the Blockchain class.
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria, which we set accordingly.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(last_block.index + 1,
                          self.unconfirmed_transactions,
                          time.time(),
                          last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index

if  __name__ == "__main__":
    myBlockchain = Blockchain()
    transaction1 = Transaction("Aman","Vedang",'5 dogecoin',time.time())
    transaction2 = Transaction("Vedang","Vedang",'10 dogecoin',time.time())
    #print(MyBlockchain.__dict__)
    myBlockchain.add_new_transaction(transaction1)
    #print(MyBlockchain.__dict__)
    myBlockchain.add_new_transaction(transaction2)
    #print(MyBlockchain.__dict__)
    jsonStr = json.dumps(myBlockchain.last_block.__dict__, indent=4, cls=BlockEncoder)
    print(jsonStr)
    myBlockchain.mine()
    #print(MyBlockchain.__dict__)
    jsonStr = json.dumps(myBlockchain.last_block.__dict__, indent=4, cls=BlockEncoder)
    print(jsonStr)
    

