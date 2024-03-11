import numpy as np
import functions
import fitting
import json

# import data
leagues = functions.initialize_leagues(r"clean_data/hgf_leagues.csv")
matches = functions.initialize_matches(r"clean_data/hgf_matches_ordered.csv")

inittype = 'initial'
initfile = r"results/initial_data/initial_elos.json"
with open(initfile, "r") as file:
    initial_elos = json.load(file)

results = []

print("Optimizing k and home advantage")
for k in range(10, 102, 2):
    for h in range(-30, 50, 10):
        print(f"k={k}, h={h}")
        cost = fitting.cost_for_k_h(k, h, matches, inittype, initial_elos, leagues)
        print(f"{k}, {h}, {cost}")
        results.append([k, h, cost])

print("...done")

with open("results/initial_data/cost_k_h.json", "w") as file:
    json.dump(results, file)

imin = -1
min = 99999999
for i in range(len(results)):
    if results[i][2]<min:
        min = results[i][2]
        imin = i
print("Minimum:")
print(results[imin])

