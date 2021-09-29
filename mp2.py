"""
Alison Major
September 20, 2021
Artificial Intelligence 1 – CPSC 57100
Fall Semester 2021
Machine Problem 2

Full code and test suite available on GitHub:
https://github.com/amajor/artificial-intelligence-machine-problem-2
"""

import math
import numpy as np


def print_current_depth(debugging_on):
    """
    Strictly for debugging purposes
    """
    depth = GenGameBoard.depth
    if debugging_on:
        print(' ' * depth, '---> Depth:', depth)


class GenGameBoard:
    """
    Class responsible for representing the game board and game playing methods
    """
    num_pruned = 0  # counts number of pruned branches due to alpha/beta
    utility_max = 0  # counts number of pruned branches due to reaching maximum utility
    utility_min = 0  # counts number of pruned branches due to reaching minimum utility
    MAX_DEPTH = 6  # max depth before applying evaluation function
    depth = 0  # current depth within minimax search

    DEBUGGING_ON = False  # Whether we should print debugging information

    def __init__(self, board_size):
        """
        Constructor method - initializes each position variable and the board size
        """
        # Holds the size of the board
        self.board_size = board_size

        # Holds the mark for each position
        self.marks = np.empty((board_size, board_size), dtype='str')
        self.marks[:, :] = ' '

    def print_board(self):
        """
        Prints the game board using current marks
        """
        # Print the column numbers
        print(' ', end='')
        for j in range(self.board_size):
            print(" " + str(j + 1), end='')

        # Print the rows with marks
        print("")
        for i in range(self.board_size):
            # Print the line separating the row
            print(" ", end='')
            for j in range(self.board_size):
                print("--", end='')

            print("-")

            # Print the row number
            print(i + 1, end='')

            # Print the marks on self row
            for j in range(self.board_size):
                print("|" + self.marks[i][j], end='')

            print("|")

        # Print the line separating the last row
        print(" ", end='')
        for j in range(self.board_size):
            print("--", end='')

        print("-")

    def make_move(self, row, col, mark):
        """
        Attempts to make a move given the row, col, and mark.
        If move cannot be made, returns False and prints a message if mark is 'X' (player).
        Otherwise, returns True
        """
        possible = False  # Variable to hold the return value
        if row == -1 and col == -1:
            return False

        # Change the row,col entries to array indexes
        row = row - 1
        col = col - 1

        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            print("Not a valid row or column!")
            return False

        # Check row and col, and make sure space is empty
        # If empty, set the position to the mark and change possible to True
        if self.marks[row][col] == ' ':
            self.marks[row][col] = mark
            possible = True

        # Print out the message to the player if the move was not possible
        if not possible and mark == 'X':
            print("\nThis position is already taken!")

        return possible

    def check_for_win(self, mark):
        """
        Determines whether a game winning condition exists.
        If so, returns True, and False otherwise.
        """
        won = False  # Variable holding the return value

        # Check wins by examining each combination of positions, where N is the board size.
        #   1. Check each row for N matching values.
        #   2. Check each column for N matching values.
        #   3. Check the first diagonal for N matching values.
        #   4. Check the second diagonal for N matching values.

        # Check each row.
        for i in range(self.board_size):
            won = True
            for j in range(self.board_size):
                if self.marks[i][j] != mark:
                    won = False
                    break
            if won:
                break

        # Check each column.
        if not won:
            for i in range(self.board_size):
                won = True
                for j in range(self.board_size):
                    if self.marks[j][i] != mark:
                        won = False
                        break
                if won:
                    break

        # Check first diagonal.
        if not won:
            for i in range(self.board_size):
                won = True
                if self.marks[i][i] != mark:
                    won = False
                    break

        # Check second diagonal.
        if not won:
            for i in range(self.board_size):
                won = True
                if self.marks[self.board_size - 1 - i][i] != mark:
                    won = False
                    break

        return won

    def no_more_moves(self):
        """
        Determines whether the board is full.
        If full, returns True, and False otherwise.
        """
        return (self.marks != ' ').all()

    # TODO - self method should run minimax to determine the value of each move
    # Then make best move for the computer by placing the mark in the best spot
    def make_computer_move(self):
        """ Make the computer move based on best action. """
        # Make AI move
        best_action = self.alpha_beta_search()
        row = best_action[0] + 1
        col = best_action[1] + 1
        # TODO: Only make this move if it's allowed, otherwise pick new action.
        self.make_move(row, col, 'O')
        print("Computer chose: " + str(row) + "," + str(col))

    def is_terminal(self):
        """
        Determines if the current board state is a terminal state
        """
        return self.no_more_moves() or self.check_for_win('X') or self.check_for_win('O')

    def get_est_utility(self):
        """
        Implements an evaluation function to estimate the utility of current state
        """
        assert not self.is_terminal()
        points = 0

        # Check each row
        for i in range(self.board_size):
            num_o_in_row = 0
            num_x_in_row = 0
            for j in range(self.board_size):
                if self.marks[i][j] == 'O':
                    num_o_in_row = num_o_in_row + 1
                elif self.marks[i][j] == 'X':
                    num_x_in_row = num_x_in_row + 1
            points = points + 10 ** num_o_in_row - 10 ** num_x_in_row

        # Check each column
        for i in range(self.board_size):
            num_o_in_row = 0
            num_x_in_row = 0
            for j in range(self.board_size):
                if self.marks[j][i] == 'O':
                    num_o_in_row = num_o_in_row + 1
                elif self.marks[j][i] == 'X':
                    num_x_in_row = num_x_in_row + 1
            points = points + 10 ** num_o_in_row - 10 ** num_x_in_row

        # Check main diagonal
        num_o_in_row = 0
        num_x_in_row = 0
        for i in range(self.board_size):
            if self.marks[i][i] == 'O':
                num_o_in_row = num_o_in_row + 1
            elif self.marks[i][i] == 'X':
                num_x_in_row = num_x_in_row + 1
        points = points + 10 ** num_o_in_row - 10 ** num_x_in_row

        # Check other diagonal
        num_o_in_row = 0
        num_x_in_row = 0
        for i in range(self.board_size):
            if self.marks[self.board_size - 1 - i][i] == 'O':
                num_o_in_row = num_o_in_row + 1
            elif self.marks[self.board_size - 1 - i][i] == 'X':
                num_x_in_row = num_x_in_row + 1
        points = points + 10 ** num_o_in_row - 10 ** num_x_in_row

        return points

    def get_utility(self):
        """
        Finds the utility of a terminal state
        """
        assert self.is_terminal()
        if self.check_for_win('X'):
            return -10 ** self.board_size
        elif self.check_for_win('O'):
            return 10 ** self.board_size
        else:
            return 0

    def get_actions(self):
        """ Generates a list of possible moves. """
        return np.argwhere(self.marks == ' ')

    def alpha_beta_search(self):
        """
        Go through all possible successor states and generate the max_value
        return action (row,col) that gives the max
        uses the backtracking method
        """
        GenGameBoard.depth = 0
        utility_value, best_action = self.max_value(-math.inf, math.inf)
        print_current_depth(GenGameBoard.DEBUGGING_ON)
        return best_action

    def max_value(self, alpha, beta):
        """
        Finds the action that gives highest minimax value for computer
        Returns both best action and the resulting value
        """
        print_current_depth(GenGameBoard.DEBUGGING_ON)
        if self.is_terminal():
            return self.get_utility(), np.array([-1, -1])
        if GenGameBoard.depth > GenGameBoard.MAX_DEPTH:
            return self.get_est_utility(), np.array([-1, -1])
        utility_value = -math.inf
        for action in self.get_actions():
            GenGameBoard.depth = GenGameBoard.depth + 1
            # current_marks = np.array(self.marks) # save current state, so it can be backtracked
            # self.makeMove(action[0]+1, action[1]+1, 'O')
            self.marks[action[0]][action[1]] = 'O'
            min_val = self.min_value(alpha, beta)
            GenGameBoard.depth = GenGameBoard.depth - 1
            if min_val > utility_value:
                utility_value = min_val
                best_action = action
            # utility_value = max(v, self.min_value(alpha, beta))
            # self.marks = current_marks # backtrack to prior state
            self.marks[action[0]][action[1]] = ' '

            if utility_value >= 10 ** self.board_size:
                GenGameBoard.utility_max = GenGameBoard.utility_max + 1
                return utility_value, best_action
            if utility_value >= beta:
                GenGameBoard.num_pruned = GenGameBoard.num_pruned + 1
                return utility_value, best_action

            # Set the MAX utility value (alpha)
            alpha = max(alpha, utility_value)
        return utility_value, best_action

    def min_value(self, alpha, beta):
        """
        Finds the action that gives lowest minimax value for computer
        Returns the resulting value
        """
        print_current_depth(GenGameBoard.DEBUGGING_ON)
        if self.is_terminal():
            return self.get_utility()
        if GenGameBoard.depth > GenGameBoard.MAX_DEPTH:
            return self.get_est_utility()
        utility_value = math.inf
        for action in self.get_actions():
            GenGameBoard.depth = GenGameBoard.depth + 1
            # current_marks = np.array(self.marks) # save current state, so it can be backtracked
            # self.makeMove(action[0]+1, action[1]+1, 'X')
            self.marks[action[0]][action[1]] = 'X'
            utility_value = min(utility_value, self.max_value(alpha, beta)[0])
            # self.marks = current_marks # backtrack to prior state
            # self.makeMove(action[0]+1, action[1]+1, ' ')
            self.marks[action[0]][action[1]] = ' '
            GenGameBoard.depth = GenGameBoard.depth - 1
            if utility_value <= -(10 ** self.board_size):
                GenGameBoard.utility_min = GenGameBoard.utility_min + 1
                return utility_value
            if utility_value <= alpha:
                GenGameBoard.num_pruned = GenGameBoard.num_pruned + 1
                return utility_value

            # Set the MIN utility value (beta)
            beta = min(beta, utility_value)
        return utility_value


