# Results obtained with different initial conditions
Important input from the following websites was used:

https://opisthokonta.net/?p=1387

https://opisthokonta.net/?p=1412

## initial_data1
- *initial_elos.json* - Includes initial Elo values obtained by minimizing the differences between the estimated and observed win probabilities using the least squares fit (from scipy). For each Team, the first 7 matches were considered (or as many as the Team played) and the Elos were not updated. The initial guess was the average of the initial Elos from the levels of the league the team played in (1 - 1. Bundesliga, 2000; 2 - 2. Bundesliga / Pokal, 1500; 3 - Regionalliga / Verbandsliga, 1000).
- *cost_k_h.json* - Includes the values of the cost function (sum of the squared differences between the estimated and observed win probabilities) for different values of the k parameter and the home advantage. The optimal value is k=62, h=10.

## dataset1
- *elovstime.json* - Elo values for all teams.
- *dates.json* - All dates at which matches were played.
- *elo_1buli_2122.pdf* - Plot of Elo values for teams which participated in 1. BuLi in the season 21/22 (but might have played in another leagues before)
- *elo_2buli_2122.pdf* - Plot of Elo values for teams which participated in 2. BuLi in the season 21/22 (but might have played in another leagues before)
