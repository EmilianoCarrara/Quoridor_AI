class Cell:
    def __init__(self):
        self.occupant = "empty"
        self.directions = {"U": True, "D": True, "L": True, "R": True}

class Board:
    def __init__(self):
        self.grid = [[Cell() for _ in range(9)] for _ in range(9)]
        self.set_borders()
        self.grid[0][4].occupant = "player2"
        self.grid[8][4].occupant = "player1"

    def set_borders(self):
        for x in range(9):
            self.grid[x][0].directions["L"] = False
            self.grid[x][8].directions["R"] = False
        for y in range(9):
            self.grid[0][y].directions["U"] = False
            self.grid[8][y].directions["D"] = False

class QuoridorGame:
    DIRECTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

    def __init__(self):
        self.board = Board()
        self.walls = []
        self.player_positions = {"player1": (8, 4), "player2": (0, 4)}
        self.turn = "player1"

    def switch_turn(self):
        self.turn = "player2" if self.turn == "player1" else "player1"

    def move_player(self, direction):
        x, y = self.player_positions[self.turn]
        dx, dy = self.DIRECTIONS[direction]
        nx, ny = x + dx, y + dy

        if not (0 <= nx < 9 and 0 <= ny < 9):
            return False
        if not self.board.grid[x][y].directions[direction]:
            return False
        if self.board.grid[nx][ny].occupant != "empty":
            return False

        self.board.grid[x][y].occupant = "empty"
        self.board.grid[nx][ny].occupant = self.turn
        self.player_positions[self.turn] = (nx, ny)
        return True

    def place_wall(self, x, y, orientation):
        if orientation == 'H':
            if y >= 8 or x >= 8:
                return False
            self.board.grid[x][y].directions['D'] = False
            self.board.grid[x][y+1].directions["D"] = False
            self.board.grid[x+1][y].directions["U"] = False
            self.board.grid[x+1][y+1].directions["U"] = False
        elif orientation == 'V':
            if x >= 8 or y >= 8:
                return False
            self.board.grid[x][y].directions["R"] = False
            self.board.grid[x+1][y].directions["R"] = False
            self.board.grid[x][y+1].directions["L"] = False
            self.board.grid[x+1][y+1].directions["L"] = False
        self.walls.append((x, y, orientation))
        return True

    def check_win(self):
        p1_x, _ = self.player_positions["player1"]
        p2_x, _ = self.player_positions["player2"]
        if p1_x == 0:
            return "player1"
        elif p2_x == 8:
            return "player2"
        return None

    def game_state(self):
        return {
            "player_positions": self.player_positions,
            "walls": self.walls,
            "turn": self.turn,
            "board": [[[cell.occupant, cell.directions] for cell in row] for row in self.board.grid]
        }
