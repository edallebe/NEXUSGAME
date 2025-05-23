from datetime import datetime
from config import Conexion
from bson.objectid import ObjectId

db = Conexion()
teams_collection = db["equipos"]

class Team:
    def __init__(self, nombre, descripcion, lider_id, juego_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.lider_id = ObjectId(lider_id)
        self.juego_id = ObjectId(juego_id)
        self.miembros = [ObjectId(lider_id)]  # El líder es el primer miembro
        self.creado_en = datetime.utcnow()

    def save(self):
        team_data = {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "lider_id": self.lider_id,
            "juego_id": self.juego_id,
            "miembros": self.miembros,
            "creado_en": self.creado_en
        }
        return teams_collection.insert_one(team_data)

    @staticmethod
    def find_by_id(team_id):
        return teams_collection.find_one({"_id": ObjectId(team_id)})

    @staticmethod
    def find_all():
        return teams_collection.find()

    @staticmethod
    def find_by_game(game_id):
        return teams_collection.find({"juego_id": ObjectId(game_id)})

    @staticmethod
    def find_by_member(user_id):
        return teams_collection.find({"miembros": ObjectId(user_id)})

    @staticmethod
    def add_member(team_id, user_id):
        return teams_collection.update_one(
            {"_id": ObjectId(team_id)},
            {"$push": {"miembros": ObjectId(user_id)}}
        )

    @staticmethod
    def remove_member(team_id, user_id):
        return teams_collection.update_one(
            {"_id": ObjectId(team_id)},
            {"$pull": {"miembros": ObjectId(user_id)}}
        )

    @staticmethod
    def update_team(team_id, update_data):
        return teams_collection.update_one(
            {"_id": ObjectId(team_id)},
            {"$set": update_data}
        )

    @staticmethod
    def delete_team(team_id):
        return teams_collection.delete_one({"_id": ObjectId(team_id)}) 