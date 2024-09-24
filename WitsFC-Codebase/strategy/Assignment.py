from .Submission_One import cover_zeros
import numpy as np


from strategy.Strategy import Strategy
from world.World import World


def mask_out(matrix, row, col):
    for i in range(len(matrix[0])):
        matrix[row][i] = np.inf
    for j in range(len(matrix)):
        matrix[j][col] = np.inf


def find_row_with_least_zeros(matrix):
    min_zeros = np.inf
    row_index = -1

    for i, row in enumerate(matrix):
        zero_count = np.sum(row == 0.0)
        if 1 <= zero_count < min_zeros:
            min_zeros = zero_count
            row_index = i

    return row_index


def find_row_with_lowest_value(matrix):
    lowest_row_index = -1
    lowest_value = np.inf

    for i, row in enumerate(matrix):
        min_value = np.min(row)  # Find the minimum value in the current row
        if min_value < lowest_value:
            lowest_value = min_value
            lowest_row_index = i

    return lowest_row_index, lowest_value


def find_row_with_most_zeros(matrix):
    max_zeros = 0
    row_index = -1

    for i, row in enumerate(matrix):
        zero_count = np.sum(row == 0.0)
        if zero_count > max_zeros:
            max_zeros = zero_count
            row_index = i

    return row_index


def find_first_value(row, value):
    for i in range(len(row)):
        if row[i] == value:
            return i


def find_first_zero(row):
    for i in range(len(row)):
        if row[i] == 0.0:
            return i


def CalculateCostMatrix(team_pos, form_pos):
    n = len(team_pos)
    cost_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            cost_matrix[i][j] = np.linalg.norm(team_pos[i] - form_pos[j])
    return cost_matrix


def role_assignment(teammate_positions, formation_positions):

    np.set_printoptions(floatmode="fixed", precision=2, suppress=True)
    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    # -----------------------------------------------------------#
    # step 1
    # convert to numpy array
    # -----------------------------------------------------------#

    # may need to sort out parameter passed to strategy, could be okay i think
    cost_matrix = CalculateCostMatrix(teammate_positions, formation_positions)

    # step 2 - 6
    # modifies the cost matrix in place.
    cost_matrix = np.array(cost_matrix)  # requires np array
    cost_matrix = cover_zeros(cost_matrix)
    # print("cover zero Matrix:")
    # print("\n")
    # print(cost_matrix)
    # print("\n")
    # # TODO: step 7
    # something here
    n = cost_matrix.shape[0]
    point_preferences = {}

    while True:  # loop until zeros masked
        # find lowest zeros rows
        row_index = find_row_with_least_zeros(cost_matrix)

        if row_index == -1:
            # if np.any(np.isfinite(cost_matrix)):
            #     row_index, val = find_row_with_lowest_value(cost_matrix)
            #     col_index = find_first_value(cost_matrix[row_index], val)
            #     point_preferences[row_index + 1] = formation_positions[col_index]
            #     mask_out(cost_matrix, row_index, col_index)
            #     continue
            break

        col_index = find_first_zero(cost_matrix[row_index])

        point_preferences[row_index + 1] = formation_positions[col_index]
        # mask out row and col for selected zero
        mask_out(cost_matrix, row_index, col_index)

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
