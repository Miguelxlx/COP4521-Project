from pymongo import MongoClient
import datetime
import bcrypt
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

def setup():
    uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['bettingData']
    print('Connected to MongoDB Atlas successfully')

    # Drop existing collections
    db.users.drop()
    db.bets.drop()
    db.transactions.drop()
    print('Existing collections dropped')

    # Create hashed password
    hashed_password = bcrypt.hashpw("securepassword".encode('utf-8'), bcrypt.gensalt())

    # Users Collection
    user = {
        "username": "admin",
        "email": "admin@example.com",
        "password": hashed_password.decode('utf-8'),
        "role": "admin",
        "balance": 1000.0
    }
    user_id = db.users.insert_one(user).inserted_id
    print('Admin user initialized successfully')

    # Bets Collection
    bet = {
        "betTime": datetime.datetime.utcnow(),
        "homeTeam": "Golden State Warriors",
        "visitorTeam": "New Orleans Pelicans",
        "gameTime": "2024-04-13T02:11:03Z",
        "wager": "Over",
        "line": 213.5,
        "odds": 1.93,
        "amountPlaced": "10",
        "status": "W",
        "profit": 19.3
    }
    bet_id = db.bets.insert_one(bet).inserted_id
    print('Sample bet initialized successfully')

    # Transactions Collection
    transaction = {
        "userId": user_id,
        "transactionTime": datetime.datetime.utcnow(),
        "amount": 100,
        "betIds": [bet_id]
    }
    db.transactions.insert_one(transaction)
    print('Sample transaction initialized successfully')

if __name__ == "__main__":
    setup()