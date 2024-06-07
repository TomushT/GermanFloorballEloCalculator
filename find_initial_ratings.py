import numpy as np
import json
from scipy.optimize import least_squares
import functions
import fitting

print('Optimizing initial ratings')

# import data
leagues = functions.initialize_leagues(r"data_from_sm/v2_leagues_floorball_deutschland_hgf_buli.csv")
teams = functions.initialize_teams(r"data_from_sm/v2_teams_floorball_deutschland_hgf_buli.csv")
matches = functions.initialize_matches(r"data_from_sm/v2_matches_floorball_deutschland_hgf_buli.csv")

# working directory
wdir = "results/dataset6/"
print(f"Working directory: {wdir}")

# Condition for league level
cond_level = 2  # None: all, 1: 1.Buli, 2: 2.BuLi
print(f"chosen league level: {cond_level}")

# Ordered list of TeamIDs
teamids = list(teams['TeamID'].drop_duplicates())
teamids.sort()

gamesplayed = {}

nmatches = 5

print("Finding initial guess...")
initial_guess = []
# bounds for least squares
lb = []
ub = []
# go through all teams
for it, teamid in enumerate(teamids):
    gamesplayed[teamid] = 0
    avgielo = 0
    occurrences = 0
    # go through all matches
    for ir, row in matches.iterrows():
        # get data
        forfait = row['forfait']
        if not forfait:
            league_id = row['league_id']
            team1 = row['home_team_name']
            team2 = row['guest_team_name']
            goals1 = row['home_goals']
            goals2 = row['guest_goals']
            # handle league
            level = int(functions.handle_league(league_id, leagues))
            # conditions
            if cond_level is None or level == cond_level:
                # handle teams
                t1id, t2id = functions.handle_teams(team1, team2, teams)
                if t1id == teamid or t2id == teamid:
                    occurrences += 1
                    if occurrences <= nmatches:
                        ielo = functions.initial_elo_from_level(level)
                        avgielo += ielo
                    else:
                        break
    if occurrences > 0:
        if occurrences < nmatches:
            avgielo /= occurrences
        else:
            avgielo /= nmatches
        initial_guess.append(avgielo)
        # specify bounds for least squares
        if avgielo < 1500:
            lbi = 500
            ubi = 1500
        else:
            lbi = 1500
            ubi = 2500
        lb.append(lbi)
        ub.append(ubi)
    else:
        del gamesplayed[teamid]

initial_guess = np.array(initial_guess)
lb = np.array(lb)
ub = np.array(ub)

print(f"Number of teams: {len(gamesplayed)}")
print("...done")
print()

print("Optimizing initial Elos")
initial_elos = least_squares(fitting.check_initial_rankings, initial_guess, args=(matches, gamesplayed, teams, leagues, cond_level), bounds=(lb, ub), verbose=2, ftol=1.e-2, xtol=1.e-2, gtol=1.e-2)
print("...done")

# Use only teams which really participated
teamids = list(gamesplayed.keys())
teamids.sort()

# write result to json
to_file = []
print("Team name, initial guess, initial Elo")
for it, teamid in enumerate(teamids):
    to_file.append([teamid, int(np.round(initial_elos.x[it]))])
    teamrow = teams[teams['TeamID'] == teamid]
    teamname = teamrow['MainName'].values
    print(f"{teamname}, {initial_guess[it]}, {int(np.round(initial_elos.x[it]))}")
with open(wdir+"initial_elos.json", "w") as file:
    json.dump(to_file, file)
