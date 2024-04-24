from config import app, db, logos
from bet_status import update_pending_bets
from odds import api_odds
from flask import request, jsonify
from bson import ObjectId
import bcrypt
import datetime


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
    # Retrieves list of dicts from odds script
    odds, remaing_requests = api_odds()

    # Add logos to dicts
    odds_and_logos = []
    for odd in odds:
        odd['home_img'] = logos[odd['home_team']]
        odd['visitor_img'] = logos[odd['visitor_team']]
        odds_and_logos.append(odd)
    
    return jsonify({"odds": odds_and_logos})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Retrieve fields from POST request
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Query MongoDB to check if email already taken
    user = db['users'].find_one({'email': email})

    if user:
        return jsonify({'valid': False, 'message': 'Email already in use'}), 400
    
    # Create hashed password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user entry and insert into db
    user = {
        "name": name,
        "email": email,
        "password": hashed_password.decode('utf-8'),
        "role": "user",
        "balance": 1000.0
    }

    db.users.insert_one(user)

    return jsonify({'valid': True, 'message': 'Registration valid!'})  

@app.route('/profile', methods=['GET']) 
def get_profile():
    data = request.get_json()
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
        # User info passed back to the frontend to be saved in the Redux
        user = {
            'id': str(user['_id']), 
            'username': user['name'],
            'email' : user['email'],
            'balance' : user['balance'],
            'role' : user['role']
        }
        return jsonify({"message": "Login successful", "user":user}), 200
    else:
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

    # Gets each bet from with their betId and converts ObjectIds to string
    bets = [convert_objectid(db.bets.find_one({"_id": id})) for id in bet_ids]

    return jsonify({"bets": bets})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    # Get userId from frontend
    user_id = request.args.get('user_id')

    # Get all transactions with userId
    transactions = db.transactions.find({"userId": ObjectId(user_id)})

    # Convert all objectIds to strings to avoid json error
    transaction_list = [convert_objectid(transaction) for transaction in transactions]

    return jsonify({"transactions": transaction_list})

@app.route('/submit_transaction', methods=['POST'])
def submit_transaction():
    data = request.get_json()

    # Form information
    user_id =  ObjectId(data['id'])
    transaction_amount = data['total']
    bet_slip = data['betSlip']

    time_placed = datetime.datetime.now()

    user = db.users.find_one({"_id": user_id})
    user_balance = user['balance']

    # Only place transaction if user has enough balance
    if user and user_balance >= transaction_amount:
        bet_ids = []

        # Insert all bets in transaction into bets collection
        for bet in bet_slip:
            wager = bet['team']
            odds = None

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

            # Save the betId returned from the db
            bet_ids.append(entry.inserted_id)
        
        # Insert transaction info and list of betIds into collection
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
    data = request.get_json()

    # update pending bets if games have finished
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

@app.route('/user_list', methods=['GET'])
def get_users():
    users = db.users.find()
    user_list = [convert_objectid(user) for user in users]

    return jsonify({"users": user_list})

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    user_id = ObjectId(data['id'])

    if not user_id:
        return jsonify({"message": "Invalid request, missing user_id"}), 400
    try:
        result = db.users.delete_one({"_id": user_id})
        if result.deleted_count > 0:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"message": "No user found with provided ID"}), 404
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
