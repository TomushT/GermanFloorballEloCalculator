import numpy as np
from scipy.optimize import least_squares
import functions
import fitting
import json

# import data
leagues = functions.initialize_leagues(r"data_from_sm/v2_leagues_floorball_deutschland_hgf_buli.csv")
teams = functions.initialize_teams(r"data_from_sm/v2_teams_floorball_deutschland_hgf_buli.csv")
matches = functions.initialize_matches(r"data_from_sm/v2_matches_floorball_deutschland_hgf_buli.csv")

# Condition for league level
cond_level = None  # None: all, 1: 1.Buli, 2: 2.BuLi

inittype = 'initial'
initfile = r"results/dataset4/initial_elos.json"
with open(initfile, "r") as file:
    initial_elos = json.load(file)

initial_guess = np.array([60, 100])
print(initial_guess)
print("Optimizing k and home advantage")
optimized = least_squares(fitting.check_predictions_for_k, initial_guess, args=(matches, cond_level, teams, inittype,
                                                                                initial_elos, leagues),
                          verbose=2, ftol=1.e-6, xtol=1.e-6, gtol=1.e-6)
print("...done")

print()
print(f"Optimal k:{optimized.x[0]}, home advantage:{optimized.x[1]}")
print(f"Gradient: {optimized.grad}")