def main():
    """ Runs the main program for the game. """

    # Print out the header info
    print('Artificial Intelligence')
    print('MP2: Alpha/Beta Search for Generalized Tic-Tac-Toe')
    print('SEMESTER: FALL 2021, TERM 1')
    print('NAME: ALISON MAJOR\n')

    # Define constants
    LOST = 0  # pylint: disable=invalid-name
    WON = 1   # pylint: disable=invalid-name
    DRAW = 2  # pylint: disable=invalid-name

    # wrongInput = False
    # Get the board size from the user
    board_size = int(input("Please enter the size of the board n (e.g. n=3,4,5,...): "))

    # Create the game board of the given size and print it
    board = GenGameBoard(board_size)
    board.print_board()

    # Start the game loop
    while True:
        # *** Player's move ***

        # Try to make the move and check if it was possible
        # If not possible get col,row inputs from player
        row, col = -1, -1
        while not board.make_move(row, col, 'X'):
            print("Player's Move")
            row, col = input("Choose your move (row, column): ").split(',')
            row = int(row)
            col = int(col)

        # Display the board again
        board.print_board()

        # Check for ending condition
        # If game is over, check if player won and end the game
        if board.check_for_win('X'):
            # Player won
            result = WON
            break
        elif board.no_more_moves():
            # No moves left -> draw
            result = DRAW
            break

        # *** Computer's move ***
        board.make_computer_move()

        # Print out the board again
        board.print_board()

        # Check for ending condition
        # If game is over, check if computer won and end the game
        if board.check_for_win('O'):
            # Computer won
            result = LOST
            break
        elif board.no_more_moves():
            # No moves left -> draw
            result = DRAW
            break

    # Check the game result and print out the appropriate message
    print("GAME OVER")
    if result == WON:
        print("You Won!")
    elif result == LOST:
        print("You Lost!")
    else:
        print("It was a draw!")


if __name__ == "__main__":
    main()
