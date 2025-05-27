from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models.post import Post, Comment, Reaction, posts_collection
from models.games import games_collection
from models.user import users_collection
from bson.objectid import ObjectId
from datetime import datetime
social_bp = Blueprint('social', __name__, url_prefix='/social')

@social_bp.route('/')
def feed():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver el muro social', 'error')
        return redirect(url_for('auth.login'))
    
    page = request.args.get('page', 1, type=int)
    limit = 10
    skip = (page - 1) * limit
    
    posts = Post.get_all(limit=limit, skip=skip)
    total_posts = posts_collection.count_documents({})
    
    # Obtener información adicional para cada post
    for post in posts:
        autor = users_collection.find_one({"_id": post["autor_id"]})
        post["autor"] = autor["username"] if autor else "Usuario desconocido"
        
        if post.get("juego_id"):
            juego = games_collection.find_one({"_id": post["juego_id"]})
            post["juego"] = juego["game"] if juego else "Juego no encontrado"
        
        # Verificar si el usuario actual ha dado like
        reaction = Reaction.get_by_user_and_post(session['user_id'], post["_id"])
        post["user_reaction"] = reaction["tipo"] if reaction else None
    
    return render_template('social/feed.html', 
                         posts=posts,
                         page=page,
                         total_pages=(total_posts + limit - 1) // limit)

@social_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para crear una publicación', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            post = Post(
                titulo=request.form['titulo'],
                contenido=request.form['contenido'],
                autor_id=session['user_id'],
                tipo=request.form['tipo'],
                juego_id=request.form.get('juego_id')
            )
            post.save()
            flash('Publicación creada exitosamente', 'success')
            return redirect(url_for('social.feed'))
        except Exception as e:
            flash(f'Error al crear la publicación: {str(e)}', 'error')
    
    games = list(games_collection.find())
    return render_template('social/new_post.html', games=games)

@social_bp.route('/post/<post_id>')
def view_post(post_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver las publicaciones', 'error')
        return redirect(url_for('auth.login'))
    
    post = Post.get_by_id(post_id)
    if not post:
        flash('Publicación no encontrada', 'error')
        return redirect(url_for('social.feed'))
    
    # Obtener información del autor
    autor = users_collection.find_one({"_id": post["autor_id"]})
    post["autor"] = autor["username"] if autor else "Usuario desconocido"
    
    # Obtener información del juego si existe
    if post.get("juego_id"):
        juego = games_collection.find_one({"_id": post["juego_id"]})
        post["juego"] = juego["game"] if juego else "Juego no encontrado"
    
    # Obtener comentarios
    comments = Comment.get_by_post(post_id)
    for comment in comments:
        autor = users_collection.find_one({"_id": comment["autor_id"]})
        comment["autor"] = autor["username"] if autor else "Usuario desconocido"
    
    # Verificar reacción del usuario
    reaction = Reaction.get_by_user_and_post(session['user_id'], post["_id"])
    post["user_reaction"] = reaction["tipo"] if reaction else None
    
    return render_template('social/view_post.html', post=post, comments=comments)

@social_bp.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        comment = Comment(
            contenido=request.form['contenido'],
            autor_id=session['user_id'],
            post_id=post_id
        )
        result = comment.save()
        
        # Obtener información del autor para la respuesta
        autor = users_collection.find_one({"_id": ObjectId(session['user_id'])})
        
        return jsonify({
            'success': True,
            'comment': {
                'id': str(result.inserted_id),
                'contenido': request.form['contenido'],
                'autor': autor['username'],
                'fecha_creacion': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/post/<post_id>/react', methods=['POST'])
def react_to_post(post_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        reaction = Reaction(
            usuario_id=session['user_id'],
            post_id=post_id,
            tipo=request.form.get('tipo', 'like')
        )
        is_new = reaction.save()
        
        # Obtener el número actualizado de likes
        post = Post.get_by_id(post_id)
        
        return jsonify({
            'success': True,
            'likes': post['likes'],
            'is_new': is_new
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@social_bp.route('/post/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    if 'user_id' not in session:
        flash('No autorizado', 'error')
        return redirect(url_for('social.feed'))
    
    post = Post.get_by_id(post_id)
    if not post:
        flash('Publicación no encontrada', 'error')
        return redirect(url_for('social.feed'))
    
    if str(post['autor_id']) != session['user_id']:
        flash('No tienes permiso para eliminar esta publicación', 'error')
        return redirect(url_for('social.view_post', post_id=post_id))
    
    try:
        Post.delete_post(post_id)
        flash('Publicación eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar la publicación: {str(e)}', 'error')
    
    return redirect(url_for('social.feed'))

@social_bp.route('/comment/<comment_id>/delete', methods=['POST'])
def delete_comment(comment_id):
    if 'user_id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        result = Comment.delete_comment(comment_id)
        if result:
            return jsonify({'success': True})
        return jsonify({'error': 'Comentario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500 