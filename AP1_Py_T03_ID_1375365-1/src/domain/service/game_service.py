from abc import ABC, abstractmethod
from uuid import UUID
from ..model.game import Game

class GameService(ABC):
    @abstractmethod
    def create_game(self, uuid: UUID) -> Game: ...

    @abstractmethod
    def make_move(self, game: Game) -> Game: ...

    @abstractmethod
    def validate_board(self, game: Game) -> bool: ...

    @abstractmethod
    def is_finished(self, board) -> bool: ...