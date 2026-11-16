import datetime
import random
import smtplib
from email.mime.text import MIMEText
from functools import wraps

import jwt
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from db import db

#Define BLUEPRINT
auth_bp = Blueprint('auth', __name__)
users_collection = db["users"]
SECRET_KEY = "genesis_secret_key"

# LOGIN/REGISTRATION/PASSWORD RESET LOGIC

@auth_bp.route('/api/register', methods=['POST'])
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

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    
    user = users_collection.find_one({"username": data.get("username")})
    
    if user and check_password_hash(user["password"], data.get("password")):
        token = jwt.encode({
            "username": user["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token, "username": user["username"]}), 200
    
    return jsonify({"error": "Invalid username or password"}), 401

@auth_bp.route('/api/forgot-password', methods=['POST'])
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

def token_required (f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split("")[1]
            
        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data["username"]
        except Exception as e:
            return jsonify({"error": "Token is invalid or expired"}), 401
        
        
        return f(current_user, *args, **kwargs)
    return decorated