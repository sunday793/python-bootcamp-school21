from ..model.game import GameEntity
from domain.model.game import Game
from .board_mapper import BoardMapper


class GameMapper:
    @staticmethod
    def to_domain(entity: GameEntity) -> Game:
        return Game(entity.uuid, BoardMapper.to_domain(entity.board))

    @staticmethod
    def to_entity(domain: Game) -> GameEntity:
        return GameEntity(domain.uuid, BoardMapper.to_entity(domain.board))