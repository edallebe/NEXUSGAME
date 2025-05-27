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
            # Determinar miembros por equipo basado en la modalidad
            miembros_x_equipo = 1
            if request.form['modalidad'] == 'equipo':
                miembros_x_equipo = int(request.form['miembros_X_equipo'])

            # Crear el torneo con el premio principal
            tournament = Tournament(
                nombre=request.form['nombre'],
                juego_id=request.form['juego_id'],
                descripcion=request.form['descripcion'],
                fecha_inicio=request.form['fecha_inicio'],
                fecha_fin=request.form['fecha_fin'],
                modalidad=request.form['modalidad'],
                max_cupos=int(request.form['max_cupos']),
                miembros_X_equipo=miembros_x_equipo,
                premio=request.form['premio']  # Premio principal
            )

            # Actualizar los premios adicionales si existen
            if request.form.get('premio2'):
                tournament.premios[1]['premio'] = request.form['premio2']
            if request.form.get('premio3'):
                tournament.premios[2]['premio'] = request.form['premio3']

            # Actualizar campos adicionales
            tournament.reglas = request.form['reglas']
            tournament.img_portada = request.form['img_portada'] or ""
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
                        "tipo": "equipo"
                    })
        
        tournament["participantes_info"] = participantes_info
        return render_template('tournaments/view.html', tournament=tournament)
    
    flash('Torneo no encontrado', 'error')
    return redirect(url_for('tournaments.list_tournaments'))

@tournaments_bp.route('/<tournament_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tournament(tournament_id):
    tournament = Tournament.find_by_id(tournament_id)
    if not tournament:
        flash('Torneo no encontrado', 'error')
        return redirect(url_for('tournaments.list_tournaments'))

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

    games = list(games_collection.find())
    return render_template('tournaments/edit.html', tournament=tournament, games=games)

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
        
        participant_id = session['user_id']
        if tournament['modalidad'] == 'equipo':
            # TODO: Implementar lógica para seleccionar equipo al unirse

            flash('Función de unirse como equipo en desarrollo', 'info')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        if ObjectId(participant_id) in tournament['participantes']:
            flash('Ya estás inscrito en este torneo', 'info')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        Tournament.add_participant(tournament_id, participant_id)
        flash('Te has inscrito al torneo exitosamente', 'success')
    except Exception as e:
        flash(f'Error al unirse al torneo: {str(e)}', 'error')
    
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
        
        participant_id = session['user_id']
        if ObjectId(participant_id) not in tournament['participantes']:
            flash('No estás inscrito en este torneo', 'info')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        Tournament.remove_participant(tournament_id, participant_id)
        flash('Has abandonado el torneo exitosamente', 'success')
    except Exception as e:
        flash(f'Error al abandonar el torneo: {str(e)}', 'error')
    
    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

@tournaments_bp.route('/<tournament_id>/start')
@login_required
def start_tournament(tournament_id):
    try:
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            flash('Torneo no encontrado', 'error')
            return redirect(url_for('tournaments.list_tournaments'))
        
        if tournament['estado'] != 'pendiente':
            flash('El torneo ya ha iniciado o finalizado', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        if len(tournament['participantes']) < 2:
            flash('El torneo necesita al menos 2 participantes para iniciar', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        Tournament.update_status(tournament_id, 'en_progreso')
        flash('El torneo ha iniciado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al iniciar el torneo: {str(e)}', 'error')
    
    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

@tournaments_bp.route('/<tournament_id>/finish')
@login_required
def finish_tournament(tournament_id):
    try:
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            flash('Torneo no encontrado', 'error')
            return redirect(url_for('tournaments.list_tournaments'))
        
        if tournament['estado'] != 'en_progreso':
            flash('El torneo debe estar en progreso para poder finalizarlo', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        Tournament.update_status(tournament_id, 'finalizado')
        flash('El torneo ha finalizado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al finalizar el torneo: {str(e)}', 'error')
    
    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id)) 