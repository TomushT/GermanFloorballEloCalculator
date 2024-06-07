import pandas as pd
import numpy as np
import functions
import json
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# import data
pathtoresults = "results/dataset4/"
pathtodata = "data_from_sm/"

# parameters
kthresh = 7

teams = functions.initialize_teams(pathtodata+"v2_teams_floorball_deutschland_hgf_buli.csv")
with open(pathtoresults+"elovstime.json", "r") as file:
    elovstime = json.load(file)
with open(pathtoresults+"dates.json", "r") as file:
    dates = json.load(file)

fig, ax = plt.subplots(figsize=(14, 11))

teamids = teams['TeamID'].values

jet = plt.cm.jet
colors = jet(np.linspace(0, 1, len(elovstime)))
markers = ["o", "v", "^", "<", ">", "s", "P", "X", "D"]
between_seasons = ['2016-08-01', '2017-08-01', '2018-08-01', '2019-08-01', '2020-08-01', '2021-08-01', '2022-08-01', '2023-08-01', '2024-08-01',]

for i, teamid in enumerate(elovstime):
    teamname, dateids, elos = functions.get_elos_team(int(teamid), elovstime, teams)
    datesindiv = []
    elosindiv = []
    for idateid, dateid in enumerate(dateids):
        date = dates[dateid]
        elo = elos[idateid]
        datesindiv.append(date)
        elosindiv.append(elo)

    datesindiv2 = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in datesindiv]
    imarker = i % len(markers)
    ax.plot(datesindiv2[:kthresh], elosindiv[:kthresh], '-', marker=markers[imarker], color=colors[i], alpha = 0.2)
    ax.plot(datesindiv2[kthresh:], elosindiv[kthresh:], '-', marker=markers[imarker], label=teamname.values[0], color=colors[i])
    for bs in between_seasons:
        ax.axvline(dt.datetime.strptime(bs, '%Y-%m-%d').date(), color='k', linestyle='--', lw=1)

ax.set_xlabel("Datum")
ax.set_ylabel("Elo Punkte")

ax.set_ylim(350, 2700)

plt.title("Teams aus der 1. und 2. Bundesliga")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=120))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()
