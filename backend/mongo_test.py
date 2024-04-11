from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    dbname = 'bettingData'
        # Access the specified database
    db = client[dbname]
    
    # Specify the collections to retrieve entries from
    collections_to_query = ['transactions', 'games', 'users']
    
    for collection_name in collections_to_query:
        # Access the collection
        collection = db[collection_name]
        
        # Retrieve all entries (documents) from the collection
        entries = collection.find()
        
        # Print the entries (documents) from the collection
        print(f"Entries in the '{collection_name}' collection:")
        for entry in entries:
            print(entry)
        print()  # Add a blank line for separation

except Exception as e:
    print(e)

