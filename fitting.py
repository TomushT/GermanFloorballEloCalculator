import numpy as np
import functions


def check_initial_rankings(x, matches, gamesplayed, teams, leagues, cond_level, nmatches=7):
    r"""
    Calculates the values of the residuals for given initial Elo values. To be used by scipy.optimize.least_squares
    :param x: initial rankings of teams sorted by TeamID
    :param nmatches: number of matches considered for the fit
    :param matches: DataFrame with matches
    :param gamesplayed: Dictionary of teams with number of matches played
    :param teams: DataFrame with teams
    :param leagues: DataFrame with leagues
    :param cond_level: Condition for choice of level
    :return: residuals...array of the residuals
    """

    # Sorted list of TeamIDs
    teamids = list(gamesplayed.keys())
    teamids.sort()

    # Initialize residuals
    residuals = []

    # go through all matches
    for ir, row in matches.iterrows():
        # get data
        forfait = row['forfait']
        if not forfait:
            league_id = row['league_id']
            team1 = row['home_team_name']
            team2 = row['guest_team_name']
            gs1 = row['home_goals']
            gs2 = row['guest_goals']
            # handle league
            level = int(functions.handle_league(league_id, leagues))
            # conditions
            if cond_level is None or level == cond_level:
                # handle teams
                t1id, t2id = functions.handle_teams(team1, team2, teams)

                # update gamesplayed
                gamesplayed[t1id] += 1
                gamesplayed[t2id] += 1

                b1 = gamesplayed[t1id] <= nmatches
                b2 = gamesplayed[t2id] <= nmatches

                if b1 or b2:
                    # get w1, w2
                    w1, w2 = functions.get_result(gs1, gs2)
                    # indices in the list x
                    ix1 = teamids.index(t1id)
                    ix2 = teamids.index(t2id)
                    # Elos
                    elo1 = x[ix1]
                    elo2 = x[ix2]
                    # Get win probabilities
                    we1, we2 = functions.win_probability(elo1, elo2)

                    # Append residuals
                    if b1:
                        residuals.append(w1-we1)
                    if b2:
                        residuals.append(w2-we2)

    # reset gamesplayed
    for iid in teamids:
        gamesplayed[iid] = 0
    return np.array(residuals)


def check_predictions_for_k(x, matches, inittype='initial', initial_elos=None, leagues=None):
    r"""
    Calculates the values of the residuals for given k and h. To be used by scipy.optimize.least_squares
    :param x: Parameters to be optimized. x[0]...k, x[1]...home advantage
    :param matches: DataFrame with leagues
    :param inittype: Type of setting the initial Elos. 'initial'...from optimized initial Elos
                                                   'firstmatch'...from the level of the league of the first match
    :param initial_elos: Initial Elos
    :param leagues: DataFrame with leagues
    :return: residuals...array with the residuals
    """
    residuals = []
    k = x[0]
    h = x[1]
    level = None
    # initialize dictionary with all Elos
    elovstime = {}

    # go through all matches
    for ir, row in matches.iterrows():
        # get data
        if inittype == 'firstmatch':
            league = row['League']
            # handle league
            level = functions.handle_league(league, leagues)
        t1id = int(row['T1ID'])
        t2id = int(row['T2ID'])
        gs1 = row['GT1']
        gs2 = row['GT2']
        # handle teams in elovstime
        gp1, gp2, elo1, elo2, elovstime = functions.handle_teams_in_elovstime(t1id, t2id, elovstime, inittype,
                                                                              initial_elos=initial_elos, level=level)
        # calculate new elos
        nelo1, nelo2 = functions.calculate_elos(elo1, elo2, gp1, gp2, gs1, gs2, k=k, h=h)
        # append new data
        elovstime[t1id]['elos'].append(nelo1)
        elovstime[t2id]['elos'].append(nelo2)

        # get w1, w2
        w1, w2 = functions.get_result(gs1, gs2)
        # get win probabilities
        we1, we2 = functions.win_probability(elo1, elo2, h=h)
        # Append residuals
        residuals.append(w1 - we1)
        residuals.append(w2 - we2)

    return np.array(residuals)


def cost_for_k_h(k, h, matches, teams, cond_level, inittype='initial', initial_elos=None, leagues=None):
    r"""
    Calculates the value of the cost function for given k and h
    :param cond_level: Condition for level
    :param teams:  DataFrame with teams
    :param k: k-parameter
    :param h: home advantage
    :param matches: DataFrame with matches
    :param inittype: Type of setting the initial Elos. 'initial'...from optimized initial Elos
                                                       'firstmatch'...from the level of the league of the first match
    :param initial_elos: Initial Elos
    :param leagues: DataFrame with leagues
    :return: cost...value of the cost function
    """
    residuals = []
    level = None
    # initialize dictionary with all Elos
    elovstime = {}

    # go through all matches
    for ir, row in matches.iterrows():
        # get data
        forfait = row['forfait']
        if not forfait:
            league_id = row['league_id']
            team1 = row['home_team_name']
            team2 = row['guest_team_name']
            gs1 = row['home_goals']
            gs2 = row['guest_goals']
            # handle league
            level = int(functions.handle_league(league_id, leagues))
            # conditions
            if cond_level is None or level == cond_level:
                # handle teams
                t1id, t2id = functions.handle_teams(team1, team2, teams)
                # handle teams in elovstime
                gp1, gp2, elo1, elo2, elovstime = functions.handle_teams_in_elovstime(t1id, t2id, elovstime, inittype,
                                                                                      initial_elos=initial_elos, level=level)
                # calculate new elos
                nelo1, nelo2 = functions.calculate_elos(elo1, elo2, gp1, gp2, gs1, gs2, k=k, h=h)
                # append new data
                elovstime[t1id]['elos'].append(nelo1)
                elovstime[t2id]['elos'].append(nelo2)

                # get w1, w2
                w1, w2 = functions.get_result(gs1, gs2)
                # get win probabilities
                we1, we2 = functions.win_probability(elo1, elo2, h=h)
                # Append residuals
                residuals.append(w1 - we1)
                residuals.append(w2 - we2)

    residuals = np.array(residuals)
    cost = 0.5*np.dot(residuals, residuals)

    return cost
