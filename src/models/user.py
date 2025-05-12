from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src.config import Conexion

# Obtener la conexión a la base de datos
db = Conexion()
users_collection = db["usuarios"]

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()
        self.profile = {
            "avatar": None,
            "full_name": "",
            "bio": "",
            "favorite_games": [],
            "statistics": {
                "tournaments_played": 0,
                "tournaments_won": 0,
                "matches_played": 0,
                "win_rate": 0
            }
        }

    def save(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at,
            "profile": self.profile
        }
        return users_collection.insert_one(user_data)

    @staticmethod
    def find_by_username(username):
        return users_collection.find_one({"username": username})

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def verify_password(stored_password_hash, provided_password):
        return check_password_hash(stored_password_hash, provided_password) 