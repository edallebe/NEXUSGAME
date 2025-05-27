from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.tournament import Tournament
from models.games import games_collection
from models.team import Team
from models.user import User
from decorators.auth_decorators import login_required
from bson.objectid import ObjectId
from datetime import datetime

tournaments_bp = Blueprint('tournaments', __name__, url_prefix='/tournaments')

@tournaments_bp.route('/')
def list_tournaments():
    tournaments = list(Tournament.find_all())
    # Obtener información de los juegos para cada torneo
    for tournament in tournaments:
        game = games_collection.find_one({"_id": tournament["juego_id"]})
        tournament["juego"] = game["game"] if game else "Juego no encontrado"
    return render_template('tournaments/list.html', tournaments=tournaments)

@tournaments_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_tournament():
    if request.method == 'POST':
        try:
            modalidad = request.form['modalidad']
            miembros_x_equipo = 1 if modalidad == 'individual' else int(request.form.get('miembros_X_equipo', 2))

            tournament = Tournament(
                nombre=request.form['nombre'],
                juego_id=request.form['juego_id'],
                descripcion=request.form['descripcion'],
                fecha_inicio=request.form['fecha_inicio'],
                fecha_fin=request.form['fecha_fin'],
                modalidad=modalidad,
                max_cupos=int(request.form['max_cupos']),
                miembros_X_equipo=miembros_x_equipo,
                premio=request.form['premio']
            )

            # Establecer el creador del torneo
            tournament.creador_id = ObjectId(session['user_id'])

            # Actualizar campos adicionales
            tournament.reglas = request.form.get('reglas', '')
            tournament.img_portada = request.form.get('img_portada', '')

            # Actualizar premios adicionales
            if request.form.get('premio2'):
                tournament.premios[1]['premio'] = request.form['premio2']
            if request.form.get('premio3'):
                tournament.premios[2]['premio'] = request.form['premio3']

            tournament.save()
            flash('Torneo creado exitosamente', 'success')
            return redirect(url_for('tournaments.list_tournaments'))
        except Exception as e:
            flash(f'Error al crear el torneo: {str(e)}', 'error')
            return redirect(url_for('tournaments.new_tournament'))

    games = list(games_collection.find())
    return render_template('tournaments/new.html', games=games)

@tournaments_bp.route('/<tournament_id>')
def view_tournament(tournament_id):
    tournament = Tournament.find_by_id(tournament_id)
    if tournament:
        # Obtener información del juego
        game = games_collection.find_one({"_id": tournament["juego_id"]})
        tournament["juego"] = game["game"] if game else "Juego no encontrado"
        
        # Obtener información de participantes
        participantes_info = []
        for participant_id in tournament["participantes"]:
            if tournament["modalidad"] == "individual":
                user = User.find_by_id(participant_id)
                if user:
                    participantes_info.append({
                        "id": str(user["_id"]),
                        "nombre": user["username"],
                        "tipo": "individual"
                    })
            else:
                team = Team.find_by_id(participant_id)
                if team:
                    participantes_info.append({
                        "id": str(team["_id"]),
                        "nombre": team["nombre"],
                        "tipo": "equipo",
                        "miembros": team["miembros"]
                    })
        
        tournament["participantes_info"] = participantes_info
        
        # Verificar si el usuario actual es el creador
        is_creator = False
        if 'user_id' in session:
            is_creator = str(tournament.get('creador_id', '')) == str(session['user_id'])
        
        return render_template('tournaments/view.html', tournament=tournament, is_creator=is_creator)
    
    flash('Torneo no encontrado', 'error')
    return redirect(url_for('tournaments.list_tournaments'))

