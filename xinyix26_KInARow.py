'''
xinyix26_KInARow.py
Authors: Xu, Claire; Chen, Ziwen

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 415, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

AUTHORS = 'Claire Xu and Ziwen Chen'

from agent_base import KAgent
from game_types import State, Game_Type
import time  # You'll probably need this to avoid losing a


# game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent (KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__ (self, twin=False):
        self.twin = twin
        self.nickname = 'ZTC'
        if twin: self.nickname += '2'
        self.long_name = 'Zara the Cat'
        if twin: self.long_name += ' II'
        self.persona = 'agressive'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "X"  # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

    def introduce (self):
        intro = '\nMy name is Zara the Cat.\n' + \
                'Claire Xu and Ziwen Chen made me.\n' + \
                'Their netIDs are xinyix26 and zchen56.\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare (
            self,
            game_type,
            what_side_to_play,
            opponent_nickname,
            expected_time_per_move=0.1,  # Time limits can be
            # changed mid-game by the game master.

            utterances_matter=True):  # If False, just return 'OK' for each utterance,
        # or something simple and quick to compute
        # and do not import any LLM or special APIs.
        # During the tournament, this will be False.

        self.current_game_type = game_type

        if utterances_matter:
            pass
            # Optionally, import your LLM API here.
            # Then you can use it to help create utterances.

        # Write code to save the relevant information in variables
        # local to this instance of the agent.
        # Game-type info can be in global variables.
        # print ("Change this to return 'OK' when ready to test the method.")
        return "OK"

    # The core of your agent's ability should be implemented here:             
    def make_move (self, current_state, current_remark, time_limit=1000,
                   autograding=False, use_alpha_beta=True,
                   use_zobrist_hashing=False, max_ply=3,
                   special_static_eval_fn=None):
        # print ("make_move has been called")

        # 清空回合记数
        self.alpha_beta_cutoffs_this_turn = 0
        self.num_static_evals_this_turn = 0
        self.zobrist_table_num_entries_this_turn = 0
        self.zobrist_table_num_hits_this_turn = 0


        myMove = self.chooseMove (current_state)
        myUtterance = self.nextUtterance ()
        newState, newMove = myMove



        if not autograding:
            return [[newMove, newState], myUtterance]

        stats = [self.alpha_beta_cutoffs_this_turn,
                 self.num_static_evals_this_turn,
                 self.zobrist_table_num_entries_this_turn,
                 self.zobrist_table_num_hits_this_turn]


        # 根据 se 的次数来调用特殊计数
        for i in range(self.num_static_evals_this_turn):
            special_static_eval_fn(current_state)

        return [[newMove, newState] + stats, myUtterance]

    def nextUtterance (self):
        return "Meow " * 10

    def chooseMove (self, state):
        # minmax_info = self.minimax(state, 2, False ,float('-inf'), float('inf'))
        minmax_info = self.minimax (state, 2)
        return [minmax_info[2], minmax_info[1]]

    # The main adversarial search function:
    def minimax (self,
                 state,
                 depth_remaining,
                 pruning=False,
                 alpha=None,
                 beta=None):
        # print("Calling minimax. We need to implement its body.")

        # Base case: if the depth is 0 or the game is over, return the evaluation of the state
        if depth_remaining == 0 or state.finished == True:
            return [self.static_eval(state, game_type=self.current_game_type), "this is the end", "ennnnnd"]



        best_move = None
        best_state = None

        if state.whose_move == "X":  # Maximizing

            if alpha is not None:
                max_eval = alpha
            else:
                max_eval = float ('-inf')

            for move in self.get_possible_moves (state):
                new_state = self.apply_move (state, move)
                eval_score, _, _ = self.minimax (new_state, depth_remaining - 1, pruning, alpha, beta)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                    best_state = new_state

                if pruning:
                    alpha = max (alpha, eval_score)
                    if beta <= alpha:

                        # 计数
                        self.alpha_beta_cutoffs_this_turn += 1

                        break  # Beta cut-off

            return [max_eval, best_move, best_state]

        else:  # Minimizing player

            if beta is not None:
                min_eval = beta
            else:
                min_eval = float ('inf')

            for move in self.get_possible_moves (state):
                new_state = self.apply_move (state, move)
                eval_score, _, _ = self.minimax (new_state, depth_remaining - 1, pruning, alpha, beta)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    best_state = new_state

                if pruning:
                    beta = min (beta, eval_score)
                    if beta <= alpha:

                        # 计数
                        self.alpha_beta_cutoffs_this_turn += 1

                        break  # Alpha cut-off

            return [min_eval, best_move, best_state]

        # return [default_score, "my own optional stuff", "more of my stuff"]
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc.

    def static_eval (self, state, game_type=None):
        # static evaluation function.
        # Given a game state, it returns a numeric evaluation of that state
        # where a higher value means that the state is better for X and a lower value is a state better for O.

        # 计数
        self.num_static_evals_this_turn += 1


        k = game_type.k  # k in a row/column/diagonal to win
        board = state.board
        rows, cols = len (board), len (board[0])
        game_name = game_type.short_name  # amount of work depend on type of game

        # Get valid positions in the board
        if game_name == "5-in-a-Row":
            valid_positions = {(r, c) for r in range (rows) for c in range (cols) if not is_forbidden_corner (r, c)}
        elif game_name == "Cassini":
            valid_positions = {(r, c) for r in range (rows) for c in range (cols) if not is_saturn_region (r, c)}
        else:
            valid_positions = {(r, c) for r in range (rows) for c in range (cols)}

        # TODO: to make it faster, mark row/col/dia that's already checked?

        def count_lines (player, num_pieces):
            # Count the number of open enough hor/ver/dia_up/dia_down sequence with exactly num_pieces of player
            count = 0
            for r, c in valid_positions:
                if board[r][c] == player:  # Only check from positions occupied by the player
                    count += check_directions (r, c, player, num_pieces)
            return count

        def check_directions (r, c, player, num_pieces):
            # Checks open enough sequences in four directions
            # open enough means there's enough empty space (no player, no other player, and valid)
            #                   to form a sequence of length k
            directions = {'hor': get_board_row (r, board),
                          'ver': get_board_col (c, board),
                          'dia_up': get_board_dia_up (r, c, board),
                          'dia_down': get_board_dia_down (r, c, board)}
            count = 0

            for dir_name, dir_elements in directions.items ():
                # for the diagonals, skip diagonals shorter than k
                if len (dir_elements) < k:
                    break

                # Step 1: check if the current direction has exact num_pieces of player
                if dir_elements.count (player) == num_pieces:
                    # Step 2: check if there's enough empty space
                    consecutive_sequence = 0  # need at least k
                    for item in dir_elements:
                        if item == "" or item == player:
                            consecutive_sequence += 1
                        else:  # we meet other player or an obstacle
                            consecutive_sequence = 0

                        if consecutive_sequence >= k:
                            count += 1
                            break

            return count

        def compute_eval (player, k):
            # Compute evaluation of a state for a player by the following rule:
            #   count_lines of i items in an open enough row/column/diagonal * 10 ** (i-1) for 1 <= i <= k
            sum = 0
            for i in range (1, k + 1):
                sum += count_lines (player, i) * (10 ** (i - 1))
            return sum

        # return eval of X - eval of O so that value is larger when state better for X, smaller when state better for O
        return compute_eval ('X', k) - compute_eval ('O', k)







    def get_possible_moves (self, state):
        """
        Returns a list of all possible moves in the current state.
        A move is represented as a tuple (row, col).
        """
        possible_moves = []
        for row in range (len (state.board)):
            for col in range (len (state.board[0])):
                if state.board[row][col] == ' ':  # Empty spot
                    possible_moves.append ((row, col))
        return possible_moves

    def apply_move (self, state, move):
        """
        Applies a move to the board and returns a new state.

        Parameters:
        - state: The current game state.
        - move: A tuple (row, col) representing the move.

        Returns:
        - A new State object with the move applied.
        """
        row, col = move
        new_state = State (old=state)  # Copy the current state
        new_state.board[row][col] = state.whose_move  # Place the current player's mark
        new_state.change_turn ()  # Switch turns

        # Check if the game is finished (win condition needs implementation)
        new_state.finished = self.check_win (new_state, row, col)

        return new_state

    def check_win (self, state, last_row, last_col):
        """
        Checks if placing a move at (last_row, last_col) results in a win.
        This should be implemented based on the game rules (e.g., K-in-a-Row).
        """
        k = self.current_game_type.k  # 获取游戏类型对应的 k 值
        player = state.board[last_row][last_col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, Horizontal, Diagonal /

        for dr, dc in directions:
            count = 1  # Include the current move
            for sign in (-1, 1):  # Check both forward and backward
                r, c = last_row + sign * dr, last_col + sign * dc
                while 0 <= r < len (state.board) and 0 <= c < len (state.board[0]) and state.board[r][c] == player:
                    count += 1
                    if count >= k:  # Win condition met
                        return True
                    r += sign * dr
                    c += sign * dc

        return False  # No win detected


# Helper Functions

def is_forbidden_corner (r, c):
    # check if a position is in the forbidden corner in FIAR
    return (r, c) in {(0, 0), (0, 6), (6, 0), (6, 6)}


def is_saturn_region (r, c):
    # check if a position is in saturn in Cassini
    return (r, c) in {(2, 3), (2, 4), (4, 3), (4, 4), (3, 2), (3, 3), (3, 4), (3, 5)}


# Figure out who the other player is.
# For example, other("X") = "O"
def other (p):
    if p == 'X': return 'O'
    return 'X'


def get_board_col (j, board):
    # return the column j of the board
    if j < 0 or j > len (board[0]):
        raise Exception ("No such Column in this game board")
    column = []
    for i in range (len (board)):
        column.append (board[i][j])
    return column


def get_board_row (i, board):
    # return the row i of the board
    if i < 0 or i > len (board):
        raise Exception ("No such Row in this game board")
    return board[i]


def get_board_dia_up (i, j, board):
    # return the lower-left to upper-right diagonal of the board containing (i, j)
    n = len (board)  # Number of rows
    m = len (board[0])  # Number of columns
    diag_sum = i + j  # constant along the lower-left to upper-right diagonal
    diagonal = []

    for r in range (n):  # for every row
        c = diag_sum - r  # compute column index
        if 0 <= c < m:  # if in the board
            diagonal.append (board[r][c])
    return diagonal


def get_board_dia_down (i, j, board):
    # return the upper-left to lower-right diagonal of the board containing (i, j)
    n = len (board)  # Number of rows
    m = len (board[0])  # Number of columns
    diag_diff = i - j  # constant along the upper-left to lower-right diagonal
    diagonal = []

    for r in range (n):  # for every row
        c = r - diag_diff  # compute column index
        if 0 <= c < m:  # if in the board
            diagonal.append (board[r][c])
    return diagonal

# OPTIONAL THINGS TO KEEP TRACK OF:

# WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances
