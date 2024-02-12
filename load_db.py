import requests
import json
import sqlite3

ROSTER = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{}/roster"
SKILL_LIST = ["QB",'RB', 'WR', 'TE']

def get_players(data):
    players = data['athletes'][0]["items"]
    for player in players:
        id = player['id']
        name = player['fullName']
        position = player['position']['abbreviation']
        team = data['team']['displayName']
        if position not in SKILL_LIST:
            continue
        cursor.execute('insert into players values(?,?,?,?)', [id,name,position,team])

connection = sqlite3.connect('myDb.db')
cursor = connection.cursor()
cursor.execute('create table players (ESPN_id, name, position, team)')
cursor.execute('create table matchups (away, home)')

for i in range(1,35):
    if i == 31 or i == 32:
        continue
    response = requests.get(ROSTER.format(str(i)))
    data = json.loads(response.text)
    get_players(data)

response = requests.get('https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events')
data = json.loads(response.text)

matchups = {}
for value in data['items']:
    new_resp = requests.get(value['$ref'])
    new_data = json.loads(new_resp.text)
    away = new_data['name'].split(" at ")[0]
    home = new_data['name'].split(" at ")[1]
    cursor.execute('insert into matchups values (?,?)',[away,home])

connection.commit()
connection.close()