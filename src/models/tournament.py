from datetime import datetime
from config import Conexion
from bson.objectid import ObjectId

db = Conexion()
tournaments_collection = db["torneos"]

class Tournament:
    def __init__(self, nombre, juego_id, descripcion, fecha_inicio, fecha_fin, modalidad, max_cupos, miembros_X_equipo, premio):
        self.nombre = nombre
        self.juego_id = ObjectId(juego_id)  # Referencia al del juego
        self.descripcion = descripcion
        self.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        self.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        self.modalidad = modalidad.lower()  # solo escoger entre "individual" o "equipo"
        self.max_cupos = int(max_cupos)  # Máximo de jugadores o equipos
        self.miembros_X_equipo = int(miembros_X_equipo) if self.modalidad == "equipo" else 1
        
        # Inicializar los premios con el premio principal y espacios para segundo y tercer lugar
        self.premios = [
            {"puesto": 1, "premio": premio},
            {"puesto": 2, "premio": ""},
            {"puesto": 3, "premio": ""}
        ]
        self.estado = "pendiente"  # pendiente, en_progreso, finalizado
        self.participantes = []  # Lista de jugadores o equipos
        self.resultados = []  # Historial de resultados
        self.podium = [  # Lista de ganadores ordenada por puesto
            {"puesto": 1, "ganador_id": ""},
            {"puesto": 2, "ganador_id": ""},
            {"puesto": 3, "ganador_id": ""}
        ]
        self.reglas = ""  # Reglas del torneo
        self.img_portada = ""  # URL o path a imagen de portada
        self.creado_en = datetime.utcnow()        

    def save(self):
        tournament_data = {
            "nombre": self.nombre,
            "juego_id": self.juego_id,
            "descripcion": self.descripcion,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "modalidad": self.modalidad,
            "max_cupos": self.max_cupos,
            "miembros_X_equipo": self.miembros_X_equipo,
            "premios": self.premios,
            "estado": self.estado,
            "participantes": self.participantes,
            "resultados": self.resultados,
            "podium": self.podium,
            "reglas": self.reglas,
            "img_portada": self.img_portada,
            "creado_en": self.creado_en
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
    def update_status(tournament_id, new_status):
        return tournaments_collection.update_one(
            {"_id": ObjectId(tournament_id)},
            {"$set": {"estado": new_status}}
        )

    @staticmethod
    def add_participant(tournament_id, user_id):
        return tournaments_collection.update_one(
            {"_id": ObjectId(tournament_id)},
            {"$push": {"participantes": ObjectId(user_id)}}
        )

    @staticmethod
    def remove_participant(tournament_id, user_id):
        return tournaments_collection.update_one(
            {"_id": ObjectId(tournament_id)},
            {"$pull": {"participantes": ObjectId(user_id)}}
        ) 