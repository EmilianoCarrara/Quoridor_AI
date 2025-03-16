from pydantic import BaseModel

class MoveRequest(BaseModel):
    """
    A Pydantic model to define the request body for a move or wall placement.

    Attributes:
        type (str): The type of move ("move" for player moves or "wall" for wall placements).
        direction (str): The direction for a player move (e.g., 'U', 'D', 'L', 'R') (optional for wall).
        x (int): The x-coordinate for wall placement (optional).
        y (int): The y-coordinate for wall placement (optional).
        orientation (str): The orientation of the wall ('H' for horizontal, 'V' for vertical) (optional).
    """
    type: str  # "move" or "wall"
    direction: str = None  # Used if type is "move"
    x: int = None  # Used if type is "wall"
    y: int = None  # Used if type is "wall"
    orientation: str = None  # "H" or "V" if type is "wall"
    