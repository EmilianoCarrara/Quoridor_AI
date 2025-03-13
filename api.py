from fastapi import FastAPI
from models import Move, WallPlacement
from game_logic import QuoridorGame

app = FastAPI()

# Inizializza il gioco
game = QuoridorGame()

@app.get("/state")
def get_game_state():
    return game.game_state()

@app.post("/move")
def move(move: Move):
    success = game.move_player(move.direction)
    winner = game.check_win()
    if success:
        game.switch_turn()
    return {"success": success, "winner": winner, "game_state": game.game_state()}

@app.post("/wall")
def place_wall(wall: WallPlacement):
    success = game.place_wall(wall.x, wall.y, wall.orientation)
    if success:
        game.switch_turn()
    return {"success": success, "game_state": game.game_state()}

# Esegui il server API usando il comando:
# uvicorn api:app --reload