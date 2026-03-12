"""
Tic Tac Toe — Minimax AI with debug tracing
"""

import math
import sys
from colorama import init
init()

# Force debug output to the real terminal (bypasses Tkinter stdout)
if not sys.stdout.isatty():
    sys.stdout = open('/dev/tty', 'w')



X = "X"
O = "O"
EMPTY = None

DEBUG = True  # Set to False to disable debug output


def print_board(board, indent=0):
    """
    Pretty-print the board with optional indentation.
    """
    prefix = " " * indent
    symbols = {X: "X", O: "O", EMPTY: "."}
    for row in board:
        print(prefix + " ".join(symbols[cell] for cell in row))
    print()


def initial_state():
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    return {
        (i, j)
        for i in range(3)
        for j in range(3)
        if board[i][j] == EMPTY
    }


def result(board, action):
    i, j = action

    if board[i][j] != EMPTY:
        raise Exception("Invalid action: cell is not empty.")

    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    # Rows
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]

    # Columns
    for col in range(3):
        if (
            board[0][col]
            == board[1][col]
            == board[2][col]
            != EMPTY
        ):
            return board[0][col]

    # Diagonals
    if (
        board[0][0]
        == board[1][1]
        == board[2][2]
        != EMPTY
    ):
        return board[0][0]

    if (
        board[0][2]
        == board[1][1]
        == board[2][0]
        != EMPTY
    ):
        return board[0][2]

    return None


def terminal(board):
    if winner(board) is not None:
        return True
    return all(EMPTY not in row for row in board)


def utility(board):
    win = winner(board)
    return 1 if win == X else -1 if win == O else 0


def max_value(board, depth=0):
    if terminal(board):
        u = utility(board)
        if DEBUG:
            print(" " * depth + f"max_value: terminal board, utility = {u}")
            print_board(board, indent=depth)
        return u

    v = -math.inf
    if DEBUG:
        print(" " * depth + "max_value: evaluating board")
        print_board(board, indent=depth)

    for action in actions(board):
        if DEBUG:
            print(" " * depth + f"max_value: trying action {action}")
        new_board = result(board, action)
        score = min_value(new_board, depth + 2)
        if DEBUG:
            print(" " * depth + f"max_value: action {action} -> score {score}")
        v = max(v, score)

    if DEBUG:
        print(" " * depth + f"max_value: returning {v}")
    return v


def min_value(board, depth=0):
    if terminal(board):
        u = utility(board)
        if DEBUG:
            print(" " * depth + f"min_value: terminal board, utility = {u}")
            print_board(board, indent=depth)
        return u

    v = math.inf
    if DEBUG:
        print(" " * depth + "min_value: evaluating board")
        print_board(board, indent=depth)

    for action in actions(board):
        if DEBUG:
            print(" " * depth + f"min_value: trying action {action}")
        new_board = result(board, action)
        score = max_value(new_board, depth + 2)
        if DEBUG:
            print(" " * depth + f"min_value: action {action} -> score {score}")
        v = min(v, score)

    if DEBUG:
        print(" " * depth + f"min_value: returning {v}")
    return v


def minimax(board):
    if terminal(board):
        if DEBUG:
            print("minimax: terminal board, no moves")
            print_board(board)
        return None

    current = player(board)

    if DEBUG:
        print(f"minimax: current player = {current}")
        print_board(board)

    if current == X:
        best_score = -math.inf
        best_move = None

        for action in actions(board):
            if DEBUG:
                print(f"minimax (X): considering action {action}")
            score = min_value(result(board, action), depth=2)
            if DEBUG:
                print(f"minimax (X): action {action} -> score {score}")
            if score > best_score:
                best_score = score
                best_move = action

        if DEBUG:
            print(f"minimax (X): best_move = {best_move}, best_score = {best_score}")
        return best_move

    else:  # current == O
        best_score = math.inf
        best_move = None

        for action in actions(board):
            if DEBUG:
                print(f"minimax (O): considering action {action}")
            score = max_value(result(board, action), depth=2)
            if DEBUG:
                print(f"minimax (O): action {action} -> score {score}")
            if score < best_score:
                best_score = score
                best_move = action

        if DEBUG:
            print(f"minimax (O): best_move = {best_move}, best_score = {best_score}")
        return best_move


    '''
if __name__ == "__main__":
    board = initial_state()
    print("Best move from initial state:")
    print(minimax(board))
    '''
