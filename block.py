import hashlib
import json
import time


class Block:
    def __init__(self, index, transactions, previous_hash=''):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0 
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        # Package all the block's information into a single dictionary
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        
        # Convert the dictionary into a standard JSON string
        block_string = json.dumps(block_data, sort_keys=True)
        
        # Convert the text into raw bytes, then hash it
        encoded_string = block_string.encode('utf-8')
        hash_object = hashlib.sha256(encoded_string)
        
        # Return the final hash as a readable string of characters
        return hash_object.hexdigest()