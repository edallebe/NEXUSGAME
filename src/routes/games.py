from flask import Blueprint, render_template

# Creamos un blueprint para juegos
games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/')
def list_games():
    return render_template('games/list.html')

@games_bp.route('/<game_id>')
def game_detail(game_id):
    return f"Detalles del juego {game_id}"

@games_bp.route('/categories')
def categories():
    return "Categorías de juegos" 