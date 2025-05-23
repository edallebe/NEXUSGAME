from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User

# Creamos un blueprint para autenticación
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    mensaje = request.args.get('mensaje', '')
    error = request.args.get('error', False)

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validaciones
        if password != confirm_password:
            return redirect(url_for('auth.register', mensaje="Las contraseñas no coinciden", error=True))

        # Verificar si el usuario ya existe
        if User.find_by_username(username):
            return redirect(url_for('auth.register', mensaje="El nombre de usuario ya está en uso", error=True))

        if User.find_by_email(email):
            return redirect(url_for('auth.register', mensaje="El email ya está registrado", error=True))

        # Crear nuevo usuario
        try:
            user = User(username, email, password)
            user.save()
            return redirect(url_for('auth.login', mensaje="Registro exitoso! Por favor inicia sesión"))
        except Exception as e:
            return redirect(url_for('auth.register', mensaje="Error al registrar usuario", error=True))

    return render_template('auth/register.html', mensaje=mensaje, error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = request.args.get('mensaje', '')
    error = request.args.get('error', False)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Buscar usuario
        user = User.find_by_username(username)
        if user and User.verify_password(user['password_hash'], password):
            # Guardar en sesión
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash('Has cerrado sesión exitosamente', "success")
            return redirect(url_for('main.index', mensaje="Has iniciado sesión correctamente!"))
        else:
            return redirect(url_for('auth.login', mensaje="Usuario o contraseña incorrectos", error=True))

    return render_template('auth/login.html', mensaje=mensaje, error=error)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index', mensaje="Has cerrado sesión")) 