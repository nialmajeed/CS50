import math
import copy

X = "X"
O = "O"
EMPTY = None


# I feel like I should include NODE to keep track of the states
""""
class board():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
"""


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x_count += 1
            if board[i][j] == O:
                o_count += 1

    if x_count == o_count:
        return X
    else:
        return O

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    legal_actions = set()
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if item == EMPTY:
                legal_actions.append((i, j))
            elif item == X or O:
                pass
            else:
                raise NotImplementedError

    return legal_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    legal_actions = actions(board)
    player_turn = player(board)
    # Creating a copy of the board  - not updating till finishing minmax analysis
    updated_board = copy.deepcopy(board)

    # need to check the action provided is within the legal actios
    for tuple in legal_actions:
        if tuple == action:
            legal_action = action

            # updating the board with the legal action based on the player X or O
            updated_board[legal_action[0]][legal_action[1]] = player_turn
            return updated_board
    else:
        raise Exception("Please pick an open tile")

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.

    """
    winner_b = copy.deepcopy(board)

    for i, row in enumerate(winner_b):
        for j, item in enumerate(row):
            if item == EMPTY:
                winner_b[i][j] = 0
            elif item == X:
                winner_b[i][j] = 1
            elif item == O:
                winner_b[i][j] = -1
            else:
                raise NotImplementedError

    for col in zip(*winner_b):
        if sum(col) == -3:
            return O
        elif sum(col) == -3:
            return O
        else:
            continue

    for row in winner_b:
        if sum(row) == -3:
            return O
        elif sum(row) == -3:
            return O
        else:
            continue

    column_0 = 0
    column_1 = 0
    column_2 = 0
    for row in winner_b:
        column_0 += row[0]
        column_1 += row[1]
        column_2 += row[2]

    if (winner_b[0][0] + winner_b[1][1] + winner_b[2][2]) == 3:
        return X
    elif (winner_b[0][0] + winner_b[1][1] + winner_b[2][2]) == -3:
        return O
    elif (winner_b[2][0] + winner_b[1][1] + winner_b[0][2]) == 3:
        return X
    elif (winner_b[2][0] + winner_b[1][1] + winner_b[0][2]) == -3:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win = winner(board)
    # if win == X or win == O:
    if win in (X, O):
        return True
    # need to fix if there is an empty we cant have it return true
    elif any(EMPTY in row for row in board) == True:
        return False
    else:
        return True

    raise NotImplementedError


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

    raise NotImplementedError


def min_value(board):
    if terminal(board) == True:
        return utility(board)

    value = -math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value


def max_value(board):
    if terminal(board) == True:
        return utility(board)

    value = math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # check if the game is over or not
    terminal_board = terminal(board)

    if terminal_board == True:
        return None

    elif player(board) == X:
        options = []

        for action in actions(board):
            tally = min_value(result(board, action))
            # Store options in list
            options.append([tally, action])
        # Return highest value action

    elif player(board) == O:
        options = []

        for action in actions(board):
            tally = max_value(result(board, action))
            # Store options in list
            options.append([tally, action])
        # Return highest value action
        return sorted(options, reverse=True)[0][1]

    # Get initial state (board)
    # Identify how many options there are (add to frontier) BDS or DFS
    #   This would be done by identifying the frontier
    # for each level identify the minvalue = -1,0 or 1
    # optiamise to always get
    # Target X =1, O=-1 and None = 0


# ==================
board = initial_state()
action = (0, 0)

R = result(board, action)
W = winner(R)
t = terminal(R)
U = utility(R)
MM = minimax(R)

print(MM)
