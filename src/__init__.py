from flask import Flask
from src.routes.main import main_bp
from src.routes.auth import auth_bp
from src.routes.games import games_bp

def create_app():
    app = Flask(__name__)
    
    # Configuración básica
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    
    # Registrar blueprints
    app.register_blueprint(main_bp)  # Rutas principales, sin prefijo
    app.register_blueprint(auth_bp)  # Rutas de autenticación, prefijo /auth
    app.register_blueprint(games_bp) # Rutas de juegos, prefijo /games
    
    return app 