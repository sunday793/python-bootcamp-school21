from ..model.board import BoardDTO
from domain.model.board import Board

class WebBoardMapper:
    @staticmethod
    def to_domain(dto: BoardDTO) -> Board:
        cells = [[int(cell) for cell in row] for row in dto.cells]
        return Board(cells)

    @staticmethod
    def to_dto(domain: Board) -> BoardDTO:
        return BoardDTO([row[:] for row in domain.cells])