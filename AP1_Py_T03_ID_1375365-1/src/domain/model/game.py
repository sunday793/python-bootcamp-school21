from uuid import UUID
from .board import Board


class Game:
    """Game model."""
    def __init__(self, game_id: UUID, board: Board):
        self.uuid = game_id
        self.board = board
