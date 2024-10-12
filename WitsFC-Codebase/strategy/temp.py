from math import isfinite
import numpy as np
import time
import random
from numpy.core.numeric import isclose


def CalculateCostMatrix(team_pos, form_pos):
    n = len(team_pos)
    cost_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            cost_matrix[i][j] = np.linalg.norm(team_pos[i] - form_pos[j])
    return cost_matrix


def mask_out(matrix, row, col):
    matrix[row, :] = np.inf
    matrix[:, col] = np.inf
    return matrix


def subtract_row_minimum(matrix):
    for i in range(len(matrix)):
        smallest = np.min(matrix[i, :])
        matrix[i, :] = matrix[i, :] - smallest
    return matrix


def subtract_col_minimum(matrix):
    for i in range(len(matrix[0])):
        smallest = np.min(matrix[:, i])
        matrix[:, i] = matrix[:, i] - smallest
    return matrix


# have to copy the matrix every time as setting row/col to np.inf is a destructive process
# you might not be able to uncover the same values that was covered.
def find_covered_rows_and_cols(m, c_rows, c_cols):
    c_rows = set()
    c_cols = set()

    is_o = [False]
    o_rows = []
    o_cols = []

    def recursive(matrix, covered_rows, covered_cols):
        if is_o[0]:
            return

        # if there are no more zeros to cross off
        if not np.any(np.isclose(matrix, 0.0)):

            # if we covered 11 values, but it's not optimal then skip this path and go down the next
            # if there are no more zeros and this is the best we can do, save the values

            lines = len(covered_cols) + len(covered_rows)
            print(lines)

            if len(covered_cols) + len(covered_rows) == len(matrix):
                matrix[matrix == -np.inf] = 0.0
                if is_optimal(matrix):
                    print("here")
                    is_o[0] = True
                    o_rows.clear()
                    o_cols.clear()
                    o_rows.append(np.copy(covered_rows))
                    o_cols.append(np.copy(covered_cols))
                    return

            c_rows.add(covered_rows.copy())
            c_cols.add(covered_cols.copy())
            return

        # column|row , value
        max_zero_row = (-1, 0.0)
        max_zero_col = (-1, 0.0)

        for i in range(len(matrix)):
            if i in covered_rows:
                continue
            count = np.sum(np.isclose(matrix[i], 0.0))
            if max_zero_row[1] < count:
                max_zero_row = (i, count)

        for i in range(len(matrix[0])):
            if i in covered_cols:
                continue
            count = np.sum(np.isclose(matrix[:, i], 0.0))
            if max_zero_col[1] < count:
                max_zero_col = (i, count)

        if max_zero_row[1] == max_zero_col[1]:

            mat_one = np.copy(matrix)
            mat_two = np.copy(matrix)

            row = max_zero_row[0]
            # turns every occurance of 0 to -1 to show it has been used by a line
            mat_one[row, np.isclose(matrix[row], 0.0)] = -np.inf
            # matrix[row, matrix[row] == 0.0] = -np.inf
            covered_rows.add(row)

            recursive(mat_one, covered_rows, covered_cols)
            covered_rows.pop()

            if is_o[0] == True:
                return

            col = max_zero_col[0]
            # matrix[matrix[:, col] == 0.0, col] = -np.inf
            mat_two[np.isclose(matrix[:, col], 0.0), col] = -np.inf
            covered_cols.add(col)

            recursive(mat_two, covered_rows, covered_cols)

            covered_cols.pop()

            return

        if max_zero_row[1] > max_zero_col[1]:
            row = max_zero_row[0]
            # turns every occurance of 0 to -1 to show it has been used by a line
            matrix[row, np.isclose(matrix[row], 0.0)] = -np.inf
            covered_rows.add(row)

            recursive(np.copy(matrix), covered_rows, covered_cols)

            # if you come back up from the recursion you you need to undo what you did
            # don't need to do this because we're copying the entire array every time
            # matrix[row, np.isclose(matrix[row], -np.inf)] = 0.0
            covered_rows.pop()
        else:
            col = max_zero_col[0]
            # matrix[matrix[:, col] == 0.0, col] = -np.inf
            matrix[np.isclose(matrix[:, col], 0.0), col] = -np.inf
            covered_cols.add(col)

            recursive(np.copy(matrix), covered_rows, covered_cols)

            covered_cols.pop()
        return

    recursive(np.copy(m), set(), set())

    if is_o[0]:
        return o_rows[0], o_cols[0]

    print(c_rows)
    print(c_cols)
    return c_rows[0], c_cols[0]


