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
    
    def mine_block(self, difficulty):
        # Define what a correct hash looks like based on the difficulty level
        target_string = "0" * difficulty
        
        # Keep trying different nonce values until we find a hash that meets the difficulty requirement
        while self.hash[:difficulty] != target_string:
            # Increment the nonce to change the hash
            self.nonce += 1
            
            # Recalculate the hash with the new nonce value
            self.hash = self.calculate_hash()
            
        # Print a message indicating that the block has been successfully mined
        print(f"Blocked mined successfully: {self.hash}")
        
        