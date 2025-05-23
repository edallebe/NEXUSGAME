from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.games import Game, games_collection
from itertools import groupby
from operator import itemgetter
from bson.objectid import ObjectId

# Creamos un blueprint para juegos
games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/')
def list_games():
    # Obtener todos los juegos y ordenarlos por categoría
    games = list(games_collection.find().sort('categoria', 1))
    
    # Agrupar juegos por categoría
    games_by_category = {}
    for game in games:
        categoria = game.get('categoria', 'Sin categoría')
        if categoria not in games_by_category:
            games_by_category[categoria] = []
        games_by_category[categoria].append(game)
    
    return render_template('games/list.html', games_by_category=games_by_category)

@games_bp.route('/new', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        try:
            # Crear nuevo juego
            game = Game(
                game=request.form['game'],
                descripcion=request.form['descripcion'],
                categoria=request.form['categoria']
            )
            
            # Actualizar las URLs de las imágenes si se proporcionaron
            if request.form.get('img_logo'):
                game.profile_game['img_logo'] = request.form['img_logo']
            if request.form.get('img_portada'):
                game.profile_game['img_portada'] = request.form['img_portada']
            
            # Guardar el juego en la base de datos
            game.save_game()
            
            flash('Juego agregado exitosamente', 'success')
            return redirect(url_for('games.list_games'))
            
        except Exception as e:
            flash(f'Error al agregar el juego: {str(e)}', 'error')
            return redirect(url_for('games.new_game'))
    
    return render_template('games/new_game.html')

@games_bp.route('/edit/<game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    try:
        # Convertir el string ID a ObjectId de MongoDB
        game_id = ObjectId(game_id)
        
        if request.method == 'POST':
            # Obtener los datos del formulario
            updated_game = {
                'game': request.form['game'],
                'descripcion': request.form['descripcion'],
                'categoria': request.form['categoria'],
                'profile_game': {
                    'img_logo': request.form.get('img_logo') or None,
                    'img_portada': request.form.get('img_portada') or None
                }
            }
            
            # Actualizar el juego en la base de datos
            result = games_collection.update_one(
                {'_id': game_id},
                {'$set': updated_game}
            )
            
            if result.modified_count > 0:
                flash('Juego actualizado exitosamente', 'success')
            else:
                flash('No se realizaron cambios en el juego', 'info')
                
            return redirect(url_for('games.list_games'))
            
        # Obtener el juego para mostrar en el formulario
        game = games_collection.find_one({'_id': game_id})
        if game:
            return render_template('games/edit_game.html', game=game)
        else:
            flash('Juego no encontrado', 'error')
            return redirect(url_for('games.list_games'))
            
    except Exception as e:
        flash(f'Error al editar el juego: {str(e)}', 'error')
        return redirect(url_for('games.list_games'))

