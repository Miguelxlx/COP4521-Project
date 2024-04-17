from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import bcrypt
import datetime
from config import app
from odds import api_odds
from odds_sample import get_odd_sample
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt
from bson import ObjectId

MONGO_URI = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/test?retryWrites=true&w=majority"

uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['bettingData']

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains. Adjust as necessary for production.

def convert_objectid(obj):
    """Recursively convert ObjectId to string in nested documents."""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = convert_objectid(value)
    elif isinstance(obj, list):
        obj = [convert_objectid(item) for item in obj]
    return obj


@app.route("/odds", methods=["GET"])
def get_odds():
    # odds, remaing_requests = api_odds()
    odds = get_odd_sample()
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
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):

        user = {
            'id': str(user['_id']), 
            'username': user['name']
        }

        print('successful login')
        return jsonify({"message": "Login successful", "user":user}), 200
    else:
        # Failed login
        return jsonify({"message": "Invalid email or password"}), 403

# @app.route('/transactions', methods=['GET'])
# def get_transactions():
#     user_id = request.args.get('user_id')  # The user ID should be passed as a query parameter
#     transactions = db.transactions.find({"userid": user_id})
#     transaction_list = [trans for trans in transactions]  # Convert cursor to list
#     return jsonify({"transactions": transaction_list})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = db.transactions.find()
    transaction_list = [convert_objectid(transaction) for transaction in transactions]
    return jsonify({"transactions": transaction_list})

@app.route('/submit_transaction', methods=['POST'])
def submit_transaction():
    data = request.get_json()

    user_id =  ObjectId(data['id'])
    transaction_amount = data['total']
    bet_slip = data['betSlip']
    time_placed = datetime.datetime.now()
    print(bet_slip)

    user = db.users.find_one({"_id": user_id})
    user_balance = user['balance']

    if user and user_balance >= transaction_amount:
        bet_ids = []
        for bet in bet_slip:
            print('bet')
            wager = bet['team']
            odds = 0

            if wager == 'Over':
                odds = bet['over_price']
            if wager == 'Under':
                odds = bet['under_price']
            if wager == 'home_win':
                odds = bet['h2h_home_price']
            if wager == 'visitor_win':
                odds = bet['h2h_visitor_price']

            bet_entry = {
                'betTime': time_placed,
                'homeTeam': bet['home_team'],
                'visitorTeam': bet['visitor_team'],
                'gameTime': bet['time'],
                'wager': wager, 
                'line' : bet['line'], 
                'odds': odds, 
                'amountPlaced': bet['amount'], 
                'status': 'Pending'
            }

            entry = db.bets.insert_one(bet_entry)
            print('inserted bet')
            bet_ids.append(entry.inserted_id)
        
        print('transaction')
        transaction = {
            "userId" : user_id,
            "transactionTime" : time_placed,
            "amount": transaction_amount,
            "betIds": bet_ids
        }

        db.transactions.insert_one(transaction)

        print('inserted transaction')
    
        db.users.update_one({"_id": user_id}, {"$set": {"balance": user_balance - transaction_amount}})

        print('updated user')

        return jsonify({"message": "Transaction Success"}), 200
    else:
        # Failed login
        return jsonify({"message": "Transaction Failed"}), 403


if __name__ == '__main__':
    app.run(debug=True)
