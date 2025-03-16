from fastapi import FastAPI
from models import MoveRequest
from game_logic import QuoridorGame

app = FastAPI()
game = QuoridorGame()

@app.get("/state")
def get_game_state():
    """Returns the current game state including board, players, and remaining walls."""
    return game.game_state()

@app.post("/move")
def move(move: MoveRequest):
    """Handles a player move request."""
    success = game.move_player(move.direction)
    if success:
        winner = game.check_win()
        game.switch_turn()
        return {"success": success, "winner": winner, "game_state": game.game_state()}
    return {"success": False, "error": "Invalid move", "game_state": game.game_state()}

@app.post("/wall")
def place_wall(wall: MoveRequest):
    """Handles a wall placement request."""
    success = game.place_wall(wall.x, wall.y, wall.orientation)
    if success:
        game.switch_turn()
        return {"success": success, "game_state": game.game_state()}
    return {"success": False, "error": "Invalid wall placement", "game_state": game.game_state()}

@app.post("/restart")
def restart_game():
    """Resets the game to its initial state."""
    global game
    game = QuoridorGame()
    return {"success": True, "message": "Game restarted", "game_state": game.game_state()}