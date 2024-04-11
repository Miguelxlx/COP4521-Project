from flask import request, jsonify
from config import app
from odds import api_odds
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGO_URI = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/test?retryWrites=true&w=majority"

uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['bettingData']

@app.route("/odds", methods=["GET"])
def get_odds():
    odds = api_odds()
    return jsonify({"odds": odds})

@app.route('/check_registration', methods=['POST'])
def check_registration():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Query MongoDB to check if user exists with given email and password
    user = db['users'].find_one({'email': email})

    if not user:
        print('Registration valid!')
        return jsonify({'valid': True, 'message': 'Registration valid!'})
    else:
        print('Registration invalid!')
        return jsonify({'valid': False, 'message': 'Email already in use'}), 400
    
@app.route('/check_login', methods=['POST'])
def check_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Query MongoDB to check if user exists with given email and password
    user = db['users'].find_one({'email': email, 'password': password})

    if user:
        return jsonify({'valid': True, 'message': 'Login'})
    else:
        return jsonify({'valid': False, 'message': 'Invalid credentials.'}), 400


if __name__ == "__main__":
    app.run(debug=True)
