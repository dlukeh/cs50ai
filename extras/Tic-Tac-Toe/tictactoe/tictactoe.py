"""
Tic Tac Toe Player
"""
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """ 
    Returns the starting empty 3×3 board. 
    """

    return [

        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],

    ]


def player(board):
    """
    Returns the player whose turn it is.
    'X' moves first; players alternate.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

    
def actions(board):
    """
    Returns a set of all available moves (i, j) on the board.
    """
    return { 
        (i, j) 
        for i in range(3) 
        for j in range(3) 
        if board[i][j] == EMPTY 
    }


def result(board, action):
    i, j = action

    # Check bounds
    if i not in range(3) or j not in range(3):
        raise Exception("Invalid action")

    # Check if cell is empty
    if board[i][j] != EMPTY:
        raise Exception("Invalid action")

    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game: X, O, or None 
    """
    # Rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
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
    
    if (board[0][2] 
            == board[1][1] 
            == board[2][0] 
            != EMPTY
            ):
        return board[0][2]
    
    return None


def terminal(board): 
    """
    Returns True if the game is over (win or full board). 
    """ 
    if winner(board) is not None: 
        return True 
    return all(EMPTY not in row for row in board)


def utility(board): 
    """
      Returns: 1 if X has won, 
      -1 if O has won,
       0 otherwise. 
    """ 
    win = winner(board) 
    return 1 if win == X else -1 if win == O else 0


def max_value(board):
    """ 
    Recursive helper for minimax. 
    Returns the best achievable score for X. 
    """
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board): 
    """ 
    Recursive helper for minimax. Returns the best achievable score for O. 
    """ 
    if terminal(board): 
        return utility(board) 
    
    v = math.inf 
    for action in actions(board): 
        v = min(v, max_value(result(board, action))) 
    return v


def minimax(board): 
    """ 
    Returns the optimal move for the current player. 
    If the game is over, returns None. 
    """ 
    if terminal(board): 
        return None 
    
    current = player(board) 
    
    if current == X: 
        best_score = -math.inf 
        best_move = None 
        
        for action in actions(board): 
            score = min_value(result(board, action)) 
            if score > best_score: 
                best_score = score 
                best_move = action 
                
        return best_move 
    
    else:  # current == O 
        best_score = math.inf 
        best_move = None 
        
        for action in actions(board): 
            score = max_value(result(board, action)) 
            if score < best_score: 
                best_score = score 
                best_move = action 
                
        return best_move 
