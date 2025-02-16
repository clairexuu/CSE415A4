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
import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin=twin
        self.nickname = 'ZTC'
        if twin: self.nickname += '2'
        self.long_name = 'Zara the Cat'
        if twin: self.long_name += ' II'
        self.persona = 'agressive'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "don't know yet" # e.g., "X" or "O".
        self.alpha_beta_cutoffs_this_turn = -1
        self.num_static_evals_this_turn = -1
        self.zobrist_table_num_entries_this_turn = -1
        self.zobrist_table_num_hits_this_turn = -1
        self.current_game_type = None

    def introduce(self):
        intro = '\nMy name is Zara the Cat.\n'+\
            'Claire Xu and Ziwen Chen made me.\n'+\
            'Their netIDs are xinyix26 and zchen56.\n'
        if self.twin: intro += "By the way, I'm the TWIN.\n"
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1, # Time limits can be
                                      # changed mid-game by the game master.

        utterances_matter=True):      # If False, just return 'OK' for each utterance,
                                      # or something simple and quick to compute
                                      # and do not import any LLM or special APIs.
                                      # During the tournament, this will be False.
       if utterances_matter:
           pass
           # Optionally, import your LLM API here.
           # Then you can use it to help create utterances.
           
       # Write code to save the relevant information in variables
       # local to this instance of the agent.
       # Game-type info can be in global variables.
       print("Change this to return 'OK' when ready to test the method.")
       return "Not-OK"
   
    # The core of your agent's ability should be implemented here:             
    def make_move(self, current_state, current_remark, time_limit=1000,
                  autograding=False, use_alpha_beta=True,
                  use_zobrist_hashing=False, max_ply=3,
                  special_static_eval_fn=None):
        print("make_move has been called")

        possibleMoves = successors_and_moves(state)
        myMove = chooseMove(possibleMoves)
        myUtterance = self.nextUtterance()
        newState, newMove = myMove

        if not autograding:
            return [[newMove, newState], myUtterance]

        stats = [self.alpha_beta_cutoffs_this_turn,
                 self.num_static_evals_this_turn,
                 self.zobrist_table_num_entries_this_turn,
                 self.zobrist_table_num_hits_this_turn]

        return [[newMove, newState] + stats, myUtterance]

    # The main adversarial search function:
    def minimax(self,
            state,
            depth_remaining,
            pruning=False,
            alpha=None,
            beta=None):
        print("Calling minimax. We need to implement its body.")

        default_score = 0 # Value of the passed-in state. Needs to be computed.
    
        return [default_score, "my own optional stuff", "more of my stuff"]
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 

    def static_eval(self, state, game_type=None):
        # Values should be higher when the states are better for X,
        # lower when better for O.
        k = game_type.k  # k in a row/column/diagonal to win
        board = state.board
        rows, cols = len(board), len(board[0])
        game_name = game_type.short_name  # amount of work depend on type of game

        # Precompute valid positions
        if game_name == "5-in-a-Row":
            valid_positions = {(r, c) for r in range(rows) for c in range(cols) if not is_forbidden_corner(r, c)}
        elif game_name == "Cassini":
            valid_positions = {(r, c) for r in range(rows) for c in range(cols) if not is_saturn_region(r, c)}
        else:
            valid_positions = {(r, c) for r in range(rows) for c in range(cols)}

        def count_lines(player, k_needed):
            # Count the number of open sequences of length k_needed for a given player
            count = 0
            for r, c in valid_positions:
                if board[r][c] == player:  # Only check from positions occupied by the player
                    count += check_directions(r, c, player, k_needed)
            return count

        def check_directions(r, c, player, k_needed):
            # Checks sequences in four directions: horizontal, vertical,
            #                                      lower-left to upper-right,  and upper-left to lower-right
            directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Down, right, diagonal-right, diagonal-left
            count = 0
            for dr, dc in directions:
                sequence = []
                for i in range(k):
                    nr, nc = r + i * dr, c + i * dc
                    if (nr, nc) in valid_positions and 0 <= nr < rows and 0 <= nc < cols:
                        sequence.append(board[nr][nc])
                    else:
                        break
                if (len(sequence) == k and
                    sequence.count(player) == k_needed and
                    ('X' if player == 'O' else 'O') not in sequence):
                    count += 1
            return count

        def compute_eval(player, k):
            # Compute evaluation of a state for a player by the following rule:
            #   count_lines of i items in an open enough row/column/diagonal * 10 ** (i-1) for 1 <= i <= k
            sum = 0
            for i in range(1, k+1):
                sum += count_lines(player, i) * 10 ** (i-1)
            return sum

        # return eval of X - eval of O so that value is larger when state better for X, smaller when state better for O
        return compute_eval('X', k) - compute_eval('O', k)

def is_forbidden_corner(r, c):
    # check if a position is in the forbidden corner in FIAR
    return (r, c) in {(0, 0), (0, 6), (6, 0), (6, 6)}

def is_saturn_region(r, c):
    # check if a position is in saturn in Cassini
    return (r, c) in {(2, 3), (2, 4), (4, 3), (4, 4), (3, 2), (3, 3), (3, 4), (3, 5)}
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

