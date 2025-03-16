import requests
import json
import itertools
import ai_algorithm
from ai_algorithm import ai_decide

class QuoridorGame:
    """
    A class to represent the Quoridor game.

    Attributes:
        api_url (str): The URL for the API used to interact with the game state and control actions.

    Methods:
        get_game_state(): Retrieves the current game state from the API.
        make_move(player, move_type, move): Makes a move (either player move or wall placement).
        restart_game(): Resets the game to its initial state via the API.
        display_board(game_state): Displays the current board state in a readable format.
        human_turn(player): Prompts the human player for their move and processes the input.
        ai_turn(player, strategies): Makes a move for the AI based on the selected strategies.
        run_game(): Runs the main game loop, allowing the user to play against the AI.
    """

    def __init__(self, api_url):
        """
        Initializes the QuoridorGame object with the provided API URL.

        Args:
            api_url (str): The base URL for the API that manages game interactions.
        """
        self.api_url = api_url

    def get_game_state(self):
        """
        Retrieves the current game state from the API.

        Returns:
            dict: The current game state, including player positions, board state, and turn information.
        """
        response = requests.get(f"{self.api_url}/state")
        return response.json() if response.status_code == 200 else None

    def make_move(self, player, move_type, move):
        """
        Makes a move, either moving a player or placing a wall.

        Args:
            player (int): The player number (1 or 2).
            move_type (str): The type of move ('move' or 'wall').
            move (str or tuple): The move details, either a direction or coordinates for wall placement.

        Returns:
            dict: The response from the API indicating the success or failure of the move.
        """
        if move_type == "move":
            data = {"type": "move", "direction": move}
            response = requests.post(f"{self.api_url}/move", json=data)
        elif move_type == "wall":
            x, y, orientation = move
            data = {"type": "wall", "x": x, "y": y, "orientation": orientation}
            response = requests.post(f"{self.api_url}/wall", json=data)
        else:
            return {"error": "Invalid move type"}

        return response.json() if response.status_code == 200 else {"error": "Request failed"}

    def restart_game(self):
        """
        Restarts the game by resetting the state through the API.

        Returns:
            dict: The response from the API confirming the game restart.
        """
        response = requests.post(f"{self.api_url}/restart")
        return response.json() if response.status_code == 200 else {"error": "Failed to restart game"}

    def display_board(self, game_state):
        """
        Displays the current game board in a readable format.

        Args:
            game_state (dict): The current game state, including the board configuration.
        """
        board = game_state.get("board", [])
        for row in board:
            print(" ".join(row))
        print()

    def human_turn(self, player):
        """
        Handles the human player's turn, prompting for input and making the move.

        Args:
            player (int): The player number (1 or 2) for the human player.
        """
        valid_move = False
        while not valid_move:
            move_type = input("Enter move type (move/wall): ").strip()
            move = input("Enter move coordinates (e.g., 'U' or '3 4 H'): ").strip()
            move_data = move.split()

            if move_type == "move" and len(move_data) == 1:
                move = move_data[0]
            elif move_type == "wall" and len(move_data) == 3:
                move = (int(move_data[0]), int(move_data[1]), move_data[2].upper())
            else:
                print("Invalid input format. Try again.")
                continue

            response = self.make_move(player, move_type, move)
            if response.get("success"):
                valid_move = True
            else:
                print("Invalid move. Try again.")

    def ai_turn(self, player, strategies):
        """
        Handles the AI's turn by deciding the best move based on the selected strategies.

        Args:
            player (int): The player number (1 or 2) for the AI.
            strategies (tuple): The selected strategies for the AI (e.g., ('minimax', 'astar')).

        Returns:
            str: The best move determined by the AI, based on the selected strategies.
        """
        state = self.get_game_state()
        best_move = ai_decide(strategies, state)  # Pass the selected strategies to the AI decision function
        return best_move

    def run_game(self):
        """
        Runs the main game loop, allowing the user to play against the AI.

        The loop includes:
        - Strategy selection for the AI.
        - Displaying the current game board.
        - Handling turns for the human player and the AI.
        - Checking for a winner.
        """
        print("Starting Quoridor...\n")

        # Generate all possible combinations of strategies
        STRATEGIES = ['minimax', 'mcts', 'astar']
        all_combinations = []
        for r in range(1, len(STRATEGIES) + 1):
            all_combinations.extend(itertools.combinations(STRATEGIES, r))
        
        # Print available combinations
        print("Select an AI strategy (or combination):")
        for idx, combo in enumerate(all_combinations):
            print(f"{idx + 1}: {', '.join(combo)}")
        
        # Get user input for strategy selection
        selected_idx = int(input(f"Enter a number between 1 and {len(all_combinations)}: ")) - 1
        selected_strategy = all_combinations[selected_idx]

        print(f"Selected strategy: {', '.join(selected_strategy)}")

        player_turn = 1
        while True:
            game_state = self.get_game_state()
            if not game_state:
                print("Failed to retrieve game state.")
                break
            
            self.display_board(game_state)
            if game_state.get("winner"):
                print(f"Player {game_state['winner']} wins!")
                break
            
            if player_turn == 1:
                print("Your turn!")
                self.human_turn(player_turn)
            else:
                print(f"AI's turn with strategy {', '.join(selected_strategy)}...")
                ai_move = self.ai_turn(player_turn, selected_strategy)  # AI makes a move
                print(f"AI moved: {ai_move}")
            
            player_turn = 3 - player_turn  # Switch between player 1 and 2

if __name__ == "__main__":
    # The URL of the API that manages the game state and controls
    API_URL = "http://127.0.0.1:8000"
    game = QuoridorGame(API_URL)
    game.run_game()
