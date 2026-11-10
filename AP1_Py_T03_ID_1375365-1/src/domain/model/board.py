class Board:
    """Integer matrix. 0 = empty, 1 = player, 2 = computer."""
    def __init__(self, cells: list[list[int]]):
        self.cells = cells

    def copy(self) -> "Board":
        """Return a copy of the board."""
        return Board([row[:] for row in self.cells])