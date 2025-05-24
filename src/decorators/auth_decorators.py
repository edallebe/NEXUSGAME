from functools import wraps
from flask import session, redirect, url_for, flash, request
from models.user import User

def login_required(f):
    """
    Decorador que requiere que el usuario esté autenticado.
    Redirige al login si no hay sesión activa.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorador que requiere permisos de administrador.
    Verifica sesión activa Y rol de administrador.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Primero verificar si está logueado
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.login'))
        
        # Luego verificar el rol
        user = User.find_by_id(session['user_id'])
        if not user or user.get('role') != 'administrador':
            flash('No tienes permisos para acceder a esta página', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """
    Decorador flexible que permite especificar el rol requerido.
    Uso: @role_required('administrador') o @role_required('usuario')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debes iniciar sesión para acceder a esta página', 'error')
                return redirect(url_for('auth.login'))
            
            user = User.find_by_id(session['user_id'])
            if not user or user.get('role') != required_role:
                flash(f'Necesitas permisos de {required_role} para acceder', 'error')
                return redirect(url_for('main.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator