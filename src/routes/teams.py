from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.team import Team
from models.user import User
from decorators.auth_decorators import login_required
from models.games import games_collection
from bson.objectid import ObjectId

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')

@teams_bp.route('/')
def list_teams():
    
    teams = list(Team.find_all())
    # Obtener información de los juegos para cada equipo
    for team in teams:
        game = games_collection.find_one({"_id": team["juego_id"]})
        team["juego"] = game["game"] if game else "Juego no encontrado"
    return render_template('teams/list.html', teams=teams)

@teams_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_team():
    if request.method == 'POST':
        try:
            team = Team(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                lider_id=session['user_id'],
                juego_id=request.form['juego_id'],
                maximo_miembros=request.form['maximo_miembros'],
                url_logo=request.form['url_logo'] or "" 
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
@login_required
def view_team(team_id):
    team = Team.find_by_id(team_id)
    if team:
        # Obtener información del juego
        game = games_collection.find_one({"_id": team["juego_id"]})
        team["juego"] = game["game"] if game else "Juego no encontrado"
        team["juego_info"] = game if game else None

        # Obtener información de los miembros
        miembros_info = []
        for member_id in team["miembros"]:
            user = User.find_by_id(member_id)
            if user:
                miembro = {
                    "id": str(user["_id"]),
                    "username": user["username"],
                    "avatar": user["profile"]["avatar"],
                    "is_leader": str(member_id) == str(team["lider_id"])
                }
                miembros_info.append(miembro)
        
        team["miembros_info"] = sorted(miembros_info, key=lambda x: x["is_leader"], reverse=True)
        
        return render_template('teams/view.html', team=team)
    
    flash('Equipo no encontrado', 'error')
    return redirect(url_for('teams.list_teams'))

@teams_bp.route('/<team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):

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
                "juego_id": ObjectId(request.form['juego_id']),
                "maximo_miembros": int(request.form['maximo_miembros']),
                "url_logo": request.form['url_logo'] or "",
                "descripcion": request.form['descripcion']
            }
            Team.update_team(team_id, update_data)
            flash('Equipo actualizado exitosamente', 'success')
            return redirect(url_for('teams.view_team', team_id=team_id))
        except Exception as e:
            flash(f'Error al actualizar el equipo: {str(e)}', 'error')

    games = list(games_collection.find())
    return render_template('teams/edit.html', team=team, games=games)

@teams_bp.route('/<team_id>/join')
@login_required
def join_team(team_id):
    
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
@login_required
def leave_team(team_id):
    
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
@login_required
def delete_team(team_id):
    
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