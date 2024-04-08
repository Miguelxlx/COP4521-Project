from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/test?retryWrites=true&w=majority"

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_URI)

db = client.get_database()

# Sample route to test MongoDB connection
@app.route('/')
def index():
    collection_names = db.list_collection_names()

    # Print the collection names
    print("Collections in the database:")
    for name in collection_names:
        print(name)

    return f"Nothing"

if __name__ == '__main__':
    app.run(debug=True)