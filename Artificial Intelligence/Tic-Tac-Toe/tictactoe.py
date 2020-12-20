"""""""""""""""""""""""""""""""""""""""""""""""
Tic Tac Toe AI Player using Alpha-beta pruning
"""""""""""""""""""""""""""""""""""""""""""""""
import math
import numpy
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

# Empty game board
def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Check diagonal
def get_diagonal(board):
    return [[board[0][0], board[1][1], board[2][2], # diagonal 1
            board[0][2], board[1][1], board[2][0]]] # diagonal 2

# Check columns
def get_columns(board):
    columns = []
    for i in range(3):
        columns.append([row[i] for row in board])
    return columns

# Check if three in a row
def three_in_row(row):
    return True if row.count(row[0]) == 3 else False

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = 0
    count_o = 0

    for i in board: # for each row in board
        for j in i: # for cell in row
            if(j=="X"):
                count_x = count_x+1
            if(j=="O"):
                count_o = count_o+1
    return O if count_x > count_o else X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i, row in enumerate(board):
        for j, vall in enumerate(row):
            if (vall==EMPTY):
                action.add((i, j))
    return action

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action
    if(board[i][j] != EMPTY):
        raise Exception("Invalid move")
    next_move = player(board)
    deep_board = deepcopy(board)
    deep_board[i][j] = next_move
    return deep_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    rows = board+get_diagonal(board)+get_columns(board)
    for row in rows:
        current_player = row[0]
        if current_player is not None and three_in_row(row):
            return current_player
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    person = winner(board)
    if (person is not None):
        return True
    if (all(all(j!=EMPTY for j in i) for i in board)):
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    person = winner(board)
    if (person == X):
        return 1
    elif (person == O):
        return -1
    else:
        return 0

def max_alpha_beta(board, alpha, beta):
    if (terminal(board)==True):
        return (utility(board), None)
    vall = float("-inf")
    best = None
    for action in actions(board):
        min_val = min_alpha_beta(result(board, action), alpha, beta)[0]
        # Aplha-Beta Pruning
        if (min_val > vall):
            best = action
            vall = min_val
        alpha=max(alpha,vall)
        if (beta <= alpha):
            break
    return (vall, best)

def min_alpha_beta(board, alpha, beta):
    if (terminal(board)==True):
        return (utility(board), None)
    vall = float("inf")
    best = None
    for action in actions(board):
        max_val = max_alpha_beta(result(board, action), alpha, beta)[0]
        # Aplha-Beta Pruning
        if (max_val < vall):
            best = action
            vall = max_val
        beta = min(beta,vall)
        if (beta <= alpha):
            break
    return (vall, best)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if (player(board)==X): # Maximize for player 'X'
        return max_alpha_beta(board, float("-inf"), float("inf"))[1]
    if (player(board)==O): # Minimize for player 'O'
        return min_alpha_beta(board, float("-inf"), float("inf"))[1]
    else:
        raise Exception("Error")
