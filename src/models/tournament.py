from datetime import datetime
from config import Conexion
from bson.objectid import ObjectId
from models.team import Team

db = Conexion()
tournaments_collection = db["torneos"]

class Tournament:
    # Constructor aligned with routes/tournaments.py usage
    def __init__(self, nombre, juego_id, fecha_inicio, fecha_fin, modalidad, max_participantes, miembros_X_equipo, premio):
        self.nombre = nombre
        self.juego_id = ObjectId(juego_id)
        self.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        self.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        self.modalidad = modalidad.lower()
        self.max_participantes = int(max_participantes)
        self.miembros_X_equipo = int(miembros_X_equipo) # Value is pre-calculated in route

        # Attributes set after instantiation via direct assignment in routes
        self.creador_id = None
        self.descripcion = ""
        self.reglas = ""
        self.img_portada = ""

        self.premios = [
            {"puesto": 1, "premio": premio},
            {"puesto": 2, "premio": ""},
            {"puesto": 3, "premio": ""}
        ]
        self.estado = "pendiente"  # pendiente, en_curso, finalizado
        self.participantes = []
        self.resultados = []
        self.podium = [
            {"puesto": 1, "ganador_id": ""},
            {"puesto": 2, "ganador_id": ""},
            {"puesto": 3, "ganador_id": ""}
        ]
        self.creado_en = datetime.utcnow()
        self.actualizado_en = datetime.utcnow()

    def save(self):
        self.actualizado_en = datetime.utcnow()
        tournament_data = {
            "nombre": self.nombre,
            "juego_id": self.juego_id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "modalidad": self.modalidad,
            "max_participantes": self.max_participantes, # Changed from max_cupos
            "miembros_X_equipo": self.miembros_X_equipo,
            "creador_id": self.creador_id,
            "premios": self.premios,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "participantes": self.participantes,
            "resultados": self.resultados,
            "podium": self.podium,
            "reglas": self.reglas,
            "img_portada": self.img_portada,
            "creado_en": self.creado_en,
            "actualizado_en": self.actualizado_en
        }
        return tournaments_collection.insert_one(tournament_data)

    @staticmethod
    def find_by_id(tournament_id):
        return tournaments_collection.find_one({"_id": ObjectId(tournament_id)})

    @staticmethod
    def find_all():
        return tournaments_collection.find()

    @staticmethod
    def find_by_game(game_id):
        return tournaments_collection.find({"juego_id": ObjectId(game_id)})

    @staticmethod
    def update_tournament(tournament_id, data_update):
        data_update['actualizado_en'] = datetime.utcnow()
        return tournaments_collection.update_one(
            {"_id": ObjectId(tournament_id)},
            {"$set": data_update}
        )


    @staticmethod
    def update_status(tournament_id, new_status):
        return tournaments_collection.update_one(
            {"_id": ObjectId(tournament_id)},
            {"$set": {"estado": new_status}}
        )

    @staticmethod
    def add_participant(tournament_id, participant_id):
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            raise ValueError("Torneo no encontrado")

        # Verificar si hay cupos disponibles
        if len(tournament['participantes']) >= tournament['max_participantes']: # Changed max_cupos
            raise ValueError("El torneo está lleno")

        # Verificar si el participante ya está inscrito
        if ObjectId(participant_id) in tournament['participantes']:
            raise ValueError("Ya estás inscrito en este torneo")

        return tournaments_collection.update_one(
            {"_id": ObjectId(tournament_id)},
            {"$push": {"participantes": ObjectId(participant_id)}}
        )

    @staticmethod
    def remove_participant(tournament_id, participant_id):
        return tournaments_collection.update_one(
            {"_id": ObjectId(tournament_id)},
            {"$pull": {"participantes": ObjectId(participant_id)}}
        )

    @staticmethod
    def delete_tournament(tournament_id, user_id):
        tournament = Tournament.find_by_id(tournament_id)
        if not tournament:
            raise ValueError("Torneo no encontrado")
        
        if str(tournament['creador_id']) != str(user_id):
            raise ValueError("No tienes permiso para eliminar este torneo")

        return tournaments_collection.delete_one({"_id": ObjectId(tournament_id)}) 