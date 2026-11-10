class GameEntity:
    def __init__(self, uuid: str, board: "BoardEntity"):
        self.uuid = uuid
        self.board = board