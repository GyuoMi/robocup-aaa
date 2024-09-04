import numpy as np
from scipy.optimize import linear_sum_assignment
from strategy.Strategy import Strategy as strats


def subtract_row_minimum(matrix):
    for i in range(11):
        smallest = np.min(matrix[i, :])
        matrix[i, :] = matrix[i, :] - smallest
    return matrix


def subtract_col_minimum(matrix):
    for i in range(11):
        smallest = np.min(matrix[:, i])
        matrix[:, i] = matrix[:, i] - smallest
    return matrix


def find_covered_rows_and_cols(matrix, covered_rows, covered_cols):
    covered_rows.clear()
    covered_cols.clear()
    while np.any(matrix == 0):
        # column|row , value
        max_zero_row = (-1, -1)
        max_zero_col = (-1, -1)

        for i in range(11):
            if i in covered_rows:
                continue
            count = np.sum(matrix[i] == 0)
            if max_zero_row[1] > count:
                max_zero_row = (i, count)

        for i in range(11):
            if i in covered_cols:
                continue
            count = np.sum(matrix[:, i] == 0)
            if max_zero_col[1] > count:
                max_zero_col = (i, count)

        # select the row or column with the most 0's
        if max_zero_row[1] > max_zero_col[1]:
            row = max_zero_row[0]
            # turns every occurance of 0 to -1
            matrix[row, matrix[row] == 0] = -1
            covered_rows.append(row)
        else:
            col = max_zero_col[0]
            matrix[matrix[:, col] == 0, col] = -1
            covered_cols.append(col)

    # set all 0's set to -1 back to 0
    matrix[matrix == -1] = 0


def create_additional_zeros(matrix, covered_rows, covered_cols):
    uncovered_rows = []
    uncovered_cols = []
    # find uncovered rows and columns
    for i in range(11):
        if i not in covered_rows:
            uncovered_rows.append(i)
        if i not in covered_cols:
            uncovered_cols.append(i)

    # find the smallest value in uncovered elements
    smallest = 100000000
    for i in uncovered_rows:
        for j in uncovered_cols:
            smallest = min(smallest, matrix[i][j])

    # subtract smallest uncovered value from all uncovered row elements
    for i in uncovered_rows:
        for j in range(11):
            matrix[i][j] -= smallest

    # add smallest uncovered value to all covered column elements
    for i in covered_cols:
        for j in range(11):
            matrix[j][i] += smallest


def cover_zeros(matrix):
    lines = 0
    covered_rows = []
    covered_cols = []

    subtract_row_minimum(matrix)
    subtract_col_minimum(matrix)

    find_covered_rows_and_cols(matrix, covered_rows, covered_cols)
    lines = len(covered_rows) + len(covered_cols)
    while lines != 11:
        create_additional_zeros(matrix, covered_rows, covered_cols)
        # zero array before getting the next iteration of covered rows/columns
        find_covered_rows_and_cols(matrix, covered_rows, covered_cols)
        lines = len(covered_rows) + len(covered_cols)


def role_assignment(teammate_positions, formation_positions):

    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    # -----------------------------------------------------------#

    # step 1
    cost_matrix = strats.CalculateCostMatrix(
        team_pos=teammate_positions, form_pos=formation_positions
    )

    # convert to numpy array

    # step 2 - 6
    # modifies the cost matrix in place.
    cost_matrix = np.array(cost_matrix)  # requires np array
    cover_zeros(cost_matrix)

    # TODO: step 7
    # something here

    row_idx, col_idx = linear_sum_assignmene(cost_matrix)

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
