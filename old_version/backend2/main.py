from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import datetime
from config import app
from odds import api_odds

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains. Adjust as necessary for production.

client = MongoClient('localhost', 27017)
db = client['bettingData']

@app.route("/odds", methods=["GET"])
def get_odds():
    odds = api_odds()
    return jsonify({"odds": odds})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = db.users.find_one({"email": data['email']})
    if user:
        return jsonify({"message": "User already exists"}), 409

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = {
        "username": data['username'],
        "email": data['email'],
        "password": hashed_password.decode('utf-8'),
        "role": "user",
        "balance": 50.0  # Start each new user with $50
    }
    db.users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.users.find_one({"email": data['email']})
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
        # Normally, you would return a session token or a JWT token
        return jsonify({"message": "Login successful", "balance": user['balance']}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/bet', methods=['POST'])
def place_bet():
    data = request.get_json()
    user = db.users.find_one({"email": data['email']})
    if user and user['balance'] >= data['amount']:
        new_balance = user['balance'] - data['amount']
        db.users.update_one({"email": data['email']}, {"$set": {"balance": new_balance}})
        bet = {
            "userid": user['_id'],
            "gameid": data['gameid'],
            "bettype": data['bettype'],
            "price": data['amount'],
            "line": data['line'],
            "status": "Pending"
        }
        db.bets.insert_one(bet)
        return jsonify({"message": "Bet placed successfully", "new_balance": new_balance}), 200
    else:
        return jsonify({"message": "Insufficient balance"}), 403

if __name__ == '__main__':
    app.run(debug=True)
