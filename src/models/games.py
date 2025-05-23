from config import Conexion

db = Conexion()
users_collection = db["usuarios"]
games_collection = db["games"]

class Game:
    def __init__(self, game, descripcion, categoria):
        self.game = game
        self.description = descripcion
        self.categoria = categoria
        self.profile_game={
            "img_logo": None,
            "img_portada": None
        }
    def save_game(self):
        game_data={
            "game":self.game,
            "descripcion":self.description,
            "categoria":self.categoria,
            "profile_game":self.profile_game
        }
        return games_collection.insert_one(game_data)