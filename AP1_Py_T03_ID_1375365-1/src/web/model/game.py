from .board import BoardDTO


class GameDTO:
    def __init__(self, uuid: str, board: BoardDTO):
        self.uuid = uuid
        self.board = board