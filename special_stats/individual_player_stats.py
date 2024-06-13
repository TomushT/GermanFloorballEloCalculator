import pandas as pd
import datetime as dt

first_name = 'Tomáš'
last_name = 'Rauch'

def find_season_simple(league_id, leagues):
    league = leagues[leagues['id'] == league_id]
    name = league['name'].iloc[0]
    iseason = int(league['season'].iloc[0])
    season = f"{iseason+8}/{iseason+9}"
    return name, season

def get_player_info(first_name, last_name, leagues, players, print2terminal=True, export2csv=False):
    # Player
    playerlist = []
    playerstats = players[(players['first_name'] == first_name) &
                          (players['last_name'] == last_name)]
    games_tot = playerstats['games'].sum()
    goals_tot = playerstats['goals'].sum()
    ass_tot = playerstats['assists'].sum()
    penalty_tot = playerstats['penalty_2'].sum()*2 + playerstats['penalty_2and2'].sum()*4
    + playerstats['penalty_5'].sum()*5 + playerstats['penalty_10'].sum()*10
    + playerstats['penalty_ms_tech'].sum()*20 + playerstats['penalty_ms_full'].sum()*20
    + playerstats['penalty_ms1'].sum()*20 + playerstats['penalty_ms2'].sum()*20
    + playerstats['penalty_ms3'].sum()*20

    jenadict = {'Vorname': first_name, 'Nachname': last_name,
                'Saison': "Total",
                'Spiele': int(games_tot), 'Tore': int(goals_tot), 'Vorlagen': int(ass_tot),
                'Punkte': int(goals_tot)+int(ass_tot), 'Strafminuten': int(penalty_tot),
                'Tore pro Spiel': float(goals_tot)/games_tot,
                'Vorlagen pro Spiel': float(ass_tot)/games_tot,
                'Punkte pro Spiel': float(goals_tot+ass_tot)/games_tot,
                'Strafminuten pro Spiel': float(penalty_tot)/games_tot
                }

    for iir, playerrow in playerstats.iterrows():
        league_id = playerrow['league_id']
        league, season = find_season_simple(league_id,leagues)
        team = playerrow['team_name']
        games = playerrow['games']
        goals = playerrow['goals']
        assists = playerrow['assists']
        penalty = playerrow['penalty_2']*2 + playerrow['penalty_2and2']*4 + playerrow['penalty_5']*5
        + playerrow['penalty_10']*10 + playerrow['penalty_ms_tech']*20 + playerrow['penalty_ms_full']*20
        + playerrow['penalty_ms1']*20 + playerrow['penalty_ms2']*20 + playerrow['penalty_ms3']*20
        datadict = {'Vorname': first_name, 'Nachname': last_name,
                    'Liga': league, 'Saison': season, 'Team': team, 'Spiele': int(games),
                    'Tore': int(goals), 'Vorlagen': int(assists),
                    'Punkte': int(goals)+int(assists), 'Strafminuten': int(penalty),
                    'Tore pro Spiel': float(goals)/games,
                    'Vorlagen pro Spiel': float(assists)/games,
                    'Punkte pro Spiel': float(goals+assists)/games,
                    'Strafminuten pro Spiel': float(penalty)/games}
        playerlist.append(datadict)

    playerlist.append(jenadict)

    playerdf = pd.DataFrame(playerlist)
    playerdf_sorted = playerdf.sort_values(['Nachname', 'Vorname', 'Saison'], ascending=[True, True, True])

    if export2csv:
        playerdf_sorted.to_csv(f'stats_{first_name}_{last_name}.csv')
    if print2terminal:
        print(playerdf_sorted)





leagues = pd.read_pickle("leagues.pkl")
players = pd.read_pickle("players.pkl")

get_player_info(first_name, last_name, leagues, players, print2terminal=True, export2csv=False)