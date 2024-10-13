import numpy as np


def find_closest_to_target(players, target):

    closest_player = None
    min_distance = np.inf

    for player, point in enumerate(players):
        distance = np.sqrt((point[0] - target[0]) ** 2 + (point[1] - target[1]) ** 2)
        if distance < min_distance:
            closest_player = player
            min_distance = distance
    return min_distance, closest_player


def find_closest_player(player_u, players, target):

    closest_player = None
    min_distance = np.inf

    for player, point in enumerate(players):
        distance = np.sqrt((point[0] - target[0]) ** 2 + (point[1] - target[1]) ** 2)
        if distance < min_distance:
            closest_player = player
            min_distance = distance
    return min_distance, closest_player


def distance(one, two):
    return np.sqrt((one[0] - two[0]) ** 2 + (one[1] - two[1]) ** 2)


def find_closest_player_forward(player_u, players, target):
    cur_player = players[player_u]

    # find players that are closer then you to goal
    your_distance_to_target = distance(cur_player, target)
    players_closer_to_target = []

    for number, player in enumerate(players):
        d = distance(cur_player, player)
        if d < your_distance_to_target:
            players_closer_to_target.append((number, player))

    if len(players_closer_to_target) == 0:
        return 0, player_u

    # now we have a list of all players closer to the target
    # from that, find the player that is closest to you
    closest_player = None
    min_distance = np.inf
    for player_info in players_closer_to_target:
        number, player = player_info

        d = distance(cur_player, player)
        if d < min_distance:
            closest_player = number

    return min_distance, closest_player
