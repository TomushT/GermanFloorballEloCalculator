import numpy as np
from scipy.optimize import least_squares
import functions
import fitting

# import data
leagues = functions.initialize_leagues(r"clean_data/hgf_leagues.csv")
teams = functions.initialize_teams(r"clean_data/hgf_teamsmain.csv")
matches = functions.initialize_matches(r"clean_data/hgf_matches_ordered.csv")

# Ordered list of TeamIDs
teamids = list(teams['TeamID'])
teamids.sort()

gamesplayed = {}

nmatches = 5

print("Finding initial guess...")
initial_guess = []
# go through all teams
for it,teamid in enumerate(teamids):
    gamesplayed[teamid] = 0
    avgielo = 0
    occurrences = 0
    # go through all matches
    for ir,row in matches.iterrows():
        # get data
        league = row['League']
        t1id = int(row['T1ID'])
        t2id = int(row['T2ID'])
        if t1id == teamid or t2id == teamid:
            # handle league
            level = functions.handle_league(league,leagues)
            occurrences +=1
            if occurrences <= nmatches:
                ielo = functions.initial_elo_from_level(level)
                avgielo += ielo
            else:
                break
    if occurrences < nmatches:
        avgielo /= occurrences
    else:
        avgielo /= nmatches
    initial_guess.append(avgielo)

initial_guess = np.array(initial_guess)


print("...done")
print()

print("Optimizing initial Elos")
initial_elos = least_squares(fitting.check_initial_rankings,initial_guess,args=(matches,gamesplayed),bounds=(500,2500),verbose=2,ftol=1.e-3,xtol=1.e-3,gtol=1.e-3)
print("...done")

# write result to json
to_file = []
for i,teamid in enumerate(teamids):
    to_file.append([teamid,int(np.round(initial_elos.x[i]))])
import json
with open("results/initial_data/initial_elos.json", "w") as file:
    json.dump(to_file, file)

print("Team name, initial guess, initial Elo")
for it, teamid in enumerate(teamids):
    teamrow = teams[teams['TeamID'] == teamid]
    teamname = teamrow['MainName'].values
    print(f"{teamname}, {initial_guess[it]}, {int(np.round(initial_elos.x[it]))}")
