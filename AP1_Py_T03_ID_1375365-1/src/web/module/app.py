from uuid import uuid4
from flask import Flask, jsonify

from di.container import Container
from web.route.game_route import create_game_blueprint


def create_app() -> Flask:
    container = Container()
    app = Flask(__name__)

    app.register_blueprint(create_game_blueprint(container.service))

    @app.post("/game")
    def new_game():
        uuid = uuid4()
        game = container.service.create_game(uuid)
        return jsonify({
            "uuid": str(game.uuid),
            "board": game.board.cells,
        }), 201

    @app.get("/game/<uuid:game_id>")
    def get_game(game_id):
        game = container.repository.find_by_id(game_id)
        if game is None:
            return jsonify({"error": "Game not found"}), 404
        
        return jsonify({
            "uuid": str(game.uuid),
            "board": game.board.cells,
        }), 200

    return app