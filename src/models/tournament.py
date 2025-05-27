from datetime import datetime
from config import Conexion
from bson.objectid import ObjectId

db = Conexion()
tournaments_collection = db["torneos"]

class Tournament:
    def __init__(self, nombre, juego_id, fecha_inicio, fecha_fin, max_participantes, premio, descripcion):
        self.nombre = nombre
        self.juego_id = ObjectId(juego_id)
        self.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        self.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        self.max_participantes = int(max_participantes)
        self.premio = premio
        self.descripcion = descripcion
        self.estado = "pendiente"  # pendiente, en_progreso, finalizado
        self.participantes = []
        self.creado_en = datetime.utcnow()

    def save(self):
        tournament_data = {
            "nombre": self.nombre,
            "juego_id": self.juego_id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "max_participantes": self.max_participantes,
            "premio": self.premio,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "participantes": self.participantes,
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