# def find_covered_rows_and_cols(matrix, covered_rows, covered_cols):
#     covered_rows.clear()
#     covered_cols.clear()
#
#     while np.any(np.isclose(matrix, 0.0)):
#         # column|row , value
#         max_zero_row = (-1, 0.0)
#         max_zero_col = (-1, 0.0)
#
#         for i in range(len(matrix)):
#             if i in covered_rows:
#                 continue
#             count = np.sum(np.isclose(matrix[i], 0.0))
#             if max_zero_row[1] < count:
#                 max_zero_row = (i, count)
#
#         for i in range(len(matrix[0])):
#             if i in covered_cols:
#                 continue
#             count = np.sum(np.isclose(matrix[:, i], 0.0))
#             if max_zero_col[1] < count:
#                 max_zero_col = (i, count)
#
#         if max_zero_row[1] == max_zero_col[1]:
#             val = random.choice([0, 1])
#             if val == 1:
#                 row = max_zero_row[0]
#                 # turns every occurance of 0 to -1 to show it has been used by a line
#                 matrix[row, np.isclose(matrix[row], 0.0)] = -np.inf
#                 # matrix[row, matrix[row] == 0.0] = -np.inf
#                 covered_rows.append(row)
#                 continue
#             else:
#                 col = max_zero_col[0]
#                 # matrix[matrix[:, col] == 0.0, col] = -np.inf
#                 matrix[np.isclose(matrix[:, col], 0.0), col] = -np.inf
#                 covered_cols.append(col)
#                 continue
#
#         # select the row or column with the most 0's
#         if max_zero_row[1] >= max_zero_col[1]:
#             row = max_zero_row[0]
#             # turns every occurance of 0 to -1 to show it has been used by a line
#             matrix[row, np.isclose(matrix[row], 0.0)] = -np.inf
#             # matrix[row, matrix[row] == 0.0] = -np.inf
#             covered_rows.append(row)
#         else:
#             col = max_zero_col[0]
#             # matrix[matrix[:, col] == 0.0, col] = -np.inf
#             matrix[np.isclose(matrix[:, col], 0.0), col] = -np.inf
#             covered_cols.append(col)
#
#     # set all 0's set to -1 back to 0
#     matrix[matrix == -np.inf] = 0.0
#


# returns false if matrix not possible for optimal assignment
# returns true if it is with modified point_preferences
def get_assignment(matrix, point_preferences, formation_positions):
    test = np.copy(matrix)
    point_preferences.clear()
    n = len(matrix)
    while np.isfinite(test).any():  # loop until zeros masked
        # find lowest zeros rows
        zero_counts = [(i, np.sum(test[i] == 0)) for i in range(n)]
        zero_counts = [(i, count) for i, count in zero_counts if count > 0]

        if not zero_counts:
            if np.isfinite(test).any():
                return False
            else:
                return True

        # select min zero row
        selected_row, _ = min(zero_counts, key=lambda x: x[1])

        # select lowest column index
        zero_cols = np.where(test[selected_row] == 0)[0]
        selected_col = zero_cols[0]
        point_preferences[selected_row + 1] = formation_positions[selected_col]
        # mask out row and col for selected zero
        test = mask_out(test, selected_row, selected_col)


def is_optimal(matrix):
    test = matrix
    n = len(matrix)
    while True:  # loop until zeros masked
        # find lowest zeros rows
        zero_counts = [(i, np.sum(test[i] == 0)) for i in range(n)]
        zero_counts = [(i, count) for i, count in zero_counts if count > 0]

        if not zero_counts:
            print(test)
            if np.isfinite(test).any():
                return False
            else:
                return True

        # select min zero row
        selected_row, _ = min(zero_counts, key=lambda x: x[1])

        # select lowest column index
        zero_cols = np.where(test[selected_row] == 0)[0]
        selected_col = zero_cols[0]
        # mask out row and col for selected zero
        test = mask_out(test, selected_row, selected_col)


def create_additional_zeros(matrix, covered_rows, covered_cols):
    # Determine which rows and columns are uncovered
    uncovered_rows = [i for i in range(len(matrix)) if i not in covered_rows]
    uncovered_cols = [j for j in range(len(matrix[0])) if j not in covered_cols]

    # Find the smallest value in the uncovered elements
    min_uncovered_value = np.inf
    for i in uncovered_rows:
        for j in uncovered_cols:
            if matrix[i, j] < min_uncovered_value:
                min_uncovered_value = matrix[i, j]

    # Subtract the minimum uncovered value from all uncovered elements
    for i in uncovered_rows:
        matrix[i, :] -= min_uncovered_value

    # Add the minimum uncovered value to all elements that are covered twice (both row and column)
    for j in covered_cols:
        matrix[:, j] += min_uncovered_value


