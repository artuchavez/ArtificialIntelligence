# MIT 6.034 Lab 3: Games
# Written by Dylan Holmes (dxh), Jessica Noss (jmn), and 6.034 staff

from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    # check if vertical win exists
    height = board.num_cols
    width = board.num_rows
    if board.count_pieces() == height * width:
        return True
    chains = board.get_all_chains(current_player=None)
    for each in chains:
        if len(each) >= 4:
            return True
    return False


def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    if is_game_over_connectfour(board):
        return []
    possible_boards = []
    for x in range(board.num_cols):
        if board.is_column_full(x):
            continue
        else:
            new_board = board.add_piece(x)
            possible_boards.append(new_board)
    return possible_boards

def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    chains_1 = board.get_all_chains(current_player=is_current_player_maximizer)
    chains_2 = board.get_all_chains(current_player= not(is_current_player_maximizer))
    for chain in chains_1:
        if len(chain) == 4:
            return 1000
    for chain in chains_2:
        if len(chain) == 4:
            return -1000
    return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    chains_1 = board.get_all_chains(current_player=is_current_player_maximizer)
    chains_2 = board.get_all_chains(current_player= not(is_current_player_maximizer))
    for chain in chains_1:
        if len(chain) >= 4:
            return 1100 - board.count_pieces()
    for chain in chains_2:
        if len(chain) >= 4:
            return -1100 + board.count_pieces()
    return 0

def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    chains_1 = board.get_all_chains(current_player=is_current_player_maximizer)
    chains_2 = board.get_all_chains(current_player= not(is_current_player_maximizer))
    chain_1_count = 0
    max_chain_1 = 0
    for chain in chains_1:
        chain_1_count += len(chain)
        if len(chain) > max_chain_1:
            max_chain_1 = len(chain)
    avg_chain_1 = chain_1_count / len(chains_1)
    chain_2_count = 0
    max_chain_2 = 0
    for chain in chains_2:
        chain_2_count += len(chain)
        if len(chain) > max_chain_2:
            max_chain_2 = len(chain)
    avg_chain_2 = chain_2_count / len(chains_2)

    if is_current_player_maximizer:
        next_mover = 1
    else:
        next_mover = -1

    score = 50 * next_mover + 100 * (max_chain_1 - max_chain_2) + 200 * (avg_chain_1 - avg_chain_2) + 100 * (len(chains_1) - len(chains_2))
    return score

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

count = 0

def dfs_maximizing(state) :
    """Performs depth-first search to find path with highest endgame score.
    Returns a tuple containing:
     0. the best path (a list of AbstractGameState objects),
     1. the score of the leaf node (a number), and
     2. the number of static evaluations performed (a number)"""
    answer = []
    global count
    if state.is_game_over():
        part_score = state.get_endgame_score()
        count +=1
        return ([state], part_score, None)
    else:
        for next_state in state.generate_next_states():
            partial_answer = dfs_maximizing(next_state)
            if partial_answer != None:
                path = [state] + partial_answer[0]
                answer.append((path, partial_answer[1], partial_answer[2]))
        if answer != []:
            final = max(answer, key=lambda x:x[1])
            return (final[0], final[1], count)
    return None

count1 = 0

def minimax_endgame_search(state, maximize) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    def max_search(state, count):
        score = -INF
        if state.is_game_over():
            return [state], state.get_endgame_score(True), count+1
        for new_state in state.generate_next_states():
            new_path, new_value, count = min_search(new_state, count)
            if new_value > score:
                score = new_value
                path = new_path
        path.append(state)
        return (path, score, count)

    def min_search(state, count):
        score = INF
        if state.is_game_over():
            return [state], state.get_endgame_score(False), count+1
        for new_state in state.generate_next_states():
            new_path, new_value, count = max_search(new_state, count)
            if new_value < score:
                score = new_value
                path = new_path
        path.append(state)
        return (path, score, count)

    count = 0
    if maximize:
        path, score, count = max_search(state, count)
        path.reverse()
        return path, score, count
    else:
        path, score, count = min_search(state, count)
        path.reverse()
        return path, score, count



def mini_endgame_search(state, count):
    if state.is_game_over():
        return [state], state.get_endgame_score(False), count+1

    best_value = INF

    for new_state in state.generate_next_states():

        new_path, new_value, count = mini_endgame_search(new_state, count)

        if new_value < best_value:
            best_value = new_value
            best_path = new_path

    best_path.append(state)
    return (best_path, best_value, count)




# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER, True))

count2 = 0

def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True, new=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."
    global count2
    final = []
    answer = []

    if new == True:
        count2 = 0

    if state.is_game_over():
        count2 += 1
        return ([state], state.get_endgame_score(maximize), None)

    if depth_limit > 0:
        for next_state in state.generate_next_states():
            partial_answer = minimax_search(next_state, heuristic_fn, depth_limit-1, not maximize, False)
            if partial_answer != None:
                path = [state]+partial_answer[0]
                answer.append((path, partial_answer[1], partial_answer[2]))
    else:
        count2 += 1
        answer.append(([state], heuristic_fn(state.get_snapshot(), maximize), None))

    if maximize == True:
        final = max(answer, key=lambda x:x[1])
        return (final[0], final[1], count2)

    else:
        final = min(answer, key=lambda x:x[1])
        return (final[0], final[1], count2)
    return None



# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1.  Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))

def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    count = 0
    #specific for maximize == False
    def min_ab(state, depth, alpha, beta, heuristic_fn, count):
        path = []
        if state.is_game_over():
            return [state], state.get_endgame_score(False), count+1
        elif depth == 0:
            return [state], heuristic_fn(state.get_snapshot(), False), count+1

        for next_state in state.generate_next_states():
            new_depth = depth -1
            new_path, new_beta, count = max_ab(next_state, new_depth, alpha, beta, heuristic_fn, count)
            if beta > new_beta:
                path = new_path
                beta = new_beta
            if alpha >= beta:
                return path, beta, count
        path.append(state)
        return path, beta, count

    #specific for maximize == True
    def max_ab(state, depth, alpha, beta, heuristic_fn, count):
        path = []
        if state.is_game_over():
            return [state], state.get_endgame_score(True), count+1
        elif depth == 0:
            return [state], heuristic_fn(state.get_snapshot(), True), count+1

        for next_state in state.generate_next_states():
            new_depth = depth - 1
            new_path, new_alpha, count = min_ab(next_state, new_depth, alpha, beta, heuristic_fn, count)
            if alpha < new_alpha:
                path = new_path
                alpha = new_alpha
            if alpha >= beta:
                return path, alpha, count
        path.append(state)
        return path, alpha, count



    if not maximize:
        path, score, count = min_ab(state, depth_limit, alpha, beta, heuristic_fn, count)
        path.reverse()
        return path, score, count

    else:
        path, score, count = max_ab(state, depth_limit, alpha, beta, heuristic_fn, count)
        path.reverse()
        return path, score, count


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))



def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.

    depth = 1
    while depth_limit >= depth:
        answer = minimax_search_alphabeta(state, -(INF), INF, heuristic_fn, depth, maximize)
        depth += 1
        anytime_value.set_value(answer)

    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#print progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4)


##### PART 3: Multiple Choice ##################################################

ANSWER_1 = '4'

ANSWER_2 = '1'

ANSWER_3 = '4'

ANSWER_4 = '5'


#### SURVEY ###################################################

NAME = 'Arturo Chavez-Gehrig'
COLLABORATORS = 'Luana Lopes Lara'
HOW_MANY_HOURS_THIS_LAB_TOOK = '7'
WHAT_I_FOUND_INTERESTING = 'connect 4'
WHAT_I_FOUND_BORING = 'coding the arbitrary game tree searches was hard'
SUGGESTIONS = ''
