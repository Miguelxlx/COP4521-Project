import requests

API_KEY = '2e45b517a7f1b28c45fac18d4eefd331'

SPORT = 'basketball_nba'
REGIONS = 'us' 
MARKETS = 'totals,h2h' 
ODDS_FORMAT = 'decimal' 
DATE_FORMAT = 'iso'
BOOKMAKERS = 'fanduel'

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
        'bookmakers': BOOKMAKERS
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
else:
    odds_json = odds_response.json()

    for game in odds_json:
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

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])
