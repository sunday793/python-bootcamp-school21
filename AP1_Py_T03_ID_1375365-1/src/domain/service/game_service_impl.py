from uuid import UUID
from ..model.game import Game
from ..model.board import Board
from .game_service import GameService

HUMAN, COMPUTER, EMPTY = 1, 2, 0


class GameServiceImpl(GameService):
    def __init__(self, repository):
        self.repository = repository

    def create_game(self, uuid: UUID) -> Game:
        return self.repository.create(uuid)

    # public API
    def make_move(self, game: Game) -> Game:
        old = self.repository.find_by_id(game.uuid)
        if old is None:
            raise ValueError("Game not found")

        if self.is_finished(old.board):
            raise ValueError("Game is already finished. No more moves allowed.")

        error_msg = self._validate_transition(old.board, game.board)
        if error_msg:
            raise ValueError(error_msg)

        new_board = game.board.copy()
        
        if not self.is_finished(new_board):
            self._apply_minimax(new_board)

        result = Game(game.uuid, new_board)
        self.repository.save(result)
        return result

    def _validate_transition(self, old: Board, new: Board) -> str | None:
        """Возвращает текст ошибки, если ход невалиден, иначе None."""
        diff_count = 0
        
        for r in range(3):
            for c in range(3):
                old_val = old.cells[r][c]
                new_val = new.cells[r][c]
                
                if old_val != 0 and old_val != new_val:
                    if old_val == HUMAN:
                        return "Invalid board: previous moves cannot be altered."
                    else:
                        return "Invalid board: you cannot overwrite the computer's move."
                
                if old_val == 0 and new_val == HUMAN:
                    diff_count += 1
                
                elif old_val == 0 and new_val != 0 and new_val != HUMAN:
                    return "Invalid board: you can only place 1 (your move) on empty cells."

        if diff_count == 0:
            return "Invalid board: no new moves were detected."
        if diff_count > 1:
            return "Invalid board: you can only make one move at a time."

        return None

    def validate_board(self, game: Game) -> bool:
        old = self.repository.find_by_id(game.uuid)
        if old is None:
            return False
        return self._validate_transition(old.board, game.board) is None

    def is_finished(self, board: Board) -> bool:
        return self._winner(board.cells) is not None or self._is_full(board.cells)

    def _apply_minimax(self, board: Board) -> None:
        best_score, best_move = -float("inf"), None
        for r in range(3):
            for c in range(3):
                if board.cells[r][c] == EMPTY:
                    board.cells[r][c] = COMPUTER
                    score = self._minimax(board.cells, 0, False)
                    board.cells[r][c] = EMPTY
                    if score > best_score:
                        best_score, best_move = score, (r, c)
        if best_move:
            board.cells[best_move[0]][best_move[1]] = COMPUTER

    def _minimax(self, cells, depth, is_maximizing) -> int:
        winner = self._winner(cells)
        if winner == COMPUTER:
            return 10 - depth
        if winner == HUMAN:
            return depth - 10
        if self._is_full(cells):
            return 0

        if is_maximizing:
            best = -float("inf")
            for r in range(3):
                for c in range(3):
                    if cells[r][c] == EMPTY:
                        cells[r][c] = COMPUTER
                        best = max(best, self._minimax(cells, depth + 1, False))
                        cells[r][c] = EMPTY
            return best
        else:
            best = float("inf")
            for r in range(3):
                for c in range(3):
                    if cells[r][c] == EMPTY:
                        cells[r][c] = HUMAN
                        best = min(best, self._minimax(cells, depth + 1, True))
                        cells[r][c] = EMPTY
            return best

    @staticmethod
    def _winner(cells):
        lines = (
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)],
        )
        for (a, b, c) in lines:
            v = cells[a[0]][a[1]]
            if v != EMPTY and v == cells[b[0]][b[1]] == cells[c[0]][c[1]]:
                return v
        return None

    @staticmethod
    def _is_full(cells):
        return all(cells[r][c] != EMPTY for r in range(3) for c in range(3))