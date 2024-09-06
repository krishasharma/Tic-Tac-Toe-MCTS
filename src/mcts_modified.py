from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log
from timeit import default_timer as time

explore_faction = 2.

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until the end criterion are met.
    e.g. find the best expandable node (node with untried action) if it exist,
    or else a terminal node

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node

    """
    while not board.is_ended(state) and node.untried_actions == []:
        if not node.child_nodes:
            return node, state
        node = max(node.child_nodes.values(), key=lambda n: ucb(n, board.current_player(state) != bot_identity))
        state = board.next_state(state, node.parent_action)
    return node, state

def expand_leaf(node: MCTSNode, board: Board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node (if it is non-terminal).

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:
        node: The added child node
        state: The state associated with that node

    """
    action = choice(node.untried_actions)
    next_state = board.next_state(state, action)
    child_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(next_state))
    node.child_nodes[action] = child_node
    node.untried_actions.remove(action)
    return child_node, next_state

def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.
    
    Returns:
        state: The terminal game state

    """
    while not board.is_ended(state):
        legal_actions = board.legal_actions(state)
        action = heuristic_action_choice(board, state, legal_actions)
        state = board.next_state(state, action)
    return state

def heuristic_action_choice(board, state, legal_actions):
    """ Choose the action based on simple heuristics."""
    # Prioritize winning moves
    for action in legal_actions:
        next_state = board.next_state(state, action)
        if board.points_values(next_state) is not None:
            return action
    # Prioritize blocking opponent's winning moves
    for action in legal_actions:
        next_state = board.next_state(state, action)
        opponent = 3 - board.current_player(state)
        if board.points_values(next_state) is not None and is_win(board, next_state, opponent):
            return action
    # Fallback to random choice
    return choice(legal_actions)

def backpropagate(node: MCTSNode, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node is not None:
        node.visits += 1
        node.wins += won
        node = node.parent
        won = not won

def ucb(node: MCTSNode, is_opponent: bool):
    """ Calcualtes the UCB value for the given node from the perspective of the bot

    Args:
        node:   A node.
        is_opponent: A boolean indicating whether or not the last action was performed by the MCTS bot
    Returns:
        The value of the UCB function for the given node
    """
    if node.visits == 0:
        return float('inf')
    win_rate = node.wins / node.visits
    if is_opponent:
        win_rate = 1 - win_rate
    return win_rate + explore_faction * sqrt(log(node.parent.visits) / node.visits)

def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree

    Args:
        root_node:   The root node
    Returns:
        action: The best action from the root node
    
    """
    return max(root_node.child_nodes.items(), key=lambda child: child[1].visits)[0]

def is_win(board: Board, state, identity_of_bot: int):
    # checks if state is a win state for identity_of_bot
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def think(board: Board, current_state, time_limit=1.0):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state

    """
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    start_time = time()
    while time() - start_time < time_limit:
        state = current_state
        node = root_node

        # Traverse
        node, state = traverse_nodes(node, board, state, bot_identity)

        # Expand
        if not board.is_ended(state):
            node, state = expand_leaf(node, board, state)

        # Rollout
        end_state = rollout(board, state)

        # Backpropagate
        won = is_win(board, end_state, bot_identity)
        backpropagate(node, won)

    best_action = get_best_action(root_node)
    return best_action