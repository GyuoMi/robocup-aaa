from .Submission_One import cover_zeros
import numpy as np

from scipy.optimize import linear_sum_assignment

from strategy.Strategy import Strategy
from world.World import World

def mask_out(matrix, row, col):
    matrix[row, :] = float('inf')
    matrix[:, col] = float('inf')
    return matrix


def role_assignment(teammate_positions, formation_positions):

    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    # -----------------------------------------------------------#
    # step 1
    # convert to numpy array
    #-----------------------------------------------------------#

    # may need to sort out parameter passed to strategy, could be okay i think
    strats = Strategy(World)
    cost_matrix = strats.CalculateCostMatrix(teammate_positions, formation_positions)

    # step 2 - 6
    # modifies the cost matrix in place.
    cost_matrix = np.array(cost_matrix)  # requires np array
    cover_zeros(cost_matrix)

    # TODO: step 7
    # something here
    n = cost_matrix.shape[0]
    point_preferences = {}

    while np.isfinite(cost_matrix).any():  # loop until zeros masked
        # find lowest zeros rows
        zero_counts = [(i, np.sum(cost_matrix[i] == 0)) for i in range(n)]
        zero_counts = [(i, count) for i, count in zero_counts if count > 0]

        if not zero_counts:
            break

        # select min zero row
        selected_row, _ = min(zero_counts, key=lambda x: x[1])

        # select lowest column index
        zero_cols = np.where(cost_matrix[selected_row] == 0)[0]
        selected_col = zero_cols[0]

        point_preferences[selected_row + 1] = formation_positions[selected_col]

        # mask out row and col for selected zero
        cost_matrix = mask_out(cost_matrix, selected_row, selected_col)

    row_idx, col_idx = linear_sum_assignment(cost_matrix)

    # Example
    point_preferences = {}
    for i in range(len(row_idx)):
        point_preferences[row_idx[i] + 1] = formation_positions[col_idx[i]]

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
