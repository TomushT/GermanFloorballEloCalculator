# GermanFloorballEloCalculator
Calculation of Floorball Elo values for all German teams (currently only Herren Großfeld 1. Bundesliga and 2. Bundesliga). Historical data from https://saisonmanager.de/
Support with data extraction by Joshua Reibert (https://github.com/joshuarrrrr).

- *calculate_elo.py* - calculates Elo values of all teams
- *eloindiv.py* - prints Elo values for an individual team (assuming Elo values were already calculated with *calculate_elo.py*)
- *find_initial_ratings.py* - estimates initial Elo ratings by minimizing the squared differences between the estimated and observed win probabilities, see https://opisthokonta.net/?p=1387 and https://opisthokonta.net/?p=1412
- *find_k_homeadv.py* - calculates the values of the cost function (sum of the squared differences between the estimated and observed win probabilities) for varying values of the k parameter and the home advantage, looking for the minimum of the cost function
- *find_k_homeadv_leastsquares.py* - minimizes the cost function to find optimal values of k and the home advantage with least squares minimization (scipy). Does not work properly in the moment. It finds the optimal home advantage, but does not minimize `k` (zero gradient). Reason is unknown.
- *fitting.py* - includes functions used to obtain optimal parameters (initial Elo values, k, and home advantage)
- *functions.py* - includes basic functions used by other scripts
- *plot_elo_1buli.py* - plots Elo values for teams which participated in 1. BuLi only
- *plot_elo_2buli.py* - plots Elo values for teams which participated in 2. BuLi only
- *update_hgf_teamsmain.ipynb* - Jupyter notebook for updating the databases in case some teams have to be merged or separated. First update clean_data/hgf_teams.csv manually and then run *update_hgf_teamsmain.ipynb* to update everything else
- *data_loading/load_matches_josh.ipynb* - Jupyter notebook for loading the data from the API of https://saisonmanager.de/
- *data_from_sm* - includes the data extracted from the https://saisonmanager.de/
- *results* - includes the results, see readme.md in the directory
- *special_stats* - notebooks etc. to get individual player statistics, see readme.md in the directory
- *old_version* - includes old version of the code, which used https://archiv.saisonmanager.de/ and was only valid until season 21/22

# Formalism
- Calculation of the win probabilities `we1` and `we2` from `elo1` and `elo2`, assuming home advantage `h`: 
```python
we1 = 1.0/(10**(-(elo1-elo2+h)/400)+1)
we2 = 1.0/(10**(-(elo2-elo1-h)/400)+1)
```
- New Elo values for the observed result `w1` and `w2`:
```python
nelo1 = elo1 + gf*k1*(w1-we1)
nelo2 = elo2 + gf*k2*(w2-we2)
```
- *w = 1.0* for a win, *w = 0.5* for a draw, *w = 0.0* for a loss.
- `gf = max(np.log(dg),1.0)` is the goal factor, accounting for the goal difference `dg`
- `k1` and `k2` are the k parameters. Both are equal to *k* if each team played more than `ktresh` matches (default: 7). If team 1 played `<=ktresh` matches, `k1=2*k` and `k2=0.5*k`. If both teams played `<=ktresh` matches, `k1=k2=2*k`. This accounts for the fact that a reasonable Elo value is obtained only after a certain number of matches played.

# Notes on results so far
- Results for 1. BuLi and 2. BuLi together, as well as for both leagues individually were obtained, both by starting from set initial Elo values (2000 for 1. BuLi and 1000 for 2. BuLi) as well as from optimized initial values. All results seem to be quite reasonable.
- Optimal model parameters (using optimized initial Elo values) are `k=60` and `h=70` for both 1. BuLi and 2. BuLi together. Thus, the k-parameter is very large (typically between 15 and 20 for other sports). That might indicate large fluctuations of quality differences of the teams or not very good initial Elo values.
- The home advantage is comparable to other sports (typically around 100 or slightly below).
