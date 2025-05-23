from flask import Flask
from routes.main import main_bp
from routes.auth import auth_bp
from routes.games import games_bp
from routes.tournaments import tournaments_bp
from routes.teams import teams_bp

app = Flask(__name__)
    
# Configuración básica
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    
# Registrar blueprints
app.register_blueprint(main_bp)  # Rutas principales, sin prefijo
app.register_blueprint(auth_bp)  # Rutas de autenticación, prefijo /auth
app.register_blueprint(games_bp)
app.register_blueprint(tournaments_bp)
app.register_blueprint(teams_bp)

if __name__ == "__main__":
    app.run(debug=True)