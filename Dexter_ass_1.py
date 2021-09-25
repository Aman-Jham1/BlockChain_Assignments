import json
import time
from hashlib import sha256
from json import JSONEncoder

class Transaction:
    
    def __init__(self,fromAddress,toAddress,amount,timestamp):
        """
        Constructor for the `Transaction` class.
        :param fromAddress: who is sending.
        :param toAddress: who is recieving.
        :param amount: amount sent.
        :param timestamp: Time of generation of the transaction.
        """
        self.transaction = {
            "fromAddress": fromAddress,
            "toAddress": toAddress,
            "amount": amount,
            "timestamp": timestamp
        }
    
    def compute_hash(self):
        """
        Creates a SHA-256 hash of a transaction
        :param block: Transaction.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Block:
    
    def __init__(self, index, transactions, timestamp, previous_hash,nonce = 0):
        """
        Constructor for the `Block` class.
        :param index: Unique ID of the block.
        :param transactions: List of transactions.
        :param timestamp: Time of generation of the block.
        :param previos_hash: hash of the previos block.
        :nonce: Nonce of the block.
        """
        self.index = index
        self.transactions = transactions 
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        
    def compute_hash(self):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True, indent=4, cls=BlockEncoder)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    # difficulty of our PoW algorithm.
    # should be choosed accordingly.
    difficulty = 2

    def __init__(self):
        """
        Constructor for the `Blockchain` class.
        """
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
        """
        A quick pythonic way to retrieve the most recent block in the chain. Note that
        the chain will always consist of at least one block (i.e., genesis block)
        """
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
        that satisfies our difficulty criteria, which we set according to the need.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        """
        This function adds new transaction to unconfirmed transactions pool
        which will be verified than added to block when mined.
        """
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
        
        # creating new block which will all unconfirmed transactions.
        # will be added after the last block in the blockchain.
        
        new_block = Block(last_block.index + 1,
                          self.unconfirmed_transactions,
                          time.time(),
                          last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        # clearing all the pending transactions as added to the block.
        self.unconfirmed_transactions = []
        return new_block.index

class BlockEncoder(JSONEncoder):
    """
    This class overrides the default() method of a JSONEncoder class,
    so we able to convert custom Python Block object into JSON.
    """
    def default(self, o):
        return o.__dict__

class BlockChainEncoder(JSONEncoder):
    """
    This class overrides the default() method of a JSONEncoder class,
    so we able to convert custom Python Blockchain object into JSON.
    """
    def default(self, o):
        return o.__dict__

if  __name__ == "__main__":
    # myBlockchain = Blockchain()
    # transaction1 = Transaction("Aman","Vedang",'5 dogecoin',time.time())
    # transaction2 = Transaction("Vedang","AMan",'10 dogecoin',time.time())
    # transaction3 = Transaction("Shubh","Aman","5 BTC",time.time())
    # myBlockchain.add_new_transaction(transaction1)
    
    # myBlockchain.add_new_transaction(transaction2)
    
    # #print(jsonStr)
    # #jsonStr = json.dumps(myBlockchain.last_block.__dict__, indent=4, cls=BlockEncoder)
    # #print(jsonStr)
    # myBlockchain.mine()
    # myBlockchain.add_new_transaction(transaction3)
    # #myBlockchain.mine()
    # #myBlockchain.mine()
    # #hash1 = myBlockchain.last_block.hash
    # jsonStr = json.dumps(myBlockchain.__dict__, indent=4 , cls=BlockChainEncoder)
    # print(jsonStr)
    # delattr(myBlockchain.last_block,"hash")
    # hash1 = myBlockchain.last_block.compute_hash();
    # myBlockchain.last_block.transactions[0].amount = "10 dogecoin"
    # hash2 = myBlockchain.last_block.compute_hash();
    # jsonStr = json.dumps(myBlockchain.__dict__, indent=4 , cls=BlockChainEncoder)
    # #jsonStr = json.dumps(myBlockchain.last_block.__dict__, indent=4, cls=BlockEncoder)
    # #print(jsonStr)
    # #print(hash1)
    # #print(hash2)
    
    myBlockchain = Blockchain()
    
    operations = """Enter according want you want to do with blockchain,
    Enter 1 if you want to print the current BlockChain
    Enter 2 if you want to add a new transaction
    Enter 3 if you want to mine a new block."""
    
    operation_dict = {
        "1": "Print blockchain",
        "2": "Add transaction",
        "3": "Mine Block"
    }
    
    add_transaction = "Enter fromAddress, toAddress, and Amount, each in a new line"
    
    while True:
        print()
        print(operations)
        print()
        cur_oper = int(input())
        print()
        if cur_oper == 1:
            #print(myBlockchain.chain)
            jsonStr = json.dumps(myBlockchain.__dict__, indent=4 , cls=BlockChainEncoder)
            print(jsonStr)
        elif cur_oper == 2:
            print(add_transaction)
            print()
            fromAddress = input()
            toAddress = input()
            amount = input()
            myBlockchain.add_new_transaction((fromAddress,toAddress,amount,time.time()))
        else:
            if not myBlockchain.mine():
                print("No pending transactions.")
            else:
                print("Mining a new block is successful.") 
                print("Mined Block is : ")
                print(json.dumps(myBlockchain.last_block.__dict__, indent=4, cls=BlockEncoder))       
            
                
        
        
        
        
   
    

