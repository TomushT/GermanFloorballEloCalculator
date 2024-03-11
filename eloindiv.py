import functions
import json

pathtoresults = "results/dataset1/"
pathtodata = "clean_data/"

# import data
teams = functions.initialize_teams(pathtodata+"hgf_teamsmain.csv")
with open(pathtoresults+"elovstime.json", "r") as file:
    elovstime = json.load(file)
with open(pathtoresults+"dates.json", "r") as file:
    dates = json.load(file)

teamid = 97
teamname, dateids, elos = functions.get_elos_team(teamid, elovstime, teams)
print(f'{teamname}')
for idateid, dateid in enumerate(dateids):
    date = dates[dateid]
    elo = elos[idateid]
    if idateid > 0:
        elodif = elo-elos[idateid-1]
        print(f'{date}: {elo}, {elodif}')
    else:
        print(f'{date}: {elo}')
