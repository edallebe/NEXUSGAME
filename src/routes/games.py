from flask import Blueprint, render_template
from models.games import Game, games_collection

# Creamos un blueprint para juegos
games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/', methods=["GET","POST"])
def list_games():
    return render_template('games/list.html', games=games_collection)

@games_bp.route('/new_game')
def new_game():
    return render_template('games/new_game.html')

@games_bp.route('/<game_id>')
def game_detail(game_id):
    return f"Detalles del juego {game_id}"

@games_bp.route('/categories')
def categories():
    return "Categorías de juegos" 