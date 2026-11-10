from ..mapper.game_mapper import GameMapper
from ..model.game import GameEntity
from ..model.board import BoardEntity
from domain.model.game import Game
from domain.model.board import Board


class GameRepository:
    def __init__(self, storage):
        self.storage = storage

    def save(self, game: Game) -> None:
        self.storage.put(game.uuid, GameMapper.to_entity(game))

    def find_by_id(self, uuid) -> Game | None:
        entity = self.storage.get(uuid)
        return GameMapper.to_domain(entity) if entity else None

    def create(self, uuid) -> Game:
        empty = Board([[0,0,0],[0,0,0],[0,0,0]])
        game = Game(uuid, empty)
        self.save(game)
        return game