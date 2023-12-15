from bs4 import BeautifulSoup as bs
import espn_data
import pandas as pd
import requests
import sqlite3

INVALID_PLAYER_NAME = 'Invalid player name, please enter full player\'s name.'
GOOD_MATCHUP = "they are looking at a good matchup and could easily surpass those projections this week."
NEUTRAL_MATCHUP = "they should probably perform as projected making them a dependable option this week."
BAD_MATCHUP = "they are looking at a tough matchup and might have a hard time hitting those projections this week."

def scrape(scraper):
    value_map = {}
    point_elements = scraper.find_all("td", class_="Ta-end Selected")
    name_elements = scraper.find_all("td")
    team_names = get_team_names(name_elements)
    point_values = get_point_values(point_elements)
    for i in range(len(team_names)):
        value_map[team_names[i]] = [i+1, point_values[i]]
    return value_map

def get_team_names(name_elements):
    team_names = []
    for td in name_elements:
        if td.find("div"):
            if td.find("div").find("a"):
                team_names.append(td.find("div").find("a").text.split(" vs")[0].lower()) 
    return team_names

def get_point_values(point_elements):
    point_val = []
    for td in point_elements:
        point_val.append(td.find("div").text)
    return point_val

team_against_rb = requests.get("https://football.fantasysports.yahoo.com/f1/pointsagainst?season=2023&pos=RB&mode=average&sort=PTS&sdir=1&pspid=782205867&activity=players_sort_click&pspid=782205867&activity=players_sort_click")
team_against_qb = requests.get("https://football.fantasysports.yahoo.com/f1/pointsagainst?season=2023&pos=QB&mode=average&sort=PTS&sdir=1&pspid=782205822&activity=players_sort_click&pspid=782205822&activity=players_sort_click")
team_against_wr = requests.get("https://football.fantasysports.yahoo.com/f1/pointsagainst?season=2023&pos=WR&mode=average")
team_against_te = requests.get("https://football.fantasysports.yahoo.com/f1/pointsagainst?season=2023&pos=TE&mode=average")

map_list = [scrape(bs(team_against_qb.content, "html.parser")), 
            scrape(bs(team_against_wr.content, "html.parser")), 
            scrape(bs(team_against_rb.content, "html.parser")),
            scrape(bs(team_against_te.content, "html.parser"))]

def get_team_info(team_name, position):
    if team_name not in map_list[0].keys():
        return "Invalid team name! Please input full NFL team name:"
    ranks = [map[team_name][0] for map in map_list]
    points = [map[team_name][1] for map in map_list]
    report = "the {} are rank {} for points allowed to {}s at {} points per game "
    match position:
        case "QB":
            return report.format(team_name.title(), ranks[0], position, points[0])
        case "WR":
            return report.format(team_name.title(), ranks[1], position, points[1])
        case "RB":
            return report.format(team_name.title(), ranks[2], position, points[2])
        case "TE":
            return report.format(team_name.title(), ranks[3], position, points[3])
        
def process_yards(yards):
    if ',' in yards:
        return yards[0] + yards[2:]
    return yards

def QB_report(player_name, position, team_name, opponent_report, rank, projections_dict):
    pass_yds = int(process_yards(projections_dict['Passing Yards']))/5
    pass_tds = int(projections_dict['Passing Touchdowns'])/5
    projected = (pass_yds * .04) + (pass_tds * 4)
    forecast = ""
    if rank < 11:
        forecast = GOOD_MATCHUP
    elif rank < 22:
        forecast = NEUTRAL_MATCHUP
    else:
        forecast = BAD_MATCHUP
    return f"{player_name}, a {position} for the {team_name} has averaged {pass_yds} passing yards and {pass_tds} passing touchdowns over the last 5 games projecting them for {round(projected,2)} fantasy points and since {opponent_report}{forecast}"

def receiver_report(player_name, position, team_name, opponent_report, rank, projections_dict):
    receptions = int(projections_dict['Receptions'])/5
    rec_yds = int(process_yards(projections_dict['Receiving Yards']))/5
    rec_tds = int(projections_dict['Receiving Touchdowns'])/5
    projected = (rec_yds * .1) + (rec_tds * 6) + receptions
    forecast = ""
    if rank < 11:
        forecast = GOOD_MATCHUP
    elif rank < 22:
        forecast = NEUTRAL_MATCHUP
    else:
        forecast = BAD_MATCHUP
    return f"{player_name}, a {position} for the {team_name} has averaged {receptions} receptions for {rec_yds} receiving yards with {rec_tds} receiving touchdowns over the last 5 games projecting them for {round(projected, 2)} fantasy points and since {opponent_report}{forecast}"

def RB_report(player_name, position, team_name, opponent_report, rank, projections_dict):
    rush_yds = int(process_yards(projections_dict['Rushing Yards']))/5
    rush_tds = int(projections_dict['Rushing Touchdowns'])/5
    rec_yds = int(process_yards(projections_dict['Receiving Yards']))/5
    receptions = int(projections_dict['Receptions'])/5
    projected = (rush_yds * .1) + (rush_tds * 6) + (rec_yds * .1) + receptions
    forecast = ""
    if rank < 11:
        forecast = GOOD_MATCHUP
    elif rank < 22:
        forecast = NEUTRAL_MATCHUP
    else:
        forecast = BAD_MATCHUP
    return f"{player_name}, a {position} for the {team_name} has averaged {rush_yds} rushing yards and {rush_tds} rushing touchdowns as well as {receptions} receptions for {rec_yds} receiving yards over the last 5 games projecting them for {round(projected,2)} fantasy points and since {opponent_report}{forecast}"

connection = sqlite3.connect('myDb.db')
cursor = connection.cursor()

def get_player_info(player_name):
    cursor.execute(f'select ESPN_id, position, team from players where name="{player_name}"')
    output = cursor.fetchall()
    if len(output) == 0:
        return INVALID_PLAYER_NAME
    team_name = output[0][2]
    position = output[0][1]
    ESPN_id = output[0][0]
    cursor.execute(f'select * from matchups where away="{team_name}" or home="{team_name}"')
    matchup = cursor.fetchall()
    opponent = matchup[0][1] if matchup[0][0] == team_name else matchup[0][0]
    team_report = get_team_info(opponent.lower(), position)
    rank = int(team_report.split('rank ')[1].split(' for')[0])
    projections = espn_data.get_projections(ESPN_id, position)
    match position:
        case "QB":
            return QB_report(player_name,position,team_name,team_report,rank,projections)
        case "WR":
            return receiver_report(player_name,position,team_name,team_report,rank,projections)
        case "TE":
            return receiver_report(player_name,position,team_name,team_report,rank,projections)
        case "RB":
            return RB_report(player_name,position,team_name,team_report,rank,projections)

connection.commit()