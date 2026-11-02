import random
import smtplib
import uuid
from email.mime.text import MIMEText

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

from core.block import Block
from core.blockchain import Blockchain

app = Flask(__name__)
CORS(app)  # Opens the API to the React frontend

SECRET_KEY = "genesis_secret_key"

my_coin = Blockchain()

#Connecto to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["genesis_database"]
mempool = db["pending_transactions"]
completed_collection = db["completed_transactions"]
users_collection = db["users"]

#----------------------------------------------
# LOGIN/REGISTRATION/PASSWORD RESET LOGIC

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400
    
    # Check if the user already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"message": "Username is already taken."}), 400
    
    if users_collection.find_one({"email": email}):
        return jsonify({"message": "Email is already registered."}), 400
    
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)
    
    # Store the new user in the database
    new_user = {
        "username": username,
        "email": email,
        "password": hashed_password
    }
    
    users_collection.insert_one(new_user)
    
    return jsonify({"message": "Registered successfully."}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    
    user = users_collection.find_one({"username": data.get("username")})
    
    if user and check_password_hash(user["password"], data.get("password")):
        token = jwt.encode({
            "username": user["username"],
            "exp": datetime.datime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token, "username": user["username"]}), 200
    
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    user = users_collection.find_one({"email": email})
    
    if not user:
        return jsonify({"error": "Email not found."}), 404
    
    # Generate a 4-digit PIN and save it to the database
    reset_pin = str(random.randint(1000,9999))
    users_collection.update_one({"email": email}, {"$set": {"reset_pin": reset_pin}})
    
    # Configure and send email
    msg = MIMEText(f"Your Genesis password reset PIN is: {reset_pin}")
    msg['Subject'] = 'Genesis password reset'
    msg['From'] = 'noreply@genesis.com'
    msg['To'] = email
    
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("f559f0c41aaf20","297dc4f1233e9e")
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        
    return jsonify({"message": "Password reset PIN sent to email"}), 200

#----------------------------------------------
# Mining Module Logic

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    # React loads the UI tables
    pending = list(mempool.find({}, {"_id": 0}))
    completed = list(completed_collection.find({}, {"_id": 0}))
    return jsonify({
        "pending": pending,
        "completed": completed
    })

@app.route('/api/add', methods=['POST'])
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

@app.route('/api/mine', methods=['POST'])
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
    
if __name__ == '__main__':
    app.run(debug=True)