from ..model.game import GameDTO
from .board_mapper import WebBoardMapper
from domain.model.game import Game
from uuid import UUID


class WebGameMapper:
    @staticmethod
    def to_domain(dto: GameDTO) -> Game:
        return Game(UUID(dto.uuid), WebBoardMapper.to_domain(dto.board))

    @staticmethod
    def to_dto(domain: Game) -> GameDTO:
        return GameDTO(str(domain.uuid), WebBoardMapper.to_dto(domain.board))