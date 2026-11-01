from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient

from core.block import Block
from core.blockchain import Blockchain

app = Flask(__name__)
my_coin = Blockchain()

#Connecto to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["genesis_database"]
mempool = db["pending_transactions"]
completed_transactions = db["completed_transactions"]

@app.route('/')
def home():
    # Renders the HTML template for the home page
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_transaction():
    # Extract input data
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']
    # Create a transaction dictionary
    transaction = {
        "sender": sender,
        "receiver": receiver,
        "amount": amount
    }
    # Store the transaction in the mempool
    mempool.insert_one(transaction)
    return redirect(url_for('home'))  # Redirect back to the home page

@app.route('/mine', methods=['POST'])
def mine_button_clicked():
    # Fetch all pending transactions from the mempool
    pending_transactions = list(mempool.find({}, {"_id": 0}))
    
    if pending_transactions:
        # Create new block
        new_block = Block(len(my_coin.chain), pending_transactions)
        my_coin.add_block(new_block)
        # Store completed transactions in the completed_transactions collection
        completed_transactions.insert_many(pending_transactions)
        # Clear the mempool after mining
        mempool.delete_many({})
        
        # Redirect back to the home page
        return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True)