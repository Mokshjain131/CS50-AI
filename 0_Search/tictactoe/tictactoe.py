"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    X plays first.
    any value is acceptable if terminal board is provided.
    """
    # starting_state = initial_state()
    # if board == starting_state:
    #     return X

    # if terminal(board):
    #     return O

    moves = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] is not None:
                moves += 1

    if moves % 2 == 0:
        return X
    else:
        return O

    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    returns any value if terminal board is provided.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i,j))

    if len(actions) == 0:
        actions.add((1,1))

    return actions

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if (board[action[0]][action[1]] is not EMPTY) or ((action[0] > 2 or action[0] < 0) or (action[1] > 2 or action[1] < 0)):
        raise Exception("Invalid move")

    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board

    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    if there is a tie or the game is in progress it will return None.
    """
    if ((board[0][0] == board[0][1] == board[0][2]) or (board[0][0] == board[1][0] == board[2][0]) or (board[0][0] == board[1][1] == board[2][2])) and board[0][0] is not None:
        return board[0][0]

    elif ((board[0][2] == board[1][1] == board[2][0]) or (board[0][1] == board[1][1] == board[2][1]) or (board[1][0] == board[1][1] == board[1][2])) and board[1][1] is not None:
        return board[1][1]

    elif ((board[0][2] == board[1][2] == board[2][2]) or (board[2][0] == board[2][1] == board[2][2])) and board[2][2] is not None:
        return board[2][2]

    else:
        return None

    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is None:
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    return False
        return True

    else:
        return True

    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

    # raise NotImplementedError

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        best_val = -2
        best_action = None

        for action in actions(board):
            val = recursion(result(board, action))
            if val > best_val:
                best_val = val
                best_action = action

        return best_action

    if player(board) == O:
        best_val = 2
        best_action = None

        for action in actions(board):
            val = recursion(result(board, action))
            if val < best_val:
                best_val = val
                best_action = action

        return best_action

def recursion(board):
    if terminal(board):
        return utility(board)

    if player(board) == X:
        v = -2
        for action in actions(board):
            v = max(v, recursion(result(board, action)))
        return v

    if player(board) == O:
        v = 2
        for action in actions(board):
            v = min(v, recursion(result(board, action)))
        return v

    # raise NotImplementedError
