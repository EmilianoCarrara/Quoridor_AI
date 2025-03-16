class Cell:
    """
    Represents a single cell in the game board.
    
    Attributes:
        occupant (str): The occupant of the cell, either "empty" or a player ("player1" or "player2").
        directions (dict): A dictionary representing the available directions the player can move.
                           The keys are directions ('U', 'D', 'L', 'R') and values are booleans indicating if movement in that direction is allowed.
    """

    def __init__(self):
        """
        Initializes a cell with no occupant and all directions enabled.
        """
        self.occupant = "empty"
        self.directions = {"U": True, "D": True, "L": True, "R": True}


class Board:
    """
    Represents the game board, which consists of a 9x9 grid of cells.
    
    Attributes:
        grid (list of list of Cell): A 9x9 grid representing the board, where each cell is an instance of the Cell class.

    Methods:
        set_borders(): Sets the borders of the board, disallowing movement outside the grid.
    """

    def __init__(self):
        """
        Initializes the board with a 9x9 grid and sets up the borders.
        The starting positions of the players are set in the middle of the top and bottom rows.
        """
        self.grid = [[Cell() for _ in range(9)] for _ in range(9)]
        self.set_borders()
        self.grid[0][4].occupant = "player2"
        self.grid[8][4].occupant = "player1"

    def set_borders(self):
        """
        Sets the borders of the board, disallowing movement outside the grid.
        Specifically, it disables movement in the leftmost and rightmost columns, 
        and the topmost and bottommost rows.
        """
        for x in range(9):
            self.grid[x][0].directions["L"] = False
            self.grid[x][8].directions["R"] = False
        for y in range(9):
            self.grid[0][y].directions["U"] = False
            self.grid[8][y].directions["D"] = False


class QuoridorGame:
    """
    Represents the Quoridor game, including the game state, player positions, and wall placements.

    Attributes:
        DIRECTIONS (dict): A dictionary mapping direction keys ('U', 'D', 'L', 'R') to changes in coordinates.
        board (Board): The game board, an instance of the Board class.
        walls (list): A list of placed walls, represented as tuples of coordinates and orientation.
        player_positions (dict): A dictionary storing the positions of both players.
        turn (str): The current player's turn, either 'player1' or 'player2'.

    Methods:
        switch_turn(): Switches the turn between the two players.
        move_player(direction): Moves the current player in the specified direction, if possible.
        place_wall(x, y, orientation): Places a wall at the specified position and orientation, blocking movement.
        check_win(): Checks if either player has won by reaching the opposite side of the board.
        game_state(): Returns the current game state, including player positions, walls, the current turn, and the board.
    """

    DIRECTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def __init__(self):
        """
        Initializes the game with an empty board, player positions, and the starting player turn.
        Player 1 starts at the bottom center of the board and player 2 starts at the top center.
        """
        self.board = Board()
        self.walls = []
        self.player_positions = {"player1": (8, 4), "player2": (0, 4)}
        self.turn = "player1"

    def switch_turn(self):
        """
        Switches the current turn between player 1 and player 2.
        """
        self.turn = "player2" if self.turn == "player1" else "player1"

    def move_player(self, direction):
        """
        Moves the current player in the specified direction if the move is valid.

        Args:
            direction (str): The direction to move ('U', 'D', 'L', or 'R').

        Returns:
            bool: True if the move is successful, False if the move is invalid (out of bounds or blocked).
        """
        x, y = self.player_positions[self.turn]
        dx, dy = self.DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        # Check if the move is within bounds
        if not (0 <= nx < 9 and 0 <= ny < 9):
            return False
        # Check if the direction is allowed
        if not self.board.grid[x][y].directions[direction]:
            return False
        # Check if the destination is empty
        if self.board.grid[nx][ny].occupant != "empty":
            return False

        # Update the player's position and the board state
        self.board.grid[x][y].occupant = "empty"
        self.board.grid[nx][ny].occupant = self.turn
        self.player_positions[self.turn] = (nx, ny)
        return True

    def place_wall(self, x, y, orientation):
        """
        Places a wall at the specified coordinates and orientation, blocking movement.

        Args:
            x (int): The x-coordinate of the wall's starting position.
            y (int): The y-coordinate of the wall's starting position.
            orientation (str): The orientation of the wall ('H' for horizontal, 'V' for vertical).

        Returns:
            bool: True if the wall is placed successfully, False if the placement is invalid (out of bounds).
        """
        if orientation == 'H':
            if y >= 8 or x >= 8:
                return False
            # Block the vertical movement between the two cells
            self.board.grid[x][y].directions['D'] = False
            self.board.grid[x][y+1].directions["D"] = False
            self.board.grid[x+1][y].directions["U"] = False
            self.board.grid[x+1][y+1].directions["U"] = False
        elif orientation == 'V':
            if x >= 8 or y >= 8:
                return False
            # Block the horizontal movement between the two cells
            self.board.grid[x][y].directions["R"] = False
            self.board.grid[x+1][y].directions["R"] = False
            self.board.grid[x][y+1].directions["L"] = False
            self.board.grid[x+1][y+1].directions["L"] = False
        # Add the wall to the list of placed walls
        self.walls.append((x, y, orientation))
        return True

    def check_win(self):
        """
        Checks if either player has won the game.

        Returns:
            str: The winner, either "player1" or "player2", or None if no winner yet.
        """
        p1_x, _ = self.player_positions["player1"]
        p2_x, _ = self.player_positions["player2"]
        if p1_x == 0:
            return "player1"
        elif p2_x == 8:
            return "player2"
        return None

    def game_state(self):
        """
        Returns the current game state, including player positions, walls, the current turn, and the board.

        Returns:
            dict: A dictionary representing the current game state.
        """
        return {
            "player_positions": self.player_positions,
            "walls": self.walls,
            "turn": self.turn,
            "board": [[[cell.occupant, cell.directions] for cell in row] for row in self.board.grid]
        }