@tournaments_bp.route('/<tournament_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tournament(tournament_id):
    tournament = Tournament.find_by_id(tournament_id)
    if not tournament:
        flash('Torneo no encontrado', 'error')
        return redirect(url_for('tournaments.list_tournaments'))

    # Verificar si el usuario actual es el creador
    if str(tournament.get('creador_id', '')) != str(session['user_id']):
        flash('No tienes permiso para editar este torneo', 'error')
        return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

    if request.method == 'POST':
        try:
            # Solo permitir edición si el torneo está pendiente
            if tournament["estado"] != "pendiente":
                flash('No se puede editar un torneo que ya ha iniciado o finalizado', 'error')
                return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

            update_data = {
                "nombre": request.form['nombre'],
                "descripcion": request.form['descripcion'],
                "fecha_inicio": datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d'),
                "fecha_fin": datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d'),
                "max_cupos": int(request.form['max_cupos']),
                "reglas": request.form['reglas'],
                "img_portada": request.form['img_portada'] or ""
            }
            
            tournaments_collection.update_one(
                {"_id": ObjectId(tournament_id)},
                {"$set": update_data}
            )
            flash('Torneo actualizado exitosamente', 'success')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        except Exception as e:
            flash(f'Error al actualizar el torneo: {str(e)}', 'error')

    # Obtener información del juego para mostrar en el formulario
    game = games_collection.find_one({"_id": tournament["juego_id"]})
    tournament["juego"] = game["game"] if game else "Juego no encontrado"
    
    return render_template('tournaments/edit.html', tournament=tournament)

@tournaments_bp.route('/<tournament_id>/join')
@login_required
def join_tournament(tournament_id):
    try:
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            flash('Torneo no encontrado', 'error')
            return redirect(url_for('tournaments.list_tournaments'))
        
        # Verificar si el torneo está lleno
        if len(tournament['participantes']) >= tournament['max_cupos']:
            flash('El torneo está lleno', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        # Verificar si el torneo ya comenzó
        if tournament['estado'] != 'pendiente':
            flash('No se puede unir a un torneo que ya ha iniciado o finalizado', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

        user_id = session['user_id']
        
        if tournament['modalidad'] == 'equipo':
            # Buscar equipos donde el usuario es líder
            teams = Team.find_by_leader(user_id)
            if not teams:
                flash('Necesitas ser líder de un equipo para participar en este torneo', 'error')
                return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
            
            # Obtener información completa de los miembros de cada equipo
            for team in teams:
                team_members = []
                for member_id in team.get('miembros', []):
                    member = User.find_by_id(member_id)
                    if member:
                        team_members.append({
                            'id': str(member['_id']),
                            'username': member['username']
                        })
                team['miembros'] = team_members
            
            # Verificar si alguno de sus equipos ya está inscrito
            for team in teams:
                if ObjectId(team['_id']) in tournament['participantes']:
                    flash('Ya tienes un equipo inscrito en este torneo', 'info')
                    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
            
            # Si tiene equipos válidos, redirigir a la página de selección de equipo
            return render_template('tournaments/select_team.html', 
                                tournament=tournament, 
                                teams=teams)
        else:
            # Modalidad individual
            if ObjectId(user_id) in tournament['participantes']:
                flash('Ya estás inscrito en este torneo', 'info')
                return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
            
            Tournament.add_participant(tournament_id, user_id)
            flash('Te has inscrito al torneo exitosamente', 'success')
        
    except Exception as e:
        flash(f'Error al unirse al torneo: {str(e)}', 'error')
    
    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

@tournaments_bp.route('/<tournament_id>/join/team', methods=['POST'])
@login_required
def join_tournament_team(tournament_id):
    try:
        team_id = request.form.get('team_id')
        if not team_id:
            flash('Debes seleccionar un equipo', 'error')
            return redirect(url_for('tournaments.join_tournament', tournament_id=tournament_id))

        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            flash('Torneo no encontrado', 'error')
            return redirect(url_for('tournaments.list_tournaments'))

        # Verificar que el usuario sea líder del equipo
        team = Team.find_by_id(team_id)
        if not team or str(team['lider_id']) != str(session['user_id']):
            flash('No tienes permiso para inscribir este equipo', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

        # Verificar que el equipo tenga el número correcto de miembros
        if len(team['miembros']) != tournament['miembros_X_equipo']:
            flash(f'El equipo debe tener exactamente {tournament["miembros_X_equipo"]} miembros', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

        Tournament.add_participant(tournament_id, team_id)
        flash('Equipo inscrito exitosamente', 'success')

    except Exception as e:
        flash(f'Error al inscribir el equipo: {str(e)}', 'error')

    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

@tournaments_bp.route('/<tournament_id>/leave')
@login_required
def leave_tournament(tournament_id):
    try:
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            flash('Torneo no encontrado', 'error')
            return redirect(url_for('tournaments.list_tournaments'))
        
        if tournament['estado'] != 'pendiente':
            flash('No puedes abandonar un torneo que ya ha iniciado o finalizado', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        user_id = session['user_id']
        
        if tournament['modalidad'] == 'equipo':
            # Buscar el equipo del usuario que está en el torneo
            teams = Team.find_by_leader(user_id)
            for team in teams:
                if ObjectId(team['_id']) in tournament['participantes']:
                    Tournament.remove_participant(tournament_id, team['_id'])
                    flash('Tu equipo ha abandonado el torneo exitosamente', 'success')
                    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
            
            flash('No tienes ningún equipo inscrito en este torneo', 'error')
        else:
            # Modalidad individual
            if ObjectId(user_id) not in tournament['participantes']:
                flash('No estás inscrito en este torneo', 'info')
                return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
            
            Tournament.remove_participant(tournament_id, user_id)
            flash('Has abandonado el torneo exitosamente', 'success')
        
    except Exception as e:
        flash(f'Error al abandonar el torneo: {str(e)}', 'error')
    
    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

@tournaments_bp.route('/<tournament_id>/delete')
@login_required
def delete_tournament(tournament_id):
    try:
        Tournament.delete_tournament(tournament_id, session['user_id'])
        flash('Torneo eliminado exitosamente', 'success')
        return redirect(url_for('tournaments.list_tournaments'))
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
    except Exception as e:
        flash(f'Error al eliminar el torneo: {str(e)}', 'error')
        return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id)) 