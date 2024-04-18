from results import get_results
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId 
import time

uri = "mongodb+srv://miguelxlx123:xAVZHEXrJhFN4XBa@cop4521.ubpj23p.mongodb.net/?retryWrites=true&w=majority&appName=COP4521"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['bettingData']

transaction_collection = db['transactions']
bet_collection = db['bets']
user_collection = db['users']


def get_all_pending_bets(user_id):
    try:
        # Query the bets collection for documents with matching userId
        transaction_cursor = transaction_collection.find({'userId': user_id})

        pending_bets = []
        for transaction in transaction_cursor:
            bet_ids = transaction['betIds']
            for bet in bet_ids:
                bet_cursor = bet_collection.find_one({'_id': bet})
                if bet_cursor['status'] == 'Pending':
                    pending_bets.append(bet_cursor)
    except Exception as e:
        print(f"Error occurred while checking bets status: {e}")

    return pending_bets

def check_bet(bet,userId):
    date = bet['gameTime'][:10]
    games = get_results(date)


    for game in games:
        if game['home_team'] == bet['homeTeam'] and game['visitor_team'] == bet['visitorTeam']:
            if game['visitor_points'] is None:
                return 0, 0
            else:
                status = bet_status(bet['wager'], game['home_points'],game['visitor_points'],bet['line'])

                if status == 1:
                    print("amountPlaced:",int(bet['amountPlaced']))
                    print("Odds:",int(bet['odds']))
                    profit = (int(bet['amountPlaced']) * int(bet['odds']))
                    print('Profit: ',profit)
                    return 1, profit
                elif status == -1:
                    profit = - int(bet['amountPlaced'])
                    return -1 , 0 
                
    print("Did not find game")
    return 0, 0

def bet_status(bet_type,home_points,visitor_points,line):
    home_points = int(home_points)
    visitor_points = int(visitor_points)
    if (bet_type == "Over" and home_points + visitor_points > line)                                    or (bet_type == "Under" and home_points + visitor_points < line)                                   or (bet_type == "home_win" and home_points > visitor_points)                                         or(bet_type == "visitor_win" and home_points < visitor_points): 
        return 1
    else:
        return -1

def checkPendingBets(userId):
    print('Check pending bets')
    pending_bets = get_all_pending_bets(userId)

    for pending_bet in pending_bets:
        status, profit = check_bet(pending_bet,userId)
        if status == 1:
            print("Won bet")

            bet_collection.update_one({"_id": pending_bet['_id']}, {"$set": {"status": 'W'}})
            bet_collection.update_one({"_id": pending_bet['_id']}, {"$set": {"profit": profit}})

            user = user_collection.find_one({'_id':userId})
            new_balance = int(user['balance']) + profit 
            user_collection.update_one({"_id": userId}, {"$set": {"balance": new_balance}})
        elif status == -1:
            print("Lost bet")
            bet_collection.update_one({"_id": pending_bet['_id']}, {"$set": {"status": 'L'}})
            bet_collection.update_one({"_id": pending_bet['_id']}, {"$set": {"profit": profit}})
            pass
        else:
            print("Bet still pending")

        time.sleep(5)



if __name__ == "__main__":
    userId = ObjectId('661ecb2a3587f557bb71755f')
    checkPendingBets(userId)

