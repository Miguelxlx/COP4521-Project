from flask import request, jsonify
import bcrypt
import datetime
from config import app
from odds import api_odds
from odds_sample import get_odd_sample
from bson import ObjectId
from bet_status import update_pending_bets
from config import app, db
from flask import session

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
    # Retrieves a list of dictionaries containing odds information
    # odds, remaing_requests = api_odds()
    odds = get_odd_sample()
    return jsonify({"odds": odds})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Retrieve fields from POST request
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Query MongoDB to check if user exists with given email and password
    user = db['users'].find_one({'email': email})

    if user:
        return jsonify({'valid': False, 'message': 'Email already in use'}), 400
    
    # Create hashed password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user entry en insert into db
    user = {
        "name": name,
        "email": email,
        "password": hashed_password.decode('utf-8'),
        "role": "user",  # Use "user" for regular users, "admin" for administrators
        "balance": 1000.0
    }

    db.users.insert_one(user)
    return jsonify({'valid': True, 'message': 'Registration valid!'})  

@app.route('/profile', methods=['GET']) 
def get_profile():

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    # Fetch user details from the database
    user = db['users'].find_one({"email": email})
    if user:
        # Remove sensitive data before sending it to the client
        user.pop('password', None)  # Remove password if it's stored in the user document
        user_data = {
            'name': user.get('name', ''),
            'email': user.get('email', ''),
            'balance': user.get('balance', 0.0)
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404
   
@app.route('/check_login', methods=['POST'])
def check_login():
    data = request.get_json()
    user = db.users.find_one({"email": data['email']})

    # Checks if user exists and if password matches
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
        # User info passed back to the frontend
        user = {
            'id': str(user['_id']), 
            'username': user['name'],
            'email' : user['email'],
            'balance' : user['balance'],
            'role' : user['role']
        }

        print(user)

        print('successful login',user)
        return jsonify({"message": "Login successful", "user":user}), 200
    else:
        # Failed login
        return jsonify({"message": "Invalid email or password"}), 403
    
@app.route('/bets', methods=['GET'])
def get_bets():
    user_id = request.args.get('user_id') 

    # Find all transactions with user id
    transactions = db.transactions.find({"userId": ObjectId(user_id)})

    # Get all the bet ids associated with transactions
    bet_ids = []
    for transaction in transactions:
        bet_ids.extend(transaction['betIds'])

    bets = [convert_objectid(db.bets.find_one({"_id": id})) for id in bet_ids]

    return jsonify({"bets": bets})


# @app.route('/transactions', methods=['GET'])
# def get_transactions():
#     user_id = request.args.get('user_id')  # The user ID should be passed as a query parameter
#     transactions = db.transactions.find({"userid": user_id})
#     transaction_list = [trans for trans in transactions]  # Convert cursor to list
#     return jsonify({"transactions": transaction_list})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id')  # Expect user ID as a query parameter
    transactions = db.transactions.find({"userId": ObjectId(user_id)})
    transaction_list = [convert_objectid(transaction) for transaction in transactions]

    return jsonify({"transactions": transaction_list})


@app.route('/submit_transaction', methods=['POST'])
def submit_transaction():
    data = request.get_json()

    user_id =  ObjectId(data['id'])
    transaction_amount = data['total']
    bet_slip = data['betSlip']

    time_placed = datetime.datetime.now()

    user = db.users.find_one({"_id": user_id})
    user_balance = user['balance']

    if user and user_balance >= transaction_amount:
        bet_ids = []

        # Insert all the bets into collection and retrieve their ids
        for bet in bet_slip:
            print(bet)
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
            bet_ids.append(entry.inserted_id)
        
        # Insert transaction into collection and add list of betIds
        transaction = {
            "userId" : user_id,
            "transactionTime" : time_placed,
            "amount": transaction_amount,
            "betIds": bet_ids
        }

        db.transactions.insert_one(transaction)
    
        # Update user balance
        db.users.update_one({"_id": user_id}, {"$set": {"balance": user_balance - transaction_amount}})

        # User info passed back to the frontend
        user = {
            'id': str(user['_id']), 
            'username': user['name'],
            'email' : user['email'],
            'balance' : user_balance - transaction_amount,
            'role' : user['role']
        }

        return jsonify({"message": "Transaction Success", "user":user}), 200
    else:
        return jsonify({"message": "Transaction Failed"}), 403

@app.route('/check_pending_bets', methods=['POST'])
def checkPendingBets():
    print("CheckPedning")
    data = request.get_json()
    update_pending_bets(ObjectId(data['id']))

    return jsonify({"message": "Update Successful"}), 200

@app.route('/update_balance', methods=['POST'])
def update_balance():
    data = request.get_json()
    user_id = ObjectId(data['id'])
    new_balance = data['newBalance']

    if not user_id or not new_balance:
        return jsonify({"message": "Invalid request, missing user_id or newBalance"}), 400

    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": new_balance}})
            user = {
                'id': str(user['_id']),
                'username': user['name'],
                'email' : user['email'],
                'balance' : new_balance,
                'role' : user['role']
            }
            return jsonify({"message": "Balance updated successfully", "user":user}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while updating balance"}), 500

@app.route('/upgrade_premium', methods=['POST'])
def upgrade_premium():
    data = request.get_json()
    user_id = ObjectId(data['id'])

    if not user_id:
        return jsonify({"message": "Invalid request, missing user_id"}), 400
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"role": "premium"}})
            user = {
                'id': str(user['_id']),
                'username': user['name'],
                'email' : user['email'],
                'balance' : user['balance'] - 15,
                'role' : "premium"
            }
            return jsonify({"message": "Upgraded to premium successfully", "user":user}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while upgrading to premium"}), 500

"""
bet_entry
"""

if __name__ == '__main__':
    app.run(debug=True)
