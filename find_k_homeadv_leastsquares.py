import numpy as np
from scipy.optimize import least_squares
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

initial_guess = np.array([20,100])
print(initial_guess)
print("Optimizing k and home advatage")
optimized = least_squares(fitting.check_predictions_for_k,initial_guess,args=(matches,inittype,initial_elos,leagues),verbose=2,ftol=1.e-6,xtol=1.e-6,gtol=1.e-6)
print("...done")

print()
print(f"Optimal k:{optimized.x[0]}, home advantage:{optimized.x[1]}")
