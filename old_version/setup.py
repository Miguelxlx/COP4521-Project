from pymongo import MongoClient
import datetime
import bcrypt

def setup():
    client = MongoClient('localhost', 27017)
    db = client['bettingData']
    print('Connected to MongoDB successfully')
    

    # Create hashed password
    hashed_password = bcrypt.hashpw("securepassword".encode('utf-8'), bcrypt.gensalt())
    
    # Users Collection
    user = {
        "username": "admin",
        "email": "admin@example.com",
        "password": hashed_password.decode('utf-8'),
        "role": "admin",  # Use "user" for regular users, "admin" for administrators
        "balance": 1000.0
    }
    user_id = db.users.insert_one(user).inserted_id
    print('Collection users initialized successfully')

    # Transactions Collection
    transaction = {
        "userid": user_id,
        "date": datetime.datetime.utcnow(),
        "amount": -150.0,
        "bets": []  # Placeholder for embedding bet documents or references
    }
    transaction_id = db.transactions.insert_one(transaction).inserted_id
    print('Collection transactions initialized successfully')

    # Bets Collection
    bet = {
        "transactionid": transaction_id,
        "gameid": "Game123",
        "bettype": "Over",
        "price": 50.0,
        "line": 200,
        "status": "Pending"
    }
    db.bets.insert_one(bet)
    print('Collection bets initialized successfully')

    # Games Collection
    game = {
        "date": datetime.datetime.utcnow(),
        "hometeam": "HTM",
        "awayteam": "ATM",
        "homefinalscore": 100,
        "awayfinalscore": 90
    }
    db.games.insert_one(game)
    print('Collection games initialized successfully')

if __name__ == "__main__":
    setup()
