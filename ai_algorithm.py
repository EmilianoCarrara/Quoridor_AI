import requests
import random
from queue import PriorityQueue

BASE_URL = "http://127.0.0.1:8000"

# Define available strategies
STRATEGIES = ['minimax', 'mcts', 'astar']

# Get game state from the API
def get_game_state():
    return requests.get(f"{BASE_URL}/state").json()

# Send a move to the API
def send_move(direction):
    return requests.post(f"{BASE_URL}/move", json={"direction": direction}).json()

# Send a wall placement to the API
def send_wall(x, y, orientation):
    return requests.post(f"{BASE_URL}/wall", json={"x": x, "y": y, "orientation": orientation}).json()

# A* Search (Heuristic)
def a_star(board, start, goal_rows):
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
    ai_path = a_star(state["board"], state["player_positions"]["player1"], [0])
    opponent_path = a_star(state["board"], state["player_positions"]["player2"], [8])
    return opponent_path - ai_path

# Minimax with Alpha-Beta Pruning
def minimax(state, depth, alpha, beta, maximizing):
    if depth == 0 or state["winner"]:
        return heuristic(state), None

    best_move = None
    moves = ['U', 'D', 'L', 'R']

    if maximizing:
        max_eval = float('-inf')
        for move_dir in moves:
            new_state = send_move(move_dir)["game_state"]
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
            new_state = send_move(move_dir)["game_state"]
            eval, _ = minimax(new_state, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, None

# Simple Monte Carlo Tree Search (MCTS)
def simple_mcts_move():
    return random.choice(['U', 'D', 'L', 'R'])

# Main AI Decision function
def ai_decide(strategy, state):
    if strategy == 'minimax':
        _, best_move = minimax(state, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=True)
        return best_move
    elif strategy == 'mcts':
        return simple_mcts_move()
    elif strategy == 'astar':
        moves = ['U', 'D', 'L', 'R']
        best_score = float('inf')
        best_move = None
        for move_dir in moves:
            simulated_state = send_move(move_dir)["game_state"]
            score = a_star(simulated_state["board"], simulated_state["player_positions"]["player1"], [0])
            if score < best_score:
                best_score, best_move = score, move_dir
        return best_move
    else:
        return random.choice(['U', 'D', 'L', 'R'])

# Game loop
def main(strategy='minimax'):
    while True:
        state = get_game_state()
        if state['turn'] == 'player1':
            move = ai_decide(strategy, state)
            result = send_move(move)
            print(f"AI ({strategy}) moved {move}")
            if result['winner']:
                print(f"Winner is {result['winner']}!")
                break
        else:
            print("Waiting for opponent...")

if __name__ == "__main__":
    selected_strategy = input(f"Select AI strategy {STRATEGIES}: ")
    if selected_strategy not in STRATEGIES:
        selected_strategy = 'minimax'
    main(strategy=selected_strategy)
