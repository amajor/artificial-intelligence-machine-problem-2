[![Unit Tests](https://github.com/amajor/artificial-intelligence-machine-problem-2/actions/workflows/python-test.yml/badge.svg)](https://github.com/amajor/artificial-intelligence-machine-problem-2/actions/workflows/python-test.yml)
[![Pylint](https://github.com/amajor/artificial-intelligence-machine-problem-2/actions/workflows/pylint.yml/badge.svg)](https://github.com/amajor/artificial-intelligence-machine-problem-2/actions/workflows/pylint.yml)

# Artificial Intelligence 
## Machine Problem 2 – Alpha/Beta Search for Generalized Tic-Tac-Toe

### Introduction
For this assignment, you will implement the minimax algorithm with alpha-beta pruning in order to find the optimal move 
for a game of generalized tic-tac-toe. In this version of the game, the players can choose different board sizes, for 
example 4x4 or 5x5, instead of the normal 3x3. The game proceeds with the usual rules for tic-tac-toe 
(see https://en.wikipedia.org/wiki/Tic-tac-toe).

### Requirements
You are to modify the mp2_basecode program to implement the alpha-beta search for making the computer’s move. 
This will require implementing additional methods for testing for terminal states and finding the utility of states, 
among others. You can follow the textbook’s pseudocode for the algorithm.

#### Additional Requirements

1. The name of your source code file should be `mp2.py`. All your code should be within a single file.
2. You can only import `numpy`, `random`, and `math` packages.
3. Your code should follow good coding practices, including good use of whitespace and use of both inline and block
comments.
4. You need to use meaningful identifier names that conform to standard naming conventions.
5. At the top of each file, you need to put in a block comment with the following information: 
   1. your name, 
   2. date, 
   3. course name, 
   4. semester, 
   5. and assignment name.

### HINTS

It’s easiest to use the backtracking method. That is, instead of generating hypothetical states, just apply the moves to 
the game board, compute the utility, and then backtrack the move. This requires that you save the current board 
configuration before trying each move, so you can backtrack it later. 