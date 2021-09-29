""" The unit tests for the GenGameBoard class. """
import io
import math
import sys
import unittest

from parameterized import parameterized
import numpy.testing
import numpy as np

from mp2 import GenGameBoard


# We can do pruning and stop searching branches when we know the MIN state is already
# matching the MAX state... hard to explain. But this is the alpha-beta pruning.
# Read the chapter for better understanding.

# v --> utility_value
# alpha --> max utility value
# beta --> min utility value
# check for possible pruning in the minValue() and maxValue() functions

class TestGenGameBoard(unittest.TestCase):
    """ Will run tests against modules and functions in the GenGameBoard class. """

    @parameterized.expand([
        (
            "can place 'X' in empty field 1,1",
            [2, 'X', 1, 1],
            [[' ', ' '], [' ', ' ']],
            True,
            [['X', ' '], [' ', ' ']]
        ),
        (
            "can place 'X' in empty field 2,2",
            [3, 'X', 2, 2],
            [['O', 'O', 'O'], ['O', ' ', 'O'], ['O', 'O', 'O']],
            True,
            [['O', 'O', 'O'], ['O', 'X', 'O'], ['O', 'O', 'O']]
        ),
        (
            "cannot place 'X' in occupied field 3,1",
            [3, 'X', 3, 1],
            [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            False,
            [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']]
        ),
        (
            "cannot place 'O' in occupied field 3,1",
            [3, 'O', 3, 1],
            [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']],
            False,
            [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
        )
    ])
    def test_make_move(self, _test_name, move_data, marks, expected_success, desired_marks):
        """ Tests that make_move() attempts to make a move. """
        # Create the path and capture the output.
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # and redirect stdout.

        # Set up board.
        size = move_data[0]
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)

        # Attempt to make the move.
        mark = move_data[1]
        row = move_data[2]
        col = move_data[3]
        actual_result = GenGameBoard.make_move(test_board, row, col, mark)

        # Compare expected result with actual result.
        self.assertEqual(expected_success, actual_result)

        # Compare expected board marks with actual board marks after move.
        actual_marks = test_board.marks
        numpy.testing.assert_equal(actual_marks, desired_marks)

        # Print message if mark is 'X' and if a move cannot be made.
        error_msg = '\nThis position is already taken!\n'
        expected_message = '' if (expected_success or mark == 'O') else error_msg
        self.assertIn(expected_message, captured_output.getvalue())

    @parameterized.expand([
        (
            "should have winning row",
            3,
            [['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']],
            'X',
            True
        ),
        (
            "should have winning row",
            3,
            [[' ', ' ', ' '], ['X', 'X', 'X'], [' ', ' ', ' ']],
            'X',
            True
        ),
        (
            "should have winning row",
            3,
            [[' ', ' ', ' '], [' ', ' ', ' '], ['X', 'X', 'X']],
            'X',
            True
        ),
        (
            "should not have winning row",
            3,
            [['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']],
            'O',
            False
        ),
        (
            "should not have winning row",
            2,
            [['A', ' '], [' ', 'B']],
            'O',
            False
        )
    ])
    def test_check_for_win_rows(self, _test_name, board_size, board_marks, mark, expected_result):
        """ Tests using ROWS that check_for_win() returns if there is a win. """
        test_board = GenGameBoard(board_size)
        test_board.marks = np.copy(board_marks)
        actual_result = GenGameBoard.check_for_win(test_board, mark)
        self.assertEqual(expected_result, actual_result)

    @parameterized.expand([
        (
            "should have winning column",
            3,
            [['X', ' ', ' '], ['X', ' ', ' '], ['X', ' ', ' ']],
            'X',
            True
        ),
        (
            "should have winning column",
            3,
            [[' ', 'X', ' '], [' ', 'X', ' '], [' ', 'X', ' ']],
            'X',
            True
        ),
        (
            "should have winning column",
            3,
            [[' ', ' ', 'X'], [' ', ' ', 'X'], [' ', ' ', 'X']],
            'X',
            True
        ),
        (
            "should not have winning column",
            3,
            [['X', 'B', 'C'], ['X', 'B', ' '], ['X', 'B', ' ']],
            'O',
            False
        ),
        (
            "should not have winning column",
            2,
            [['A', ' '], [' ', 'B']],
            'O',
            False
        )
    ])
    def test_check_for_win_columns(self, _test_name, size, marks, mark, expected_result):
        """ Tests using COLUMNS that check_for_win() returns if there is a win. """
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)
        actual_result = GenGameBoard.check_for_win(test_board, mark)
        self.assertEqual(expected_result, actual_result)

    @parameterized.expand([
        (
            "should have winning diagonal",
            3,
            [['X', ' ', ' '], [' ', 'X', ' '], [' ', ' ', 'X']],
            'X',
            True
        ),
        (
            "should have winning diagonal",
            3,
            [[' ', ' ', 'X'], [' ', 'X', ' '], ['X', ' ', ' ']],
            'X',
            True
        ),
        (
            "should have winning diagonal",
            5,
            [
                ['X', ' ', ' ', ' ', ' '],
                [' ', 'X', ' ', ' ', ' '],
                [' ', ' ', 'X', ' ', ' '],
                [' ', ' ', ' ', 'X', ' '],
                [' ', ' ', ' ', ' ', 'X']
            ],
            'X',
            True
        ),
        (
            "should not have winning diagonal",
            3,
            [['X', 'B', 'C'], ['X', 'B', ' '], ['X', 'B', ' ']],
            'O',
            False
        ),
        (
            "should not have winning diagonal",
            2,
            [['A', ' '], [' ', 'B']],
            'O',
            False
        )
    ])
    def test_check_for_win_diagonals(self, _test_name, size, marks, mark, expected_result):
        """ Tests using COLUMNS that check_for_win() returns if there is a win. """
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)
        actual_result = GenGameBoard.check_for_win(test_board, mark)
        self.assertEqual(expected_result, actual_result)

    @parameterized.expand([
        ('return True if board is full', 2, [['A', 'B'], ['C'], ['D']], True),
        ('return False if board is not full', 2, [['A', 'B'], ['C', ' ']], False)
    ])
    def test_no_more_moves(self, _test_name, size, marks, expected_result):
        """ Tests that no_more_moves() returns if there is are moves left. """
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)
        actual_result = GenGameBoard.no_more_moves(test_board)
        self.assertEqual(expected_result, actual_result)

    @parameterized.expand([
        (
            'return True for win by X (row)',
            [['O', 'O', 'X'], ['X', 'X', 'X'], ['O', ' ', ' ']],
            True
        ),
        (
            'return True for win by O (col)',
            [['O', 'O', 'X'], ['O', 'X', 'X'], ['O', 'X', ' ']],
            True
        ),
        (
            'return True for no more moves',
            [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']],
            True
        ),
        (
            'return False when there is an empty space and no winner',
            [['A', 'B', 'C'], ['D', ' ', 'F'], ['G', 'H', 'I']],
            False
        )
    ])
    def test_is_terminal(self, _test_name, marks, expected_result):
        """ Tests the is_terminal() function. """
        size = 3
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)
        actual_result = GenGameBoard.is_terminal(test_board)
        self.assertEqual(expected_result, actual_result)

    @parameterized.expand([
        (
            'Get utility for terminal state, winning X (row)',
            [['X', 'X', 'X'], [' O', ' ', 'O'], [' ', 'O', ' ']],
            -1
        ),
        (
            'Get utility for terminal state, winning O (row)',
            [['X', ' ', 'X'], ['O', 'O', 'O'], [' ', 'X', ' ']],
            1
        ),
        (
            'Get utility for terminal state, winning X (col)',
            [['O', 'X', 'X'], ['  ', 'X', 'O'], ['O', 'X', 'O']],
            -1
        ),
        (
            'Get utility for terminal state, winning O (col)',
            [['X', 'O', 'X'], ['X', 'O', 'O'], [' ', 'O', 'X']],
            1
        ),
        (
            'Get utility for terminal state, draw',
            [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']],
            0
        )
    ])
    def test_get_utility(self, _test_name, marks, expected_result):
        """ Tests the get_utility() function. """
        size = 3
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)
        actual_result = GenGameBoard.get_utility(test_board)
        self.assertEqual(expected_result, actual_result)

    @parameterized.expand([
        (
            'Test bottom row actions',
            [['X', 'O', 'X'], ['O', 'X', 'O'], [' ', ' ', ' ']],
            [[2, 0], [2, 1], [2, 2]]
        ),
        (
                'Test diagonal  actions',
                [['X', 'O', ' '], ['O', ' ', 'O'], [' ', 'X', 'X']],
                [[0, 2], [1, 1], [2, 0]]
        )  # pylint: disable=no-self-use
    ])
    def test_get_actions(self, _test_name, marks, desired_marks):
        """ Tests the get_actions() function. """
        size = 3
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)
        actual_marks = GenGameBoard.get_actions(test_board)
        numpy.testing.assert_equal(actual_marks, desired_marks)

    @parameterized.expand([
        (
            'Test 1 for best action for MAX (player O)',
            [['X', 'O', 'X'], [' ', 'O', ' '], [' ', 'X', ' ']],
            -1,
            [1, 0]  # Row 2, Col 1 = [1, 0]
        ), (
            'Test 2 for best action for MAX (player O)',
            [['X', 'O', 'X'], ['O', 'O', 'X'], [' ', 'X', ' ']],
            -1,
            [2, 0]  # Row 3, Col 1 = [2, 0]
        )  # pylint: disable=no-self-use
    ])
    def test_max_value(self, _test_name, marks, expected_utility, expected_best):
        """ Tests the max_value() function. """
        size = 3
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)

        # Set inputs for the actual result
        alpha = 0
        beta = math.inf
        actual_result = GenGameBoard.max_value(test_board, alpha, beta)

        # Compare the expectation with actual results.
        self.assertEqual(expected_utility, actual_result[0])
        numpy.testing.assert_equal(actual_result[1], expected_best)

    @parameterized.expand([
        (
            'Test 1 for best action for MIN (player X)',
            [['X', 'O', 'X'], ['O', 'O', ' '], [' ', 'X', ' ']],
            -1
        ), (
            'Test 2 for best action for MIN (player X)',
            [['X', 'O', 'X'], ['O', 'O', 'X'], ['O', 'X', ' ']],
            -1
        )  # pylint: disable=no-self-use
    ])
    def test_min_value(self, _test_name, marks, expected_utility):
        """ Tests the min_value() function. """
        size = 3
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)

        # Set inputs for the actual result
        alpha = -math.inf
        beta = math.inf
        actual_result = GenGameBoard.min_value(test_board, alpha, beta)

        # Compare the expectation with actual results.
        self.assertEqual(expected_utility, actual_result)

    def test_alpha_beta_search(self):
        """ Tests the alpha_beta_search() function. """
        self.skipTest('Test not yet created.')

    def test_make_computer_move(self):
        """ Tests the make_computer_move() function. """
        self.skipTest('Test not yet created.')

    def test_print_board(self):
        """ Tests that print_board() prints the game board with current marks. """
        self.skipTest('Test not yet created.')


if __name__ == '__main__':
    unittest.main()
