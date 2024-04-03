from pymongo import MongoClient
import datetime

def setup():
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)  # Adjust the connection string as necessary
    db = client['bettingData']
    print('Connected to MongoDB successfully')

    # Accounts Collection
    account = {
        "Username": "admin",
        "Status": "Active",
        "Email": "admin@example.com",
        "Password": "securepassword",
        "Balance": 1000.0,
        "Transactions": []  # Placeholder for transaction documents
    }
    account_id = db.Account.insert_one(account).inserted_id
    print('Collection Account initialized successfully')

    # Transactions Collection
    transaction = {
        "AccountID": account_id,
        "Date": datetime.datetime.utcnow(),
        "Amount": -150.0,
        "Bets": []  # Placeholder for embedding bet documents or references
    }
    transaction_id = db.Transaction.insert_one(transaction).inserted_id
    print('Collection Transaction initialized successfully')

    # BetsInTransaction (This concept is typically integrated directly into the Transactions collection in MongoDB)
    bet_in_transaction = {
        "TransactionID": transaction_id,
        "BetID": [],  # This could be an array of BetIDs associated with the transaction
    }
    # In MongoDB, it's more common to embed this data directly in the Transaction or Account document

    # Bet Collection
    bet = {
        "AccountID": account_id,
        "GameID": "Game123",
        "BetType": "Over",
        "Price": 50.0,
        "Line": 200,
        "Status": "Pending"
    }
    bet_id = db.Bet.insert_one(bet).inserted_id
    print('Collection Bet initialized successfully')

    # Adding the BetID to the Transaction's Bet array
    db.Transaction.update_one({"_id": transaction_id}, {"$push": {"Bets": bet_id}})

    # Game Collection
    game = {
        "Date": datetime.datetime.utcnow(),
        "HomeTeam": "HTM",
        "AwayTeam": "ATM",
        "HomeFinalScore": 100,
        "AwayFinalScore": 90
    }
    db.Game.insert_one(game)
    print('Collection Game initialized successfully')

if __name__ == "__main__":
    setup()
