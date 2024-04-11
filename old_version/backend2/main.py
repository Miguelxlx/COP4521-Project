from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import datetime
from config import app
from odds import api_odds
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

MONGO_URI = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/test?retryWrites=true&w=majority"

uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['bettingData']

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains. Adjust as necessary for production.

@app.route("/odds", methods=["GET"])
def get_odds():
    odds = api_odds()
    return jsonify({"odds": odds})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Query MongoDB to check if user exists with given email and password
    user = db['users'].find_one({'email': email})

    if user:
        return jsonify({'valid': False, 'message': 'Email already in use'}), 400
    
    # Create hashed password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Users Collection
    user = {
        "name": name,
        "email": email,
        "password": hashed_password.decode('utf-8'),
        "role": "user",  # Use "user" for regular users, "admin" for administrators
        "balance": 1000.0
    }

    db.users.insert_one(user)
    return jsonify({'valid': True, 'message': 'Registration valid!'})
    
    
@app.route('/check_login', methods=['POST'])
def check_login():
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
