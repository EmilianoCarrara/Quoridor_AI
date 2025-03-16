import random
from queue import PriorityQueue
from copy import deepcopy

# A* Search (Heuristic)
def a_star(board, start, goal_rows):
    """
    Implements the A* pathfinding algorithm to find the shortest path.

    Args:
        board (list): The current game board.
        start (tuple): The starting position on the board.
        goal_rows (list): The goal rows (either row 0 or 8).

    Returns:
        int: The cost of the shortest path to the goal.
    """
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        _, current = frontier.get()
        if current[0] in goal_rows:
            return cost_so_far[current]

        for direction, allowed in board[current[0]][current[1]][1].items():
            if allowed:
                dx, dy = {"U":(-1,0),"D":(1,0),"L":(0,-1),"R":(0,1)}[direction]
                next_cell = (current[0]+dx, current[1]+dy)
                if 0 <= next_cell[0] < 9 and 0 <= next_cell[1] < 9:
                    new_cost = cost_so_far[current] + 1
                    if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                        cost_so_far[next_cell] = new_cost
                        priority = new_cost + abs(goal_rows[0]-next_cell[0])
                        frontier.put((priority, next_cell))
    return float('inf')

# Heuristic evaluation
def heuristic(state):
    """
    Evaluates the desirability of a game state using A* pathfinding to determine distances.

    Args:
        state (dict): The current game state.

    Returns:
        int: The difference between the AI's path and the opponent's path.
    """
    ai_path = a_star(state["board"], state["player_positions"]["player1"], [0])
    opponent_path = a_star(state["board"], state["player_positions"]["player2"], [8])
    return opponent_path - ai_path

# Minimax with Alpha-Beta Pruning
def minimax(state, depth, alpha, beta, maximizing):
    """
    Implements the Minimax algorithm with Alpha-Beta Pruning to evaluate moves.

    Args:
        state (dict): The current game state.
        depth (int): The depth of the search tree.
        alpha (float): The alpha value for pruning.
        beta (float): The beta value for pruning.
        maximizing (bool): A flag indicating whether we are maximizing or minimizing.

    Returns:
        tuple: The evaluation score and the best move.
    """
    if depth == 0 or state["winner"]:
        return heuristic(state), None

    best_move = None
    moves = ['U', 'D', 'L', 'R']
    
    if maximizing:
        max_eval = float('-inf')
        for move_dir in moves:
            new_state = deepcopy(state)
            eval, _ = minimax(new_state, depth-1, alpha, beta, False)
            if eval > max_eval:
                max_eval, best_move = eval, move_dir
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move_dir in moves:
            new_state = deepcopy(state)
            eval, _ = minimax(new_state, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, None

# Monte Carlo Tree Search (MCTS)
def mcts(state, simulations=100):
    """
    Implements the Monte Carlo Tree Search (MCTS) to evaluate moves.

    Args:
        state (dict): The current game state.
        simulations (int): The number of simulations to run.

    Returns:
        str: The best move based on the simulations.
    """
    moves = ['U', 'D', 'L', 'R']
    scores = {move: 0 for move in moves}
    
    for move in moves:
        for _ in range(simulations):
            simulated_state = deepcopy(state)
            if simulated_state["winner"] == "player1":
                scores[move] += 1
            elif simulated_state["winner"] == "player2":
                scores[move] -= 1
    
    best_move = max(scores, key=scores.get)
    return best_move

# Main AI Decision function
def ai_decide(strategies, state):
    """
    Decides the best move for the AI based on the selected combination of strategies.
    The AI evaluates each move based on the combination of Minimax, A*, and MCTS.

    Args:
        strategies (tuple): A tuple of selected strategies (e.g., ('minimax', 'astar')).
        state (dict): The current game state.

    Returns:
        str: The best move selected based on the combined strategies.


    ALL THE ALGORITHMS NEED TO BE REVIEWED AND THE ACTUAL STRATEGY TO SELECT THE BEST NEXT MOVE DEPENDING ON THE COMBINATION OF STRATEGIES HAS YET TO BE DEFINED
    """
