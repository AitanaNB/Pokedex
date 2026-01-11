"""
Controlador de autenticación.
Maneja las rutas de login, registro y gestión de usuarios.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET'])
@auth_bp.route('/login', methods=['GET'])
def login():
    """Muestra el formulario de login."""
    if 'user' in session:
        return redirect(url_for('auth.dashboard'))
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def login_post():
    """Procesa el login de usuario."""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    success, message, usuario = AuthService.login(username, password)

    if success and usuario:
        # Guardar información en la sesión
        session['user'] = usuario['username']
        session['email'] = usuario['email']
        session['is_admin'] = usuario['esAdmin']
        session['is_approved'] = usuario['aprobado']

        # Guardamos la URL de la foto en la sesión para usarla en las vistas
        session['foto'] = usuario['foto']

        flash(message, 'success')
        return redirect(url_for('auth.dashboard'))
    else:
        flash(message, 'danger')
        return render_template('login.html', error=message)


@auth_bp.route('/register', methods=['GET'])
def register():
    """Muestra el formulario de registro."""
    if 'user' in session:
        return redirect(url_for('auth.dashboard'))
    return render_template('register.html')


@auth_bp.route('/register', methods=['POST'])
def register_post():
    """Procesa el registro de un nuevo usuario."""
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    success, message = AuthService.register_user(username, email, password, confirm_password)

    if success:
        flash(message, 'success')
        return redirect(url_for('auth.login'))
    else:
        flash(message, 'danger')
        return render_template('register.html', error=message)


@auth_bp.route('/logout')
def logout():
    """Cierra la sesión del usuario."""
    session.clear()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/pending-approval')
def pending_approval():
    """Página que se muestra cuando un usuario no está aprobado."""
    return render_template('pending_approval.html')


@auth_bp.route('/dashboard')
def dashboard():
    """Dashboard principal con todas las funcionalidades."""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@auth_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    """Muestra el formulario de perfil y procesa la actualización de datos del usuario"""
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    username=session['user']

    if request.method == 'POST':
        # Recoger datos del formulario
        email = request.form.get('email', '').strip()
        foto = request.form.get('foto', '').strip()
        password = request.form.get('password', '')
        confirm_pass = request.form.get('confirm_password', '')
        # Llama al servicio
        success, message = AuthService.actualizar_datos(username, email, foto, password, confirm_pass)
        if success:
            flash(message, 'success')
            # Actualizar datos en sesión si cambiaron
            session['email'] = email
            session['foto'] = foto
        else:
            flash(message, 'danger')
        # Recargar la página para ver los cambios
        return redirect(url_for('auth.perfil'))

    # Método GET: obtener datos actuales para rellenar el formulario
    usuario=UserRepository.find_by_username(username)
    return render_template('user/perfil.html', usuario=usuario)