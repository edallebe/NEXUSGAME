from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from models.user import User
from bson.objectid import ObjectId
from models.games import Game

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.find_by_id(session['user_id'])
    games = Game.get_all()  # Supongamos que esta función devuelve todos los juegos como una lista de dicts

    if request.method == 'POST':
        new_profile = {
            "avatar": request.form.get('avatar'),
            "full_name": request.form.get('full_name'),
            "bio": request.form.get('bio'),
            "favorite_games": request.form.getlist('favorite_games'),
            "statistics": user["profile"]["statistics"]
        }
        User.update_profile(session['user_id'], new_profile)
        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for('profile.edit_profile'))

    return render_template('edit_profile.html', user=user, games=games)

@profile_bp.route('/profile', methods=['GET'])
def view_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user = User.find_by_id(session['user_id'])
    return render_template('view_profile.html', user=user)