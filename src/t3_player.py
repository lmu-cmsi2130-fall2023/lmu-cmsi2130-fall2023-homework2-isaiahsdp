"""
Artificial Intelligence responsible for playing the game of T3!
Implements the alpha-beta-pruning mini-max search algorithm
"""
from dataclasses import *
from typing import *
from t3_state import *
    
def choose(state: "T3State") -> Optional["T3Action"]:
    """
    Main workhorse of the T3Player that makes the optimal decision from the max node
    state given by the parameter to play the game of Tic-Tac-Total.
    
    [!] Remember the tie-breaking criteria! Moves should be selected in order of:
    1. Best utility
    2. Smallest depth of terminal
    3. Earliest move (i.e., lowest col, then row, then move number)
    
    You can view tiebreaking as something of an if-ladder: i.e., only continue to
    evaluate the depth if two candidates have the same utility, only continue to
    evaluate the earliest move if two candidates have the same utility and depth.
    
    Parameters:
        state (T3State):
            The board state from which the agent is making a choice. The board
            state will be either the odds or evens player's turn, and the agent
            should use the T3State methods to simplify its logic to work in
            either case.
    
    Returns:
        Optional[T3Action]:
            If the given state is a terminal (i.e., a win or tie), returns None.
            Otherwise, returns the best T3Action the current player could take
            from the given state by the criteria stated above.
    """ 

    # [!] TODO! Implement alpha-beta-pruning minimax search!
    if state.is_win() or state.is_tie():
        return None
    _, best_action = minimax(state, 0, (float('-inf'), 0), (float('inf'), 0), True)
    return best_action

# [Optional / Suggested] TODO! Add any helper methods or dataclasses needed to
# manage the alpha-beta-pruning minimax operation

def minimax(t3state: "T3State", depth: int, alpha: Tuple[float, int], beta: Tuple[float, int], isMaxPlayer: bool) -> Tuple[Tuple[float, int], Optional["T3Action"]]:
    if isMaxPlayer: # max turn
        if t3state.is_win():
            return (-1, -depth), None
        if t3state.is_tie():
            return (0, -depth), None
        else:
            best_val: Tuple[float, int] = (float('-inf'), 0)

    else: # min turn
        if t3state.is_win():
            return (1, depth), None
        if t3state.is_tie():
            return (0, depth), None
        else:
            best_val = (float('inf'), 0)
    best_action = None

    for action, next_state in t3state.get_transitions():
        if next_state.is_win():
            if isMaxPlayer:
                return (1, depth), action
            else:
                return (-1, depth), action
    
    for action, next_state in t3state.get_transitions(): 
        util_value, _ = minimax(next_state, depth+1, alpha, beta, not isMaxPlayer)
        if isMaxPlayer: #max turn
            if util_value[0] > best_val[0] or (util_value[0] == best_val[0] and util_value[1] < best_val[1]): #tie breaker
                best_val = util_value
                best_action = action
            if util_value[0] > alpha[0] or (util_value[0] == alpha[0] and util_value[1] < alpha[1]):
                alpha = util_value
        else: #min turn
            if util_value[0] < best_val[0] or (util_value[0] == best_val[0] and util_value[1] < best_val[1]):
                best_val = util_value
                best_action = action
            if util_value[0] < beta[0] or (util_value[0] == beta[0] and util_value[1] < beta[1]):
                beta = util_value

        if alpha[0] >= beta[0]: #prunes if a worse or equal solution is found
            break

    return ((best_val), best_action)

