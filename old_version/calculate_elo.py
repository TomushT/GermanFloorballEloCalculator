import functions
import json

# import data
leagues = functions.initialize_leagues(r"clean_data/hgf_leagues.csv")
teams = functions.initialize_teams(r"clean_data/hgf_teamsmain.csv")
matches = functions.initialize_matches(r"clean_data/hgf_matches_ordered.csv")

inittype = 'initial'
initfile = r"results/initial_data/initial_elos.json"
with open(initfile, "r") as file:
    initial_elos = json.load(file)

# initialize dictionary with all Elos
elovstime = {}
dates = []

# go through all matches
for ir, row in matches.iterrows():
    # get data
    date = row['Date']
    league = row['League']
    t1id = int(row['T1ID'])
    t2id = int(row['T2ID'])
    gs1 = row['GT1']
    gs2 = row['GT2']
    # handle date
    idate, dates = functions.handle_date(dates, date)
    # handle league
    level = functions.handle_league(league, leagues)
    # handle teams in elovstime
    gp1, gp2, elo1, elo2, elovstime = functions.handle_teams_in_elovstime(t1id, t2id, elovstime, inittype, initial_elos, level)
    # calculate new elos
    nelo1, nelo2 = functions.calculate_elos(elo1, elo2, gp1, gp2, gs1, gs2)
    # append new data
    elovstime[t1id]['elos'].append(nelo1)
    elovstime[t1id]['dateID'].append(idate)
    elovstime[t2id]['elos'].append(nelo2)
    elovstime[t2id]['dateID'].append(idate)

# write result to json
with open("elovstime.json", "w") as file:
    json.dump(elovstime, file)
with open("dates.json", "w") as file:
    json.dump(dates, file)
