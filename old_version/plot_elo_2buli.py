import pandas as pd
import numpy as np
import functions
import json
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

# import data
teams = functions.initialize_teams(r"clean_data/hgf_teamsmain.csv")
with open("results/dataset1/elovstime.json", "r") as file:
    elovstime = json.load(file)
with open("results/dataset1/dates.json", "r") as file:
    dates = json.load(file)
chosenteams = pd.read_csv("clean_data/hgf_teams_2BuLi_2122.csv")

fig, ax = plt.subplots(figsize=(12, 6))

teamids = chosenteams['TeamID'].values

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

#ax.set_ylim(1400,2900)

plt.title("Teams aus der 2. Bundesliga 21/22")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=150))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()
