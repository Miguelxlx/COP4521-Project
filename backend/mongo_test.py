from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId  # Import ObjectId here
from datetime import datetime  # Ensure datetime is imported if you're going to use it

uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    dbname = 'bettingData'
    db = client[dbname]  # Access the specified database
    
    # Access the transactions collection directly
    collection = db['transactions']

    # Define the document to be inserted
    doc = {
        "_id": ObjectId("661ee24267ed7cda8111c435"),
        "userid": ObjectId("6618527fed36ee0d30c03c85"),
        "date": datetime.strptime("2024-04-16T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
        "amount": -150,
        "bets": [
            ObjectId("661ee4ea6c90df95030791a8"),
            ObjectId("661ee5486c90df95030791a9"),
            ObjectId("661ee54f6c90df95030791aa")
        ]
    }

    # Insert the document into the collection
    collection.insert_one(doc)
    print("Document inserted successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
