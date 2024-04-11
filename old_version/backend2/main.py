from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import datetime
from config import app
from odds import api_odds
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGO_URI = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/test?retryWrites=true&w=majority"

uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['bettingData']

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains. Adjust as necessary for production.

client = MongoClient('localhost', 27017)
db = client['bettingData']

@app.route("/odds", methods=["GET"])
def get_odds():
    odds = api_odds()
    return jsonify({"odds": odds})

<<<<<<< HEAD
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
=======
@app.route('/check_registration', methods=['POST'])
def check_registration():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Query MongoDB to check if user exists with given email and password
    user = db['users'].find_one({'email': email})

    if not user:
        print('Registration valid!')
        return jsonify({'valid': True, 'message': 'Registration valid!'})
    else:
        print('Registration invalid!')
        return jsonify({'valid': False, 'message': 'Email already in use'}), 400
    
@app.route('/check_login', methods=['POST'])
def check_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Query MongoDB to check if user exists with given email and password
    user = db['users'].find_one({'email': email, 'password': password})

    if user:
        return jsonify({'valid': True, 'message': 'Login'})
    else:
        return jsonify({'valid': False, 'message': 'Invalid credentials.'}), 400


if __name__ == "__main__":
>>>>>>> c15456d2fa9fd28d3eba6e7a7f70a75a18c698b7
    app.run(debug=True)
