from flask import Flask, request, jsonify
from flask_cors import CORS
from game import Game

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "https://jukesites.com"]
    }
})
game = Game()


@app.route("/health_check")
def health():
    return jsonify({"name": "rock-paper-scissors", "version": "", "status": "OK"}), 200


@app.route("/add_player", methods=["POST"])
def add_player():
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    player = data.get("player")
    if not player:
        return jsonify({"error": "No player name provided"}), 400
    game.add_player(player)
    return jsonify({"message": f"Player {player} added"}), 200


@app.route("/play", methods=["POST"])
def play():
    data = request.json
    if data is None:
        return jsonify({"error": "Invalid input, expected JSON"}), 400
    choice = data.get("choice")
    if choice not in ["rock", "paper", "scissors", "exit"]:
        return jsonify({"error": "Invalid choice"}), 400
    result = game.play_round(choice)
    return jsonify(result), 200


@app.route("/status", methods=["GET"])
def status():
    status = {
        "player_score": game.player_score if game.player_score else None,
        "cpu_score": game.cpu_score if game.cpu_score else None,
        "is_active": game.is_active if game.is_active else None,
        "player": game.player if game.player else None,
    }
    return jsonify(status), 200


if __name__ == "__main__":
    app.run(debug=True)
