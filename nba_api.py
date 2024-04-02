import requests

url = "https://api-nba-v1.p.rapidapi.com/games"

querystring = {"date":"2024-04-01"}

headers = {
	"X-RapidAPI-Key": "b32a2e36fbmshd22362ae58d4d2fp142d89jsnfd4f85576b32",
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
nba_json = response.json()

games = []

print(nba_json['response'][0]['season'])

for game in nba_json['response']:
    visitor_name = game['teams']['visitors']['name']
    visitor_points = game['scores']['visitors']['points']
    home_name = game['teams']['home']['name']
    home_points = game['scores']['home']['points']

    g = {'visitor_name':visitor_name,'visitor_points':visitor_points,
         'home_name':home_name,'home_points':home_points}
    
    games.append(g)

print(games)