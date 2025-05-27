from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.team import Team
from models.games import games_collection
from bson.objectid import ObjectId

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')

@teams_bp.route('/')
def list_teams():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver los equipos', 'error')
        return redirect(url_for('auth.login'))
    
    teams = list(Team.find_all())
    # Obtener información de los juegos para cada equipo
    for team in teams:
        game = games_collection.find_one({"_id": team["juego_id"]})
        team["juego"] = game["game"] if game else "Juego no encontrado"
    return render_template('teams/list.html', teams=teams)

@teams_bp.route('/new', methods=['GET', 'POST'])
def new_team():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para crear un equipo', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        try:
            team = Team(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                lider_id=session['user_id'],
                juego_id=request.form['juego_id']
            )
            team.save()
            flash('Equipo creado exitosamente', 'success')
            return redirect(url_for('teams.list_teams'))
        except Exception as e:
            flash(f'Error al crear el equipo: {str(e)}', 'error')
            return redirect(url_for('teams.new_team'))

    games = list(games_collection.find())
    return render_template('teams/new.html', games=games)

@teams_bp.route('/<team_id>')
def view_team(team_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver los equipos', 'error')
        return redirect(url_for('auth.login'))

    team = Team.find_by_id(team_id)
    if team:
        game = games_collection.find_one({"_id": team["juego_id"]})
        team["juego"] = game["game"] if game else "Juego no encontrado"
        return render_template('teams/view.html', team=team)
    flash('Equipo no encontrado', 'error')
    return redirect(url_for('teams.list_teams'))

@teams_bp.route('/<team_id>/edit', methods=['GET', 'POST'])
def edit_team(team_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para editar equipos', 'error')
        return redirect(url_for('auth.login'))

    team = Team.find_by_id(team_id)
    if not team:
        flash('Equipo no encontrado', 'error')
        return redirect(url_for('teams.list_teams'))

    if str(team['lider_id']) != session['user_id']:
        flash('Solo el líder del equipo puede editarlo', 'error')
        return redirect(url_for('teams.view_team', team_id=team_id))

    if request.method == 'POST':
        try:
            update_data = {
                "nombre": request.form['nombre'],
                "descripcion": request.form['descripcion'],
                "juego_id": ObjectId(request.form['juego_id'])
            }
            Team.update_team(team_id, update_data)
            flash('Equipo actualizado exitosamente', 'success')
            return redirect(url_for('teams.view_team', team_id=team_id))
        except Exception as e:
            flash(f'Error al actualizar el equipo: {str(e)}', 'error')

    games = list(games_collection.find())
    return render_template('teams/edit.html', team=team, games=games)

@teams_bp.route('/<team_id>/join')
def join_team(team_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para unirte a un equipo', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        team = Team.find_by_id(team_id)
        if not team:
            flash('Equipo no encontrado', 'error')
            return redirect(url_for('teams.list_teams'))
        
        if ObjectId(session['user_id']) in team['miembros']:
            flash('Ya eres miembro de este equipo', 'info')
            return redirect(url_for('teams.view_team', team_id=team_id))
        
        Team.add_member(team_id, session['user_id'])
        flash('Te has unido al equipo exitosamente', 'success')
    except Exception as e:
        flash(f'Error al unirse al equipo: {str(e)}', 'error')
    
    return redirect(url_for('teams.view_team', team_id=team_id))

@teams_bp.route('/<team_id>/leave')
def leave_team(team_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para salir de un equipo', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        team = Team.find_by_id(team_id)
        if not team:
            flash('Equipo no encontrado', 'error')
            return redirect(url_for('teams.list_teams'))
        
        if str(team['lider_id']) == session['user_id']:
            flash('El líder no puede abandonar el equipo', 'error')
            return redirect(url_for('teams.view_team', team_id=team_id))
        
        if ObjectId(session['user_id']) not in team['miembros']:
            flash('No eres miembro de este equipo', 'info')
            return redirect(url_for('teams.view_team', team_id=team_id))
        
        Team.remove_member(team_id, session['user_id'])
        flash('Has salido del equipo exitosamente', 'success')
    except Exception as e:
        flash(f'Error al salir del equipo: {str(e)}', 'error')
    
    return redirect(url_for('teams.view_team', team_id=team_id))

@teams_bp.route('/<team_id>/delete')
def delete_team(team_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para eliminar equipos', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        team = Team.find_by_id(team_id)
        if not team:
            flash('Equipo no encontrado', 'error')
            return redirect(url_for('teams.list_teams'))
        
        if str(team['lider_id']) != session['user_id']:
            flash('Solo el líder puede eliminar el equipo', 'error')
            return redirect(url_for('teams.view_team', team_id=team_id))
        
        Team.delete_team(team_id)
        flash('Equipo eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar el equipo: {str(e)}', 'error')
    
    return redirect(url_for('teams.list_teams')) 