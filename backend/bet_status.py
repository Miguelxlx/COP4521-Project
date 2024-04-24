from results import get_results
from bson import ObjectId 
from config import db
import time

bets = db['bets']
transactions = db['transactions']
users = db['users']

def get_all_pending_bets(user_id):
    try:
        # Query the bets collection for documents with matching user_id
        transaction_cursor = transactions.find({'user_id': user_id})

        pending_bets = []

        # Must go through transactions first since the bets do not carry userId
        for transaction in transaction_cursor:
            bet_ids = transaction['betIds']
            for bet in bet_ids:
                bet_cursor = bets.find_one({'_id': bet})

                # Add bet to list if status is Pending
                if bet_cursor and bet_cursor['status'] == 'Pending':
                    pending_bets.append(bet_cursor)

    except Exception as e:
        print(f"Error occurred while checking bets status: {e}")

    return pending_bets

def check_bet_status(bet):
    # Truncate to only have the date
    date = bet['gameTime'][:10]

    # Retrieves all the games from that date
    games = get_results(date)

    for game in games:
        if game['home_team'] == bet['homeTeam'] and game['visitor_team'] == bet['visitorTeam']:
            # Game has not finished yet
            if game['visitor_points'] is None:
                return 0, 0
            else:
                # Compares outcome of the game with wager placed
                status = get_bet_result(bet['wager'], game['home_points'],game['visitor_points'],bet['line'])

                if status == 1:
                    # Calculates profit made based bet slip odds
                    profit = (float(bet['amountPlaced']) * float(bet['odds']))
                    return 1, profit
                elif status == -1:
                    profit = - float(bet['amountPlaced'])
                    return -1 , 0 
                

    # Did not find game
    return 0, 0

def get_bet_result(bet_type,home_points,visitor_points,line):
    home_points = int(home_points)
    visitor_points = int(visitor_points)

    if (bet_type == "Over" and home_points + visitor_points > line)                                    or (bet_type == "Under" and home_points + visitor_points < line)                                   or (bet_type == "home_win" and home_points > visitor_points)                                         or(bet_type == "visitor_win" and home_points < visitor_points): 
        return 1
    else:
        return -1

def update_pending_bets(user_id):
    # List of all bets whose outcome is still pending
    pending_bets = get_all_pending_bets(user_id)

    for pending_bet in pending_bets:
        # Check status of the bet
        status, profit = check_bet_status(pending_bet)

        # Won bet
        if status == 1:
            # Update bet status in db
            bets.update_one({"_id": pending_bet['_id']}, {"$set": {"status": 'W'}})
            bets.update_one({"_id": pending_bet['_id']}, {"$set": {"profit": profit}})

            # Update user balance
            user = users.find_one({'_id':user_id})
            new_balance = int(user['balance']) + profit 
            users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
        # Lost bet
        elif status == -1:
            # Update bet status in db
            bets.update_one({"_id": pending_bet['_id']}, {"$set": {"status": 'L'}})
            bets.update_one({"_id": pending_bet['_id']}, {"$set": {"profit": profit}})

        # To avoid errors from api
        time.sleep(5)


