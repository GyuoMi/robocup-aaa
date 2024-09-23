import numpy as np
import time


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


def find_covered_rows_and_cols(matrix, covered_rows, covered_cols):
    covered_rows.clear()
    covered_cols.clear()
    while np.any(matrix == 0):
        # column|row , value
        max_zero_row = (-1, -1)
        max_zero_col = (-1, -1)

        for i in range(len(matrix)):
            if i in covered_rows:
                continue
            count = np.sum(matrix[i] == 0)
            if max_zero_row[1] < count:
                max_zero_row = (i, count)

        for i in range(len(matrix[0])):
            if i in covered_cols:
                continue
            count = np.sum(matrix[:, i] == 0)
            if max_zero_col[1] < count:
                max_zero_col = (i, count)

        # select the row or column with the most 0's
        if max_zero_row[1] > max_zero_col[1]:
            row = max_zero_row[0]
            # turns every occurance of 0 to -1 to show it has been used by a line
            matrix[row, matrix[row] == 0] = -np.inf
            covered_rows.append(row)
        else:
            col = max_zero_col[0]
            matrix[matrix[:, col] == 0, col] = -np.inf
            covered_cols.append(col)

    # set all 0's set to -1 back to 0
    matrix[matrix == -np.inf] = 0


def create_additional_zeros(matrix, covered_rows, covered_cols):
    uncovered_rows = []
    uncovered_cols = []
    # find uncovered rows and columns
    for i in range(len(matrix)):
        if i not in covered_rows:
            uncovered_rows.append(i)
        if i not in covered_cols:
            uncovered_cols.append(i)

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
        for j in range(len(matrix[0])):
            matrix[j][i] += smallest


def cover_zeros(matrix):
    lines = 0
    covered_rows = []
    covered_cols = []

    subtract_row_minimum(matrix)
    subtract_col_minimum(matrix)

    find_covered_rows_and_cols(matrix, covered_rows, covered_cols)
    lines = len(covered_rows) + len(covered_cols)
    while lines != len(matrix):
        create_additional_zeros(matrix, covered_rows, covered_cols)
        # zero array before getting the next iteration of covered rows/columns
        find_covered_rows_and_cols(matrix, covered_rows, covered_cols)
        lines = len(covered_rows) + len(covered_cols)
