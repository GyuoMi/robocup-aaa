from ..temp import *
import numpy as np


def role_assignment(teammate_positions, formation_positions):

    cost_matrix = CalculateCostMatrix(teammate_positions, formation_positions)
    point_preferences = {}
    copy_of_cost = cost_matrix.copy()
    cover_zeros(copy_of_cost)
    n = cost_matrix.shape[0]

    test = copy_of_cost

    while np.isfinite(test).any():  # loop until zeros masked
        # find lowest zeros rows
        zero_counts = [(i, np.sum(test[i] == 0)) for i in range(n)]
        zero_counts = [(i, count) for i, count in zero_counts if count > 0]

        if not zero_counts:
            if np.isfinite(test).any():
                copy_of_cost = cost_matrix.copy()
                cover_zeros(copy_of_cost)
                test = copy_of_cost
                continue
            break

        # select min zero row
        selected_row, _ = min(zero_counts, key=lambda x: x[1])

        # select lowest column index
        zero_cols = np.where(test[selected_row] == 0)[0]
        selected_col = zero_cols[0]
        point_preferences[selected_row + 1] = formation_positions[selected_col]
        # mask out row and col for selected zero
        test = mask_out(test, selected_row, selected_col)

    return point_preferences


def pass_reciever_selector(player_unum, teammate_positions, final_target):

    # Input : Locations of all teammates and a final target you wish the ball to finish at
    # Output : Target Location in 2d of the player who is recieveing the ball
    # -----------------------------------------------------------#

    # Example
    pass_reciever_unum = (
        player_unum + 1
    )  # This starts indexing at 1, therefore player 1 wants to pass to player 2

    if pass_reciever_unum != 12:
        target = teammate_positions[
            pass_reciever_unum - 1
        ]  # This is 0 indexed so we actually need to minus 1
    else:
        target = final_target

    return target
