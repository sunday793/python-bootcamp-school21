from flask import Blueprint, request, jsonify
from uuid import UUID

from ..model.board import BoardDTO
from ..model.game import GameDTO
from ..mapper.game_mapper import WebGameMapper

game_bp = Blueprint("game", __name__)


def create_game_blueprint(service):
    @game_bp.post("/game/<uuid:game_id>")
    def make_move(game_id: UUID):
        payload = request.get_json(silent=True)
        if not payload or "board" not in payload:
            return jsonify({"error": "Missing board"}), 400

        try:
            dto = GameDTO(str(game_id), BoardDTO(payload["board"]))
            domain = WebGameMapper.to_domain(dto)
            result = service.make_move(domain)
            return jsonify({
                "uuid": str(result.uuid),
                "board": result.board.cells,
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal error", "detail": str(e)}), 500

    return game_bp