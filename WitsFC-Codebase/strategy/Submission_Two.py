import numpy as np


def distance(one, two):
    return np.sqrt((one[0] - two[0]) ** 2 + (one[1] - two[1]) ** 2)


# given a list of players and a target distance, find the closest
def find_closest_to_target(players, target):

    closest_player = None
    min_distance = np.inf

    for player, point in enumerate(players):
        d = distance(point, target)
        if d < min_distance:
            closest_player = player
            min_distance = d
    return min_distance, closest_player


def find_closest_players_to_target(players, target):

    closest_players = []
    for player, point in enumerate(players):
        d = distance(point, target)
        closest_players.append((d, player))
    closest_players = sorted(closest_players, key=lambda data: data[0])
    return closest_players


# given you and a list of players, find the closest one
def find_closest_player(player_u, players, target):

    closest_player = None
    min_distance = np.inf

    for player, point in enumerate(players):
        distance = np.sqrt((point[0] - target[0]) ** 2 + (point[1] - target[1]) ** 2)
        if distance < min_distance:
            closest_player = player
            min_distance = distance
    return min_distance, closest_player


# find the single player closer to the target then you without opponents around them
def find_closest_player_forward_without_opponent_at_least_distance_closer_to_goal(
    player_u,
    players,
    opponents,
    target,
    max_kick_distance,
    max_opp_distance,
    distance_forward,
):
    # gets the coords of the current player
    cur_player = players[player_u]

    # find players that are closer then you to goal
    your_distance_to_target = distance(cur_player, target)
    players_closer_to_target = []

    for number, player in enumerate(players):
        d = distance(cur_player, player)
        # find people closer to the target then you
        # they should also be sufficiently closer, at least some x amount
        if d < your_distance_to_target - distance_forward:
            players_closer_to_target.append((number, player))

    if len(players_closer_to_target) == 0:
        # if nobody is closer then return yourself
        return your_distance_to_target, player_u

    # now we have a list of all players closer to the target
    # from that, find the player that is closest to you that ISN'T YOU
    closest_players = []
    # furthest kicking distance
    kick_distance = max_kick_distance

    # gets a list of players that are within kick distance from you
    for player_info in players_closer_to_target:
        number, player = player_info

        d = distance(cur_player, player)
        if d < kick_distance and number != player_u:
            closest_players.append((d, number, player))

    # if you're the closest just return yourself and your number
    if len(closest_players) == 0:
        return your_distance_to_target, player_u

    # if there are players within kick distance from you
    # check which one of them are have players around them
    viable_players = []
    max_opponent_distance = max_opp_distance
    for d, number, player in closest_players:
        # if the closest opponent to you is larger then max_allowed_distance then add them as viable
        opp_distance, _ = find_closest_to_target(opponents, player)
        if opp_distance > max_opponent_distance:
            viable_players.append((d, number, player))

    # once again check if there is no viable candidates
    # if you're the closest just return yourself and your number
    if len(viable_players) == 0:
        return your_distance_to_target, player_u

    # return the first viable candidate since all of them would be fine
    min_distance, number, player = viable_players[0]

    return min_distance, number


# find the single player closer to the target then you without opponents around them
def find_closest_player_forward_without_opponent(
    player_u, players, opponents, target, max_kick_distance, max_opp_distance
):
    # gets the coords of the current player
    cur_player = players[player_u]

    # find players that are closer then you to goal
    your_distance_to_target = distance(cur_player, target)
    players_closer_to_target = []

    for number, player in enumerate(players):
        d = distance(cur_player, player)
        # find people closer to the target then you
        # they should also be sufficiently closer, at least some x amount
        if d < your_distance_to_target:
            players_closer_to_target.append((number, player))

    # this doesn't run for whatever reason
    if len(players_closer_to_target) == 0:
        print("nobody closer to goal")
        return your_distance_to_target, player_u

    # now we have a list of all players closer to the target
    # from that, find the player that is closest to you that ISN'T YOU
    closest_players = []
    # furthest kicking distance
    kick_distance = max_kick_distance

    # gets a list of players that are within kick distance from you 5
    for player_info in players_closer_to_target:
        number, player = player_info

        d = distance(cur_player, player)
        if d < kick_distance and number != player_u:
            closest_players.append((d, number, player))

    # if you're the closest just return yourself and your number
    if len(closest_players) == 0:
        return your_distance_to_target, player_u

    # if there are players within kick distance from you
    # check which one of them are have players around them
    viable_players = []
    max_opponent_distance = max_opp_distance
    for d, number, player in closest_players:
        opp_distance, _ = find_closest_to_target(opponents, player)
        if opp_distance > max_opponent_distance:
            viable_players.append((d, number, player))

    # once again check if there is no viable candidates
    # if you're the closest just return yourself and your number
    if len(viable_players) == 0:
        return your_distance_to_target, player_u

    # return the first viable candidate since all of them would be fine
    min_distance, number, player = viable_players[0]

    return min_distance, number


def find_closest_player_forward(player_u, players, target):
    cur_player = players[player_u]

    # find players that are closer then you to goal
    your_distance_to_target = distance(cur_player, target)
    players_closer_to_target = []

    for number, player in enumerate(players):
        d = distance(cur_player, player)
        if d < your_distance_to_target:
            players_closer_to_target.append((number, player))

    # this doesn't run for whatever reason
    if len(players_closer_to_target) == 0:
        print("nobody closer to goal")
        return your_distance_to_target, player_u

    # now we have a list of all players closer to the target
    # from that, find the player that is closest to you that ISN'T YOU
    closest_player = None
    min_distance = np.inf

    for player_info in players_closer_to_target:
        number, player = player_info

        d = distance(cur_player, player)
        if d < min_distance and number != player_u:
            min_distance = d
            closest_player = number

    if closest_player == None:
        return your_distance_to_target, player_u

    return min_distance, closest_player
