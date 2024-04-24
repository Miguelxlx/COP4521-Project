import requests
import json

url = "https://api-nba-v1.p.rapidapi.com/games"

headers= {
    "X-RapidAPI-Key": "b32a2e36fbmshd22362ae58d4d2fp142d89jsnfd4f85576b32",
    "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }


# We are actually not fetching from this function for the running website since there are some mismatches in the team names that we edited directly in the json logos file
def get_logos():
    querystring = {"season":"2022"}
    response = requests.get(url, headers=headers, params=querystring)
    nba_json = response.json()

    team_logos = {}

    # Retrieve logos for every team
    for team in nba_json['response']:
        team_name = team['teams']['home']['name']
        if team_name == 'LA Clippers':
            team_name = 'Los Angeles Clippers'

        logo = team['teams']['home']['logo']
        team_logos[team_name] = logo

    return team_logos

# date has to be in the format 'YYYY-MM-DD'
def get_results(date):
    querystring = {"date":date}
    response = requests.get(url, headers=headers, params=querystring)
    nba_json = response.json()

    results = []

    # Store all games from that date
    for game in nba_json['response']:
        visitor_name = game['teams']['visitors']['name']
        visitor_points = game['scores']['visitors']['points']
        home_name = game['teams']['home']['name']
        home_points = game['scores']['home']['points']

        result = {'visitor_team':visitor_name,'visitor_points':visitor_points,
            'home_team':home_name,'home_points':home_points}
        
        results.append(result)

    return results
