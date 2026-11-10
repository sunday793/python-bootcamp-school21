from ..model.board import BoardEntity
from domain.model.board import Board


class BoardMapper:
    @staticmethod
    def to_domain(entity: BoardEntity) -> Board:
        return Board([row[:] for row in entity.cells])

    @staticmethod
    def to_entity(domain: Board) -> BoardEntity:
        return BoardEntity([row[:] for row in domain.cells])