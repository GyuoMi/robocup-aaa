import numpy as np

import time


def subtract_row_minimum(matrix):
    # Step 1: Subtract the row minimum
    for i in range(matrix.shape[0]):
        matrix[i] -= np.min(matrix[i])
    return matrix


def subtract_col_minimum(matrix):
    for j in range(matrix.shape[1]):
        matrix[:, j] -= np.min(matrix[:, j])
    return matrix


def find_covered_rows_and_cols(matrix, covered_rows, covered_cols):
    while np.any(matrix == 0.0):
        # column|row , value
        max_zero_row = (-1, 0)
        max_zero_col = (-1, 0)

        for i in range(len(matrix)):
            if i in covered_rows:
                continue
            count = np.count_nonzero(matrix[i] == 0.0)
            if max_zero_row[1] < count:
                max_zero_row = (i, count)

        for j in range(len(matrix[0])):
            if j in covered_cols:
                continue
            count = np.count_nonzero(matrix[:, j] == 0.0)
            if max_zero_col[1] < count:
                max_zero_col = (j, count)

        # select the row or column with the most 0's
        if max_zero_row[1] >= max_zero_col[1]:
            row = max_zero_row[0]
            # turns every occurance of 0 to -1 to show it has been used by a line
            matrix[row, matrix[row] == 0.0] = -1
            covered_rows.append(row)
        else:
            col = max_zero_col[0]
            matrix[matrix[:, col] == 0.0, col] = -1
            covered_cols.append(col)
        print("matrix during greedy: \n", matrix)
        print("\n")

    # set all 0's set to -1 back to 0
    matrix[matrix == -1] = 0.0
    return matrix


# def find_covered_rows_and_cols(matrix, cov_rows, cov_cols):
#     while np.any(matrix == 0):
#         # Count zeros per row and column
#         row_zeros = np.sum(matrix == 0, axis=1)  # Sum along rows
#         col_zeros = np.sum(matrix == 0, axis=0)  # Sum along columns
#
#         # Find the row and column index with the maximum zeros
#         max_row_index = np.argmax(row_zeros)
#         max_col_index = np.argmax(row_zeros)
#
#         if (np.sum(matrix[max_row_index] == 0)) > (
#             np.sum(matrix[:, max_col_index] == 0)
#         ):
#             matrix[max_row_index, matrix[max_row_index] == 0.0] = -1
#             cov_rows.append(max_row_index)
#         else:
#             matrix[matrix[:, max_col_index] == 0.0, max_col_index] = -1
#             cov_cols.append(max_col_index)
#
#     matrix[matrix == -1] = 0


def create_additional_zeros(matrix, covered_rows, covered_cols):
    # find uncovered rows and columns
    uncovered_rows = [i for i in range(len(matrix)) if i not in covered_rows]
    uncovered_cols = [j for j in range(len(matrix)) if j not in covered_cols]

    # find the smallest value in uncovered elements
    smallest = np.inf
    for i in uncovered_rows:
        for j in uncovered_cols:
            smallest = min(smallest, matrix[i][j])

    # subtract smallest uncovered value from all uncovered row elements
    for i in uncovered_rows:
        for j in range(len(matrix)):
            matrix[i][j] -= smallest

    # add smallest uncovered value to all covered column elements
    for i in covered_cols:
        for j in range(len(matrix)):
            matrix[j][i] += smallest
    return matrix


def cover_zeros(matrix):
    lines = 0
    covered_rows = []
    covered_cols = []

    matrix = subtract_row_minimum(matrix)
    matrix = subtract_col_minimum(matrix)

    matrix = find_covered_rows_and_cols(matrix, covered_rows, covered_cols)
    lines = len(covered_rows) + len(covered_cols)
    while lines < len(matrix):
        matrix = create_additional_zeros(matrix, covered_rows, covered_cols)
        covered_rows = []
        covered_cols = []
        # zero array before getting the next iteration of covered rows/columns
        matrix = find_covered_rows_and_cols(matrix, covered_rows, covered_cols)

        lines = len(covered_rows) + len(covered_cols)

    return matrix
