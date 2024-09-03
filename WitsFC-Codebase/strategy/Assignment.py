import numpy as np
from scipy.optimize import linear_sum_assignment
from strategy.Strategy import Strategy
from world.World import World
def role_assignment(teammate_positions, formation_positions):

    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    #-----------------------------------------------------------#

    # may need to sort out parameter passed to strategy, could be okay i think
    strats = Strategy(World)
    cost_matrix = strats.CalculateCostMatrix(teammate_positions, formation_positions)

    row_idx, col_idx = linear_sum_assignment(cost_matrix)

    # Example
    point_preferences = {}
    for i in range(len(row_idx)):
        point_preferences[row_idx[i] + 1] = formation_positions[col_idx[i]]


    return point_preferences


def pass_reciever_selector(player_unum, teammate_positions, final_target):

    # Input : Locations of all teammates and a final target you wish the ball to finish at
    # Output : Target Location in 2d of the player who is recieveing the ball
    #-----------------------------------------------------------#

    # Example
    pass_reciever_unum = player_unum + 1                  #This starts indexing at 1, therefore player 1 wants to pass to player 2

    if pass_reciever_unum != 12:
        target = teammate_positions[pass_reciever_unum-1] #This is 0 indexed so we actually need to minus 1
    else:
        target = final_target

    return target
