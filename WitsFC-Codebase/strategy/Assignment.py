import numpy as np
from scipy.optimize import linear_sum_assignment


def CalculateCostMatrix(team_pos, form_pos):
    n = len(team_pos)
    cost_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            cost_matrix[i][j] = np.linalg.norm(team_pos[i] - form_pos[j])
    return cost_matrix


def role_assignment(teammate_positions, formation_positions):

    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    # -----------------------------------------------------------#

    cost_matrix = CalculateCostMatrix(teammate_positions, formation_positions)
    # Example
    point_preferences = {}

    row_idx, col_idx = linear_sum_assignment(cost_matrix)

    # Example
    point_preferences = {}
    for i in range(len(row_idx)):
        point_preferences[row_idx[i] + 1] = formation_positions[col_idx[i]]

    return point_preferences


from .Submission_Two import *


def pass_reciever_selector(player_unum, teammate_positions, final_target):
    player_unum -= 1
    # Input : Locations of all teammates and a final target you wish the ball to finish at
    # Output : Target Location in 2d of the player who is recieveing the ball
    # -----------------------------------------------------------#

    # pass to person closest to the goal
    # 1. to do that though we need to find which person is closest to the goal

    # finds closest player, which might be itself

    # min_distance, closest_player = find_closest_to_target(
    #     teammate_positions, final_target
    # )
    min_distance, closest_player = find_closest_player_forward(
        player_unum, teammate_positions, final_target
    )

    # if you are the closest then take the shot directly
    if player_unum == closest_player:
        target = final_target
    else:
        target = teammate_positions[closest_player]

    return min_distance, target
