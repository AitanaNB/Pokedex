"""
Decoradores para proteger rutas y requerir autenticación.
"""
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    Decorador que requiere que el usuario esté autenticado.
    Redirige a login si no lo está.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorador que requiere que el usuario sea administrador.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('auth.login'))
        
        if not session.get('is_admin', False):
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('pokedex.index'))
        return f(*args, **kwargs)
    return decorated_function


def approved_required(f):
    """
    Decorador que requiere que el usuario esté aprobado por un admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('auth.login'))
        
        if not session.get('is_approved', False):
            flash('Tu cuenta aún no ha sido aprobada por un administrador', 'info')
            return redirect(url_for('auth.pending_approval'))
        return f(*args, **kwargs)
    return decorated_function
