import numpy as np
import functions
import fitting
import json

# import data
leagues = functions.initialize_leagues(r"data_from_sm/v2_leagues_floorball_deutschland_hgf_buli.csv")
teams = functions.initialize_teams(r"data_from_sm/v2_teams_floorball_deutschland_hgf_buli.csv")
matches = functions.initialize_matches(r"data_from_sm/v2_matches_floorball_deutschland_hgf_buli.csv")

# working directory
wdir = "results/dataset6/"
print(f"Working directory: {wdir}")

# Condition for league level
cond_level = 2  # None: all, 1: 1.Buli, 2: 2.BuLi

# Type of Elo initialization
#inittype = 'firstmatch'
#inittype = 'constant'
inittype = 'initial'
initfile = wdir+r"initial_elos.json"
with open(initfile, "r") as file:
    initial_elos = json.load(file)

results = []

print("Optimizing k and home advantage")
for k in range(10, 105, 5):
    for h in range(-30, 160, 10):
        print(f"k={k}, h={h}")
        cost = fitting.cost_for_k_h(k, h, matches, teams, cond_level, inittype, initial_elos, leagues)
        print(f"{k}, {h}, {cost}")
        results.append([k, h, cost])

print("...done")

with open(wdir+"cost_k_h.json", "w") as file:
    json.dump(results, file)

imin = -1
minimum = 99999999
for i in range(len(results)):
    if results[i][2] < minimum:
        minimum = results[i][2]
        imin = i
print("Minimum:")
print(results[imin])

