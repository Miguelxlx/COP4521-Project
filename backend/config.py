from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import os

# MongoDB uri
uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['bettingData']

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains


logos = None
curr_dir = os.path.dirname(__file__)
file_path = os.path.join(curr_dir, 'logos', 'logos.json')
with open(file_path, 'r') as file:
    logos = json.load(file)
