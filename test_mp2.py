""" The unit tests for the GenGameBoard class. """
import unittest


from parameterized import parameterized
# import numpy.testing
import numpy as np

from mp2 import GenGameBoard


class TestGenGameBoard(unittest.TestCase):
    """ Will run tests against modules and functions in the GenGameBoard class. """

    def test_print_board(self):
        """ Tests that print_board() prints the game board with current marks. """
        self.skipTest('Test not yet created.')

    def test_make_move(self):
        """ Tests that make_move() attempts to make a move. """
        self.skipTest('Test not yet created.')

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

    def test_no_more_moves(self):
        """ Tests that no_more_moves() returns if there is are moves left. """
        self.skipTest('Test not yet created.')

    def test_make_computer_move(self):
        """ Tests the make_computer_move() function. """
        self.skipTest('Test not yet created.')

    def test_is_terminal(self):
        """ Tests the is_terminal() function. """
        self.skipTest('Test not yet created.')

    def test_get_est_utility(self):
        """ Tests the get_est_utility() function. """
        self.skipTest('Test not yet created.')

    def test_get_utility(self):
        """ Tests the get_utility() function. """
        self.skipTest('Test not yet created.')

    def test_get_actions(self):
        """ Tests the get_actions() function. """
        self.skipTest('Test not yet created.')

    def test_alpha_beta_search(self):
        """ Tests the alpha_beta_search() function. """
        self.skipTest('Test not yet created.')

    def test_max_value(self):
        """ Tests the max_value() function. """
        self.skipTest('Test not yet created.')

    def test_min_value(self):
        """ Tests the min_value() function. """
        self.skipTest('Test not yet created.')


if __name__ == '__main__':
    unittest.main()
