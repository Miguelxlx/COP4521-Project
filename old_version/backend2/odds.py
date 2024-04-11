import requests

API_KEY = '9c2217366d70c38fe65769268e689c76'

SPORT = 'basketball_nba'
REGIONS = 'us' 
MARKETS = 'totals,h2h' 
ODDS_FORMAT = 'decimal' 
DATE_FORMAT = 'iso'
BOOKMAKERS = 'fanduel'

def api_odds():

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
        return None
    else:
        odds_json = odds_response.json()

        games = []
        for game in odds_json:
            time = game["commence_time"]
            home_team = game["home_team"]
            visitor_team = game["away_team"]
            line = game["bookmakers"][0]["markets"][1]["outcomes"][0]["point"]
            over_price = game["bookmakers"][0]["markets"][1]["outcomes"][0]["price"]
            under_price = game["bookmakers"][0]["markets"][1]["outcomes"][1]["price"]
            
            # Onlye need the date for the key
            key = time[0:10] + home_team + visitor_team

            h2h_home_price = None
            h2h_visitor_price = None

            if game["bookmakers"][0]["markets"][0]["outcomes"][0]["name"] == home_team:
                h2h_home_price = game["bookmakers"][0]["markets"][0]["outcomes"][0]["price"]
                h2h_visitor_price = game["bookmakers"][0]["markets"][0]["outcomes"][1]["price"]
            else:
                h2h_home_price = game["bookmakers"][0]["markets"][0]["outcomes"][1]["price"]
                h2h_visitor_price = game["bookmakers"][0]["markets"][0]["outcomes"][0]["price"]

            g = {"key":key, "time":time,"home_team":home_team,"visitor_team":visitor_team,"line":line,"over_price":over_price,"under_price":under_price, "h2h_home_price": h2h_home_price, 'h2h_visitor_price':h2h_visitor_price}
            
            games.append(g)

        return games

        # Games
        # List of dicts for each game
        # Each game dict has time, home team, away team, line, over and under price and h2h dict
        # h2h dict has two dicts with each team_name and price

        # Check the usage quota
        # print('Remaining requests', odds_response.headers['x-requests-remaining'])
        # print('Used requests', odds_response.headers['x-requests-used'])

if __name__ == "__main__":
    print(api_odds())