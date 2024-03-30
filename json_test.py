# JSON data
data = [{
        'id': '5198ff67982e7c0097a7f79726c8c195', 
        'sport_key': 'basketball_nba', 
        'sport_title': 'NBA', 
        'commence_time': '2024-03-30T21:00:00Z', 
        'home_team': 'New Orleans Pelicans',
        'away_team': 'Boston Celtics', 
        'bookmakers': 
          [{
                'key': 'fanduel', 
                'title': 'FanDuel',
                'last_update': '2024-03-30T05:33:32Z',
                'markets':
                    [
                        {
                            'key': 'h2h', 
                            'last_update': '2024-03-30T05:33:32Z', 
                            'outcomes': 
                            [
                                { 'name': 'Boston Celtics', 'price': 1.45}, 
                                {'name': 'New Orleans Pelicans', 'price': 2.84}
                            ]
                        }, 
                        {'key': 'totals', 
                            'last_update': '2024-03-30T05:33:32Z', 
                            'outcomes': 
                            [
                                {'name': 'Over', 'price': 1.91, 'point': 223.5},
                                {'name': 'Under', 'price': 1.91, 'point': 223.5}
                            ]
                        }
                    ]
        }
    ]
}]
# Parsing JSON data
for game in data:
    time = game["commence_time"]
    home_team = game["home_team"]
    away_team = game["away_team"]
    line = game["bookmakers"][0]["markets"][1]["outcomes"][0]["point"]
    over_price = game["bookmakers"][0]["markets"][1]["outcomes"][0]["price"]
    under_price = game["bookmakers"][0]["markets"][1]["outcomes"][1]["price"]

    h2h1 = (game["bookmakers"][0]["markets"][0]["outcomes"][0]["name"],game["bookmakers"][0]["markets"][0]["outcomes"][0]["price"])
    h2h2 = (game["bookmakers"][0]["markets"][0]["outcomes"][1]["name"],game["bookmakers"][0]["markets"][0]["outcomes"][1]["price"])
    
    print("Time:", time)
    print("Home Team:", home_team)
    print("Away Team:", away_team)
    print("Line:", line)
    print("Over Price:", over_price)
    print("Under Price:", under_price)

    print(f"{h2h1[0]} to win: {h2h1[1]}")
    print(f"{h2h2[0]} to win: {h2h2[1]}")
    print("\n")