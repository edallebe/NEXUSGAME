from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Conexion
from bson.objectid import ObjectId

# Obtener la conexión a la base de datos
db = Conexion()
users_collection = db["usuarios"]

class User:
    def __init__(self, username, email, password, role="usuario"):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.created_at = datetime.utcnow()
        # NUEVO: Campo de rol con valor por defecto
        self.role = role  # "administrador" o "usuario"
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
            "role": self.role,  # NUEVO: Guardar rol en BD
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
    def find_by_id(user_id):
        return users_collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def verify_password(stored_password_hash, provided_password):
        return check_password_hash(stored_password_hash, provided_password)
    
    # NUEVO: Métodos para gestión de roles
    @staticmethod
    def update_role(user_id, new_role):
        """Actualiza el rol de un usuario"""
        return users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"role": new_role}}
        )
    
    @staticmethod
    def get_admins():
        """Obtiene todos los administradores"""
        return list(users_collection.find({"role": "administrador"}))
    
    @staticmethod
    def get_users():
        """Obtiene todos los usuarios regulares"""
        return list(users_collection.find({"role": "usuario"}))