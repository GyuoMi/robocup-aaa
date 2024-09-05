import unittest
from Submission_One import *


class TestSubOne(unittest.TestCase):
    # has to use numpy array
    def test_subtract_row_minimum(self):
        input = np.array([[15, 40, 45], [20, 60, 35], [20, 40, 25]])
        expected_output = np.array([[0, 25, 30], [0, 40, 15], [0, 20, 5]])

        test_matrix = input.copy()

        subtract_row_minimum(test_matrix)

        self.assertEqual(expected_output.tolist(), test_matrix.tolist())

    def test_subtract_col_minimum(self):
        input = np.array([[0, 25, 30], [0, 40, 15], [0, 20, 5]])
        expected_output = np.array([[0, 5, 25], [0, 20, 10], [0, 0, 0]])

        test_matrix = input.copy()
        subtract_col_minimum(test_matrix)

        self.assertEqual(expected_output.tolist(), test_matrix.tolist())

    def test_cover_all_zeros_with_min_lines(self):
        input = np.array([[0, 5, 25], [0, 20, 10], [0, 0, 0]])
        test_matrix = input.copy()
        covered_rows = []
        covered_cols = []
        find_covered_rows_and_cols(test_matrix, covered_rows, covered_cols)
        lines = len(covered_cols) + len(covered_rows)
        # check to see if it correctly crossed off the lines
        self.assertEqual(lines, 2)

        # check to see if it reset all values in array
        self.assertEqual(input.tolist(), test_matrix.tolist())

    def test_create_additional_zeros(self):
        input = np.array([[0, 5, 25], [0, 20, 10], [0, 0, 0]])
        expected_output = np.array([[0, 0, 20], [0, 15, 5], [5, 0, 0]])

        test_matrix = input.copy()
        covered_rows = [2]
        covered_cols = [0]
        create_additional_zeros(test_matrix, covered_rows, covered_cols)

        self.assertEqual(expected_output.tolist(), test_matrix.tolist())

    def test_cover_zeros(self):
        input = np.array([[15, 40, 45], [20, 60, 35], [20, 40, 25]])
        expected_output = np.array([[0, 0, 20], [0, 15, 5], [5, 0, 0]])

        test_matrix = input.copy()
        cover_zeros(test_matrix)

        self.assertEqual(expected_output.tolist(), test_matrix.tolist())


if __name__ == "__main__":
    unittest.main()