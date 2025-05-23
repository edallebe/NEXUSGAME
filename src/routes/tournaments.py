from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.tournament import Tournament
from models.games import games_collection
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
def new_tournament():
    if request.method == 'POST':
        try:
            tournament = Tournament(
                nombre=request.form['nombre'],
                juego_id=request.form['juego_id'],
                fecha_inicio=request.form['fecha_inicio'],
                fecha_fin=request.form['fecha_fin'],
                max_participantes=request.form['max_participantes'],
                premio=request.form['premio'],
                descripcion=request.form['descripcion']
            )
            tournament.save()
            flash('Torneo creado exitosamente', 'success')
            return redirect(url_for('tournaments.list_tournaments'))
        except Exception as e:
            flash(f'Error al crear el torneo: {str(e)}', 'error')
            return redirect(url_for('tournaments.new_tournament'))

    # Obtener lista de juegos para el formulario
    games = list(games_collection.find())
    return render_template('tournaments/new.html', games=games)

@tournaments_bp.route('/<tournament_id>')
def view_tournament(tournament_id):
    tournament = Tournament.find_by_id(tournament_id)
    if tournament:
        game = games_collection.find_one({"_id": tournament["juego_id"]})
        tournament["juego"] = game["game"] if game else "Juego no encontrado"
        return render_template('tournaments/view.html', tournament=tournament)
    flash('Torneo no encontrado', 'error')
    return redirect(url_for('tournaments.list_tournaments'))

@tournaments_bp.route('/<tournament_id>/edit', methods=['GET', 'POST'])
def edit_tournament(tournament_id):
    tournament = Tournament.find_by_id(tournament_id)
    if not tournament:
        flash('Torneo no encontrado', 'error')
        return redirect(url_for('tournaments.list_tournaments'))

    if request.method == 'POST':
        try:
            updated_tournament = {
                "nombre": request.form['nombre'],
                "juego_id": ObjectId(request.form['juego_id']),
                "fecha_inicio": datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d'),
                "fecha_fin": datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d'),
                "max_participantes": int(request.form['max_participantes']),
                "premio": request.form['premio'],
                "descripcion": request.form['descripcion']
            }
            tournaments_collection.update_one(
                {"_id": ObjectId(tournament_id)},
                {"$set": updated_tournament}
            )
            flash('Torneo actualizado exitosamente', 'success')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        except Exception as e:
            flash(f'Error al actualizar el torneo: {str(e)}', 'error')

    games = list(games_collection.find())
    return render_template('tournaments/edit.html', tournament=tournament, games=games)

@tournaments_bp.route('/<tournament_id>/join')
def join_tournament(tournament_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para unirte al torneo', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            flash('Torneo no encontrado', 'error')
            return redirect(url_for('tournaments.list_tournaments'))
        
        if len(tournament['participantes']) >= tournament['max_participantes']:
            flash('El torneo ya está lleno', 'error')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        if ObjectId(session['user_id']) in tournament['participantes']:
            flash('Ya estás registrado en este torneo', 'info')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        Tournament.add_participant(tournament_id, session['user_id'])
        flash('Te has unido al torneo exitosamente', 'success')
    except Exception as e:
        flash(f'Error al unirse al torneo: {str(e)}', 'error')
    
    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))

@tournaments_bp.route('/<tournament_id>/leave')
def leave_tournament(tournament_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para salir del torneo', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            flash('Torneo no encontrado', 'error')
            return redirect(url_for('tournaments.list_tournaments'))
        
        if ObjectId(session['user_id']) not in tournament['participantes']:
            flash('No estás registrado en este torneo', 'info')
            return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id))
        
        Tournament.remove_participant(tournament_id, session['user_id'])
        flash('Has salido del torneo exitosamente', 'success')
    except Exception as e:
        flash(f'Error al salir del torneo: {str(e)}', 'error')
    
    return redirect(url_for('tournaments.view_tournament', tournament_id=tournament_id)) 