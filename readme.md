# GermanFloorballEloCalculator
Calculation of Floorball Elo values for all German teams (currently only Herren Großfeld). Historical data from https://archiv.saisonmanager.de/

- *calculate_elo.py* - calculates Elo values of all teams
- *eloindiv.py* - prints Elo values for an individual team (assuming Elo values were already calculated with *calculate_elo.py*)
- *find_initial_ratings.py* - estimates initial Elo ratings by minimizing the squared differences between the estimated and observed win probabilities, see https://opisthokonta.net/?p=1387 and https://opisthokonta.net/?p=1412
- *find_k_homeadv.py* - calculates the values of the cost function (sum of the squared differences between the estimated and observed win probabilities) for varying values of the k parameter and the home advantage, looking for the minimum
- *find_k_homeadv_leastsquares.py* - minimizes the cost function to find optimal values of k and the home advantage with least squares minimization (scipy). Does not give any good results in the moment.
- *fitting.py* - includes functions used to obtain optimal parameters (initial Elo values, k, and home advantage)
- *functions.py* - includes basic functions used by other scripts
- *plot_elo_1buli.py* - plots Elo values for teams which participated in 1. BuLi in 21/22
- *plot_elo_2buli.py* - plots Elo values for teams which participated in 2. BuLi in 21/22

# Formalism
- Calculation of the win probabilities `we1` and `we2` from `elo1` and `elo2`, assuming home advantage `h`: 
```python
we1 = 1.0/(10**(-(elo1-elo2+h)/400)+1)
we2 = 1.0/(10**(-(elo2-elo1)/400)+1)
```
- New Elo values for the observed result `w1` and `w2`:
```python
nelo1 = elo1 + gf*k1*(w1-we1)
nelo2 = elo2 + gf*k2*(w2-we2)
```
- *w = 1.0* for a win, *w = 0.5* for a draw, *w = 0.0* for a loss.
- `gf = max(np.log(dg),1.0)` is the goal factor, accounting for the goal difference `dg`
- `k1` and `k2` are the k parameters. Both are equal to *k* if each team played more than `ktresh` matches (default: 10). If team 1 played `<=ktresh` matches, `k1=5*k` and `k2=0.5*k`. If both teams played `<=ktresh` matches, `k1=k2=5*k`. This accounts for the fact that a reasonable Elo value is obtained only after a certain number of matches played.

# Notes on results so far
- Using optimized initial Elo values (which make often sense, but are unreasonable in some cases), quite reasonable rankings are obtained after initial 10 matches. Teams from the 1. BuLi are on average ranked above Teams from the 2. BuLi. Quantitative analysis is to be done...
- Optimal model parameters (using optimized initial Elo values) are `k=62` and `h=10`. Thus, the k-parameter is very large (typically between 15 and 20 for other sports). There seems to be almost no home advantage in German Floorball!