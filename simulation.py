import time

from core.block import Block
from core.blockchain import Blockchain

#1. Initialize the network and set difficulty level to 4
print("Initializing the blockchain network...")
my_coin = Blockchain()
my_coin.difficulty = 4

#2. Package dummy transactions into a new block
print("Mining Block 1...")
tx_1 = [{"sender": "Troi", "receiver": "Mae", "amount": 12}]
block_1 = Block(1, tx_1)
my_coin.add_block(block_1)

print("Mining Block 2...")
tx_2 = [{"sender": "Liam", "receiver": "Clyde", "amount": 50}]
block_2 = Block(2, tx_2)
my_coin.add_block(block_2)

#4. Check the validity of the blockchain
print(f"Is the blockchain valid? {my_coin.is_chain_valid()}")