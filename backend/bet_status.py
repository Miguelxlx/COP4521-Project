from results import get_results
from bson import ObjectId 
from config import db
import time

bet_collection = db['bets']
transaction_collection = db['transactions']
user_collection = db['users']

user_id = None

def get_all_pending_bets():
    print("All pending")
    print(transaction_collection)
    try:
        # Query the bets collection for documents with matching user_id
        transaction_cursor = transaction_collection.find({'user_id': user_id})

        pending_bets = []
        for transaction in transaction_cursor:
            bet_ids = transaction['betIds']
            for bet in bet_ids:
                bet_cursor = bet_collection.find_one({'_id': bet})
                if bet_cursor and bet_cursor['status'] == 'Pending':
                    pending_bets.append(bet_cursor)

    except Exception as e:
        print(f"Error occurred while checking bets status: {e}")

    return pending_bets

def check_bet_status(bet):
    date = bet['gameTime'][:10]
    games = get_results(date)


    for game in games:
        if game['home_team'] == bet['homeTeam'] and game['visitor_team'] == bet['visitorTeam']:
            if game['visitor_points'] is None:
                return 0, 0
            else:
                status = get_bet_result(bet['wager'], game['home_points'],game['visitor_points'],bet['line'])

                if status == 1:
                    profit = (float(bet['amountPlaced']) * float(bet['odds']))
                    print('Profit: ',profit)
                    return 1, profit
                elif status == -1:
                    profit = - float(bet['amountPlaced'])
                    return -1 , 0 
                
    print("Did not find game")
    return 0, 0

def get_bet_result(bet_type,home_points,visitor_points,line):
    home_points = int(home_points)
    visitor_points = int(visitor_points)
    if (bet_type == "Over" and home_points + visitor_points > line)                                    or (bet_type == "Under" and home_points + visitor_points < line)                                   or (bet_type == "home_win" and home_points > visitor_points)                                         or(bet_type == "visitor_win" and home_points < visitor_points): 
        return 1
    else:
        return -1

def update_pending_bets(id):
    user_id = id
    pending_bets = get_all_pending_bets()

    for pending_bet in pending_bets:
        status, profit = check_bet_status(pending_bet)

        if status == 1:
            print("Won bet")

            bet_collection.update_one({"_id": pending_bet['_id']}, {"$set": {"status": 'W'}})
            bet_collection.update_one({"_id": pending_bet['_id']}, {"$set": {"profit": profit}})

            user = user_collection.find_one({'_id':user_id})
            new_balance = int(user['balance']) + profit 
            user_collection.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
        elif status == -1:
            print("Lost bet")
            bet_collection.update_one({"_id": pending_bet['_id']}, {"$set": {"status": 'L'}})
            bet_collection.update_one({"_id": pending_bet['_id']}, {"$set": {"profit": profit}})
            pass
        else:
            print("Bet still pending")

        time.sleep(5)

if __name__ == "__main__":
    user_id = ObjectId('661ecb2a3587f557bb71755f')
    update_pending_bets(user_id)

