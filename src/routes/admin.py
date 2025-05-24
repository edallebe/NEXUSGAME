from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from decorators.auth_decorators import admin_required, login_required
from models.user import User
from models.games import games_collection
from models.post import posts_collection
from models.team import teams_collection
from models.user import users_collection
from models.tournament import tournaments_collection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Panel principal del administrador con estadísticas"""
    stats = {
        'total_users': users_collection.count_documents({}),
        'total_games': games_collection.count_documents({}),
        'total_posts': posts_collection.count_documents({}),
        'total_teams': teams_collection.count_documents({}),
        'total_tournaments': tournaments_collection.count_documents({})
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
@admin_required
def manage_users():
    """Gestión de usuarios"""
    users = list(users_collection.find().sort('created_at', -1))
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<user_id>/promote')
@admin_required
def promote_user(user_id):
    """Promover usuario a administrador"""
    try:
        User.update_role(user_id, 'administrador')
        flash('Usuario promovido a administrador exitosamente', 'success')
    except Exception as e:
        flash(f'Error al promover usuario: {str(e)}', 'error')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/<user_id>/demote')
@admin_required
def demote_user(user_id):
    """Degradar administrador a usuario"""
    try:
        User.update_role(user_id, 'usuario')
        flash('Administrador degradado a usuario exitosamente', 'success')
    except Exception as e:
        flash(f'Error al degradar usuario: {str(e)}', 'error')
    return redirect(url_for('admin.manage_users'))