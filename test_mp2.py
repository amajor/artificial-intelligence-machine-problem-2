""" The unit tests for the GenGameBoard class. """
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
# check for possible pruning in the minValue() and maxValue() functiosn

class TestGenGameBoard(unittest.TestCase):
    """ Will run tests against modules and functions in the GenGameBoard class. """

    @parameterized.expand([
        (
            "can place 'X' in empty field 1,1",
            [2, 'X', 1, 1],
            [[' ', ' '], [' ', ' ']],
            True,
            [['X', ' '], [' ', ' ']],
        ),
        (
            "can place 'X' in empty field 2,2",
            [3, 'X', 2, 2],
            [['O', 'O', 'O'], ['O', ' ', 'O'], ['O', 'O', 'O']],
            True,
            [['O', 'O', 'O'], ['O', 'X', 'O'], ['O', 'O', 'O']],
        ),
        (
            "cannot place 'X' in occupied field 3,1",
            [3, 'X', 3, 1],
            [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            False,
            [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
        ),
        (
            "cannot place 'O' in occupied field 3,1",
            [3, 'O', 3, 1],
            [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']],
            False,
            [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']],
        )
    ])
    def test_make_move(self, _test_name, move_data, marks, expected_success, desired_marks):
        """ Tests that make_move() attempts to make a move. """
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

        # TODO: Check to see if we print a message when we cannot move and the mark is 'X'
        # Print message if mark is 'X' and if a move cannot be made.

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
        ('Estimate at -117', [['X', 'O', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']], -117),
        ('Estimate at -27', [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], -27),
        ('Estimate at 36', [[' ', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']], 36),
        ('Estimate at -36', [[' ', ' ', ' '], [' ', 'X', ' '], [' ', ' ', ' ']], -36)
    ])
    def test_get_est_utility(self, _test_name, marks, expected_result):
        """ Tests the get_est_utility() function. """
        size = 3
        test_board = GenGameBoard(size)
        test_board.marks = np.copy(marks)
        actual_result = GenGameBoard.get_est_utility(test_board)
        self.assertEqual(expected_result, actual_result)

    @parameterized.expand([
        # ('Estimate at -117', [['X', 'O', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']], -117),
        # ('Estimate at -27', [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']], -27),
        # ('Estimate at 36', [[' ', ' ', ' '], [' ', 'O', ' '], [' ', ' ', ' ']], 36),
        # ('Estimate at -36', [[' ', ' ', ' '], [' ', 'X', ' '], [' ', ' ', ' ']], -36)
        (
            'Get utility for terminal state, winning X (row)',
            [['X', 'X', 'X'], [' O', ' ', 'O'], [' ', 'O', ' ']],
            -1000
        ),
        (
            'Get utility for terminal state, winning O (row)',
            [['X', ' ', 'X'], ['O', 'O', 'O'], [' ', 'X', ' ']],
            1000
        ),
        (
            'Get utility for terminal state, winning X (col)',
            [['O', 'X', 'X'], ['  ', 'X', 'O'], ['O', 'X', 'O']],
            -1000
        ),
        (
            'Get utility for terminal state, winning O (col)',
            [['X', 'O', 'X'], ['X', 'O', 'O'], [' ', 'O', 'X']],
            1000
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

    def test_get_actions(self):
        """ Tests the get_actions() function. """
        self.skipTest('Test not yet created.')

    def test_alpha_beta_search(self):
        """ Tests the alpha_beta_search() function. """
        self.skipTest('Test not yet created.')

    def test_make_computer_move(self):
        """ Tests the make_computer_move() function. """
        self.skipTest('Test not yet created.')

    def test_max_value(self):
        """ Tests the max_value() function. """
        self.skipTest('Test not yet created.')

    def test_min_value(self):
        """ Tests the min_value() function. """
        self.skipTest('Test not yet created.')

    def test_print_board(self):
        """ Tests that print_board() prints the game board with current marks. """
        self.skipTest('Test not yet created.')


if __name__ == '__main__':
    unittest.main()
