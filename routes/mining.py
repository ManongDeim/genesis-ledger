import uuid

from flask import Blueprint, jsonify, request

from core.block import Block
from core.blockchain import Blockchain
from db import db

#Define BLUEPRINT
mining_bp = Blueprint('mining', __name__)
mempool = db["pending_transactions"]
completed_collection = db["completed_transactions"]

my_coin = Blockchain()

# Mining Module Logic

@mining_bp.route('/api/transactions', methods=['GET'])
def get_transactions():
    # React loads the UI tables
    pending = list(mempool.find({}, {"_id": 0}))
    completed = list(completed_collection.find({}, {"_id": 0}))
    return jsonify({
        "pending": pending,
        "completed": completed
    })

@mining_bp.route('/api/add', methods=['POST'])
def add_transaction():
    data = request.json
    # Create a transaction dictionary
    transaction = {
        "transaction_id": uuid.uuid4().hex,  # Generate a unique transaction ID
        "sender": data.get("sender"),
        "receiver": data.get("receiver"),
        "amount": data.get("amount")
    }
    # Store the transaction in the mempool
    mempool.insert_one(transaction)
    return jsonify({"message": "Transaction queued"})

@mining_bp.route('/api/mine', methods=['POST'])
def mine_button_clicked():
    # Fetch all pending transactions from the mempool
    pending_transactions = list(mempool.find({}, {"_id": 0}))
    
    if pending_transactions:
        # Create new block
        new_block = Block(len(my_coin.chain), pending_transactions)
        my_coin.add_block(new_block)
        
        final_block_id = f"Block-{new_block.hash}"
        
        for tx in pending_transactions:
            tx["block_id"] = final_block_id
        # Store completed transactions in the completed_transactions collection
        completed_collection.insert_many(pending_transactions)
        # Clear the mempool after mining
        mempool.delete_many({})
        return jsonify({"message": "Block mined successfully", "block_id": final_block_id})
        
    
    return jsonify({"message": "No pending transactions."})