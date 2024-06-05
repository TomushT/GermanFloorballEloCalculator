import pandas as pd
import numpy as np
import functions
import json
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# import data
pathtoresults = "results/dataset1/"
pathtodata = "data_from_sm/"

teams = functions.initialize_teams(pathtodata+"v2_teams_floorball_deutschland_hgf_buli.csv")
with open(pathtoresults+"elovstime.json", "r") as file:
    elovstime = json.load(file)
with open(pathtoresults+"dates.json", "r") as file:
    dates = json.load(file)

fig, ax = plt.subplots(figsize=(12, 6))

teamids = teams['TeamID'].values

jet = plt.cm.jet
colors = jet(np.linspace(0, 1, len(teamids)))

for i, teamid in enumerate(teamids):
    teamname, dateids, elos = functions.get_elos_team(teamid, elovstime, teams)
    datesindiv = []
    elosindiv = []
    for idateid, dateid in enumerate(dateids):
        date = dates[dateid]
        elo = elos[idateid]
        datesindiv.append(date)
        elosindiv.append(elo)

    datesindiv2 = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in datesindiv]
    ax.plot(datesindiv2[:10], elosindiv[:10], 'o-', color=colors[i], alpha = 0.2)
    ax.plot(datesindiv2[10:], elosindiv[10:], 'o-', label=teamname.values[0], color=colors[i])

ax.set_xlabel("Datum")
ax.set_ylabel("Elo Punkte")

ax.set_ylim(300, 3000)

plt.title("Teams aus der 1. und 2. Bundesliga")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=150))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()
