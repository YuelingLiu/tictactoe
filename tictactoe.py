import math
import copy

# Use these constants to fill in the game board
X = "X"
O = "O"
EMPTY = None


def start_state():
    """
    Returns starting state of the board.

    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    #

    Returns which player (either X or O) who has the next turn on a board.

    In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
    Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    """
    count_x = 0
    count_o = 0

    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_x += 1
            elif board[i][j] == O:
                count_o += 1

    if count_x > count_o:

        return O
    else:
        return X


def actions(board):
    """
    Returns the set of all possible actions (i, j) available on the board.

    The actions function should return a set of all the possible actions that can be taken on a given board.
    Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2)
    and j corresponds to the column of the move (also 0, 1, or 2).

    Possible moves are any cells on the board that do not already have an X or an O in them.

    Any return value is acceptable if a terminal board is provided as input.
    """
    # initializing a set to store all the possible actions  i and j
    possible_actions = set()

    # iterate the board and checking if this cell is none
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


# def is_board_filled(board):
#     for row in range(3):
#         for col in range(3):
#             if board[row][col] is None:
#                 return False
#
#     return True


def succ(board, action):
    """
    Returns the board that results from making move (i, j) on the board, without modifying the original board.

    If `action` is not a valid action for the board, you  should raise an exception.

    The returned board state should be the board that would result from taking the original input board, and letting
    the player whose turn it is make their move at the cell indicated by the input action.

    Importantly, the original board should be left unmodified. This means that simply updating a cell in `board` itself
    is not a correct implementation of this function. You’ll likely want to make a deep copy of the board first before
    making any changes.
    """
    if terminal(board):
        raise Exception("Game is terminated ")
    elif action not in actions(board):
        raise Exception("not a valid move")
    else:
        # taking i j from action
        (i, j) = action
        new_board = copy.deepcopy(board)
        new_board[i][j] = player(board)
        # print("checking new board", new_board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.

    - If the X player has won the game, the function should return X.
    - If the O player has won the game, the function should return O.
    - If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the
      function should return None.

    You may assume that there will be at most one winner (that is, no board will ever have both players with
    three-in-a-row, since that would be an invalid board state).
    """
    # winning condition in row, col and diagonals
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != EMPTY:
            return board[row][0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]

    # checking diagonals and only two possibilities
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]

    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != EMPTY:
        return board[2][0]

    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.

    If the game is over, either because someone has won the game or because all cells have been filled without anyone
    winning, the function should return True.

    Otherwise, the function should return False if the game is still in progress.
    """
    # 1 checking if someone has won the GAME calling winner function
    # 2 checking if board is filled. call is_board_filled function
    if winner(board) or isTie(board):
        return True

    return False


def isTie(board):

    empty_spot= (len(board) * len(board[0]))
    for i in range(3):
        for j in range(3):
            if board[i][j] is not EMPTY:
                empty_spot -= 1
    return empty_spot == ~0

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.

    You may assume utility will only be called on a board if terminal(board) is True.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == 0:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board.

    If multiple moves are equally optimal, any of those moves is acceptable.

    If the board is a terminal board, the minimax function should return None.
    """

    if terminal(board):
        return None

    max_v = float("-inf")
    min_v = float("inf")

    if player(board) == X:
        # return the optimal move from max_value
        return max_value(board, max_v, min_v)[1]
    else:
        return min_value(board, max_v, min_v)[1]

def max_value(board, maximum, minimum):
    move = None
    if terminal(board):
        return [utility(board), None];
    v = float('-inf')
    for action in actions(board):
        # to get the value only
        eval = min_value(succ(board, action), maximum, minimum)[0]
        maximum = max(maximum, eval)
        if eval > v:
            v = eval
            move = action
        if maximum >= minimum:
            break
    print("checking v at the end of max_value function and move---", v, move)
    return [v,move]

def min_value(board, maximum, minimum):
    move = None
    if terminal(board):
        return [utility(board), None];

    v = float('inf')
    for action in actions(board):
        print("checking the acton in min_value", action)

        # getting the first element of the result from max_value,which is the
        # max value it is self
        eval = max_value(succ(board, action), maximum, minimum)[0]
        minimum = min(minimum, eval)
        if eval < v:
            v = eval
            move = action
        if maximum >= minimum:
            break
    return [v, move]


