import requests
import json
import sqlite3

PLAYER_OVERVIEW = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{}/overview"
SKILL_LIST = ["QB",'RB', 'WR', 'TE']
QB_STATS = ["Completions","Passing Attempts","Completion Percentage","Passing Yards","Yards Per Pass Attempt","Passing Touchdowns","Interceptions","Longest Pass","Passer Rating"]
WR_STATS = ["Receptions","Receiving Targets","Receiving Yards","Yards Per Reception","Receiving Touchdowns","Long Reception","Receiving First Downs","Rushing Attempts","Rushing Yards","Yards Per Rush Attempt","Rushing Touchdowns","Long Rushing","Fumbles", "Fumbles Lost"]
TE_STATS = WR_STATS
RB_STATS = ["Rushing Attempts","Rushing Yards","Yards Per Rush Attempt","Rushing Touchdowns","Long Rushing","Receptions","Receiving Yards","Yards Per Reception","Receiving Touchdowns","Long Reception","Fumbles","Fumbles Lost"]

def get_skill_projections(espn_id, stat_labels):
    data = json.loads(requests.get(PLAYER_OVERVIEW.format(espn_id)).text)
    if len(data['statistics']) < 1 or len(data['statistics']['splits']) <= 2:
        return {}
    val_list = data['statistics']['splits'][2]['stats']
    projections = {}
    for idx, value in enumerate(stat_labels):
        projections[value] = val_list[idx]
    return projections

def get_projections(id, position):
    match position:
        case "WR":
            return get_skill_projections(id, WR_STATS)
        case "QB":
            return get_skill_projections(id, QB_STATS)
        case "TE":
            return get_skill_projections(id, TE_STATS)
        case "RB":
            return get_skill_projections(id, RB_STATS)