def cover_zeros(matrix):
    lines = 0
    covered_rows = []
    covered_cols = []

    subtract_row_minimum(matrix)
    subtract_col_minimum(matrix)

    covered_rows, covered_cols = find_covered_rows_and_cols(
        matrix, covered_rows, covered_cols
    )

    lines = len(covered_rows) + len(covered_cols)

    while lines != len(matrix):
        create_additional_zeros(matrix, covered_rows, covered_cols)
        # zero array before getting the next iteration of covered rows/columns
        covered_cols = []
        covered_rows = []
        covered_rows, covered_cols = find_covered_rows_and_cols(
            matrix, covered_rows, covered_cols
        )
        lines = len(covered_rows) + len(covered_cols)


teammate_positions = np.array(
    [
        [-14.0, 0],
        [-9.00671841, -5.0212432],
        [-9.0, 0],
        [-8.9, 5.0],
        [-5.05693005, -5.02106853],
        [-5.0216475, -0.03376451],
        [-4.9, 4.9],
        [-1.06363536, -5.95482965],
        [-1.03039866, -2.47499713],
        [-1.01752962, 2.52498091],
        [-1.02189553, 6.02497721],
    ]
)

formation_positions = np.array(
    [
        [-13, 0],
        [-10, -2],
        [-11, 3],
        [-8, 0],
        [-3, 0],
        [0, 1],
        [2, 0],
        [3, 3],
        [9, 1],
        [12, 0],
        [8, 0],
    ]
)

cost_matrix = np.array(
    [
        [1.00, 4.52, 4.17, 6.00, 11.00, 14.03, 16.00, 17.25, 22.00, 23.02, 26.00],
        [6.40, 3.16, 8.25, 5.10, 7.81, 10.82, 12.08, 14.42, 17.72, 18.97, 21.59],
        [4.00, 2.24, 3.61, 1.00, 6.00, 9.06, 11.00, 12.37, 17.00, 18.03, 21.00],
        [6.40, 7.07, 2.83, 5.10, 7.81, 9.85, 12.08, 12.17, 17.72, 18.44, 21.59],
        [9.44, 5.83, 10.01, 5.85, 5.42, 7.84, 8.63, 11.34, 13.95, 15.26, 17.74],
        [8.00, 5.39, 6.71, 3.00, 2.00, 5.10, 7.00, 8.54, 13.00, 14.04, 17.00],
        [9.43, 8.60, 6.32, 5.83, 5.39, 6.40, 8.60, 8.25, 13.93, 14.56, 17.72],
        [13.40, 9.84, 13.43, 9.20, 6.30, 7.04, 6.68, 9.82, 10.80, 12.19, 14.31],
        [12.29, 9.04, 11.44, 7.46, 3.21, 3.62, 3.87, 6.77, 9.31, 10.56, 13.21],
        [12.25, 10.07, 10.00, 7.43, 3.22, 1.84, 3.94, 4.04, 9.37, 10.13, 13.26],
        [13.46, 12.11, 10.47, 9.28, 6.42, 5.20, 6.80, 5.06, 10.87, 11.23, 14.36],
    ]
)


cost_matrix = CalculateCostMatrix(teammate_positions, formation_positions)
point_preferences = {}
np.set_printoptions(floatmode="fixed", precision=2, suppress=True)

# copy the array
copy_of_cost = cost_matrix.copy()

# change the copy
cover_zeros(copy_of_cost)
n = cost_matrix.shape[0]


# assign copy to test
test = copy_of_cost


while True:  # loop until zeros masked
    # find lowest zeros rows
    zero_counts = [(i, np.sum(test[i] == 0)) for i in range(n)]
    zero_counts = [(i, count) for i, count in zero_counts if count > 0]

    if not zero_counts:
        if np.isfinite(test).any():
            print("fail")
            break
        break

    # select min zero row
    selected_row, _ = min(zero_counts, key=lambda x: x[1])

    # select lowest column index
    zero_cols = np.where(test[selected_row] == 0)[0]
    selected_col = zero_cols[0]
    point_preferences[selected_row + 1] = formation_positions[selected_col]
    # mask out row and col for selected zero
    test = mask_out(test, selected_row, selected_col)
    # print(f"masked cost matrix \n\n{test}\n")
