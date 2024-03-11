import numpy as np
import pandas as pd

def get_result(gs1,gs2):
    r"""
    Get the result of the match based on the goals scored.

    :param gs1: Goals scored by Team 1
    :param gs2: Goals scored by Team 2
    :return: w1...Points awarded to Team 1
             w2...Points awarded to Team 2
    """
    if gs1<gs2:
        w1=0.0
        w2=1.0
    elif gs1>gs2:
        w1=1.0
        w2=0.0
    elif gs1==gs2:
        w1=0.5
        w2=0.5
    return w1, w2

def win_probability(elo1,elo2,h=10):
    r"""
    Calculates the win probabilities for a given pair of Elos.

    :param elo1: Elo of Team 1 (home).
    :param elo2: Elo of Team 2 (away).
    :param h:  Home advantage (def.: 100).
    :return: we1...Win probability of Team 1
             we2...Win probability of Team 2
    """

    # win probability
    we1 = 1.0/(10**(-(elo1-elo2+h)/400)+1)
    we2 = 1.0/(10**(-(elo2-elo1)/400)+1)

    return we1, we2

def calculate_elos(elo1,elo2,gp1,gp2,gs1,gs2,k=62,h=10,ktresh=10):
    r"""
    Calculates the new Elos.

    :param elo1: Elo of Team 1 (home).
    :param elo2: Elo of Team 2 (away).
    :param gp1: Games played by Team 1.
    :param gp2: Games played by Team 2.
    :param gs1: Goals scored by Team 1.
    :param gs2: Goals scored by Team 2.
    :param h:  Home advantage (def.: 100).
    :param ktresh: Treshold for the K parameter (def.: 7).
    :return: nelo1...new Elo of Team 1
             nelo2...new Elo of Team 2
    """

    # goal difference
    dg = np.abs(gs1-gs2)
    # goal factor
    gf = max(np.log(dg),1.0)
    # K factor
    if gp1>ktresh and gp2>ktresh:
        k1 = k
        k2 = k
    elif gp1<=ktresh and gp2>ktresh:
        k1 = 5*k
        k2 = 0.5*k
    elif gp1>ktresh and gp2<=ktresh:
        k1 = 0.5*k
        k2 = 5*k
    elif gp1<=ktresh and gp2<=ktresh:
        k1 = 5*k
        k2 = 5*k
    # points from actual match
    w1, w2 = get_result(gs1, gs2)
    # win probability
    we1, we2 = win_probability(elo1, elo2, h)
    # new Elos
    nelo1 = elo1 + gf*k1*(w1-we1)
    nelo2 = elo2 + gf*k2*(w2-we2)
    nelo1 = int(np.round(nelo1))
    nelo2 = int(np.round(nelo2))

    return nelo1, nelo2

def initialize_leagues(leaguesfile):
    r"""

    :param leaguesfile: File including the database with leagues
    :return: pandas DataFrame with leagues
    """
    leagues = pd.read_csv(leaguesfile)
    return leagues

def initialize_teams(teamsfile):
    r"""

    :param teamsfile: File including the database with teams
    :return: pandas DataFrame with teams
    """
    teams = pd.read_csv(teamsfile)
    return teams

def initialize_matches(matchesfile):
    r"""

    :param matchesfile: File including the database with matches
    :return: pandas DataFrame with matches
    """
    matches = pd.read_csv(matchesfile)
    return matches

def handle_date(dates,date):
    r"""
    Appends date to the dates list.

    :param dates: list with dates
    :param date: date to be added
    :return: idate...index of the added date,
             dates...list with dates
    """
    if date not in dates:
        dates.append(date)
    idate = dates.index(date)
    return idate, dates

def handle_league(league,leagues):
    r"""
    Finds the level of league.

    :param league: Investigated league.
    :param leagues: DataFrame of leagues.
    :return: level
    """
    leaguerow = leagues[leagues['LeagueName']==league]
    level = leaguerow['Level'].values
    return level

def initial_elo_from_level(level):
    r"""
    Assigns initial Elo from level of the league of the match

    :param level: Level of the league
    :return: elo...initial Elo
    """
    if level == 1:
        elo = 2000
    elif level == 2:
        elo = 1500
    elif level == 3:
        elo = 1000
    return elo

def handle_teams_in_elovstime(t1id, t2id, elovstime, inittype = 'initial', initial_elos = None, level = None):
    r"""
    Find Elos (current or initial) for both teams participating in the current match.

    :param t1id: Team1 ID
    :param t2id: Team2 ID
    :param elovstime: Dictionary with Elo for all teams
    :param inittype: Type of setting the initial Elos. 'initial'...from optimized initial Elos
                                                   'firstmatch'...from the level of the league of the first match
    :param initial_elos: List with TeamIDs and initial Elos.
    :param level: Level of the league of the current match.
    :return:gp1...Games played by Team1,
            gp2...Games played by Team2,
            elo1...Elo of Team 1,
            elo2...Elo of Team 2,
            elovstime...Dictionary with Elos for all teams
    """
    knownteams = list(elovstime.keys())
    if t1id not in knownteams:
        elovstime[t1id]={'dateID':[],'elos':[]}
        gp1 = 0
        if inittype == 'firstmatch':
            elo1 = initial_elo_from_level(level)
        elif inittype == 'initial':
            for pair in initial_elos:
                if pair[0] == t1id:
                    elo1 = pair[1]
                    break
    else:
        gp1 = len(elovstime[t1id]['elos'])
        elo1 = elovstime[t1id]['elos'][-1]

    if t2id not in knownteams:
        elovstime[t2id]={'dateID':[],'elos':[]}
        gp2 = 0
        if inittype == 'firstmatch':
            elo2 = initial_elo_from_level(level)
        elif inittype == 'initial':
            for pair in initial_elos:
                if pair[0] == t2id:
                    elo2 = pair[1]
                    break
    else:
        gp2 = len(elovstime[t2id]['elos'])
        elo2 = elovstime[t2id]['elos'][-1]

    return gp1, gp2, elo1, elo2, elovstime

def get_elos_team(teamid,elovstime,teams):
    r"""
    Find dateIDs and Elos of a given Team.

    :param teamid: ID of the Team of interest.
    :param elovstime: Dictionary with Elo for all teams
    :param teams: DataFrame with Team names and IDs
    :return: teamname...Name of Team of interest
             dateIDs...IDs of dates at which the Team was active
             elos...Elos of the Team of interest.
    """
    teamrow = teams[teams['TeamID'] == teamid]
    teamname = teamrow['MainName']
    elos = elovstime[str(teamid)]['elos']
    dateIDs = elovstime[str(teamid)]['dateID']
    return teamname, dateIDs, elos
