import functions
import json

# import data
leagues = functions.initialize_leagues(r"data_from_sm/v2_leagues_floorball_deutschland_hgf_buli.csv")
teams = functions.initialize_teams(r"data_from_sm/v2_teams_floorball_deutschland_hgf_buli.csv")
matches = functions.initialize_matches(r"data_from_sm/v2_matches_floorball_deutschland_hgf_buli.csv")

# working directory
wdir = "results/dataset6/"
print(f"Working directory: {wdir}")

# Type of Elo initialization
#inittype = 'firstmatch'
#inittype = 'constant'
inittype = 'initial'
initfile = wdir+r"initial_elos.json"
with open(initfile, "r") as file:
    initial_elos = json.load(file)

# Condition for league level
cond_level = 2  # None: all, 1: 1.Buli, 2: 2.BuLi

# initialize dictionary with all Elos
elovstime = {}
dates = []

# go through all matches
for ir, row in matches.iterrows():
    # get data
    forfait = row['forfait']
    if not forfait:
        date = row['date']
        league_id = row['league_id']
        team1 = row['home_team_name']
        team2 = row['guest_team_name']
        goals1 = row['home_goals']
        goals2 = row['guest_goals']
        # handle league
        level = int(functions.handle_league(league_id, leagues))
        # conditions
        if cond_level is None or level==cond_level:
            # handle date
            idate, dates = functions.handle_date(dates, date)
            # handle teams
            t1id, t2id = functions.handle_teams(team1, team2, teams)
            # handle teams in elovstime
            gp1, gp2, elo1, elo2, elovstime = functions.handle_teams_in_elovstime(t1id, t2id, elovstime, inittype, initial_elos=initial_elos, level=level)
            # calculate new elos
            nelo1, nelo2 = functions.calculate_elos(elo1, elo2, gp1, gp2, goals1, goals2, k=50, h=80)
            # append new data
            elovstime[t1id]['elos'].append(nelo1)
            elovstime[t1id]['dateID'].append(idate)
            elovstime[t2id]['elos'].append(nelo2)
            elovstime[t2id]['dateID'].append(idate)

# write result to json
with open(wdir+"elovstime.json", "w") as file:
    json.dump(elovstime, file)
with open(wdir+"dates.json", "w") as file:
    json.dump(dates, file)
