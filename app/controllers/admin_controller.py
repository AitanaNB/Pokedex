# -*- coding: utf-8 -*-
"""
Admin controller - User management.
Handles user administration, approval, and followers.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.decorators import login_required, admin_required
#from app.repositories.user_repository import UserRepository
from app.controllers import Pokedex

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/usuarios')
@login_required
def usuarios():
    """Mostrar página de gestión de usuarios."""
    is_admin = session.get('is_admin', False)
    username = session.get('user')

    if is_admin:
        # Admin view: all users
        pending_users = Pokedex.obtenerCuentasPendientes()
        approved_users = Pokedex.obtenerCuentasAprobadas()
        return render_template('admin/usuarios.html', 
                             pending_users=pending_users,
                             approved_users=approved_users,
                             is_admin=True)
    else:
        # Lógica para usuario normal
        user = Pokedex.buscarUsuarioLogueado(username)

        # Variables iniciales
        followers = []
        following = []
        search_results = []
        following_names = []

        # Parámetros de la URL
        view_mode = request.args.get('view', 'perfil')  # por defecto 'perfil'
        search_query = request.args.get('search', '').strip()

        # 1. Búsqueda
        if search_query:
            view_mode = 'search'
            search_results = Pokedex.buscarPorUsername(user['username'], search_query)

            # Necesitamos saber a quién seguimos para mostrar el botón correcto
            following_data = Pokedex.get_following(username)
            # Creamos una lista de nombres
            following_names = [u['username'] for u in following_data]

        # 2. Si quiere ver a quién sigue
        elif view_mode == 'following':
            following = Pokedex.get_following(username)
        # 3. Si quiere ver a sus seguidores
        elif view_mode == 'followers':
            followers = Pokedex.get_followers(username)

        return render_template('admin/usuarios.html',
                               user=user,
                               followers=followers,
                               following=following,
                               search_results=search_results,  # Resultados de búsqueda
                               search_query=search_query,
                               following_names=following_names,  # Lista de strings (para botones dinámicos)
                               is_admin=False,
                               view_mode=view_mode)



@admin_bp.route('/usuarios/aprobar/<username>', methods=['POST'])
@admin_required
def aprobar_usuario(username):
    success, message = Pokedex.aprobarCuenta(username)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/eliminar/<username>', methods=['POST'])
@admin_required
def eliminar_usuario(username):
    success = Pokedex.borrarCuenta(username)
    if success:
        flash(f'Usuario {username} eliminado correctamente', 'success')
    else:
        flash('Error al eliminar usuario', 'danger')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/seguir/<username>', methods=['POST'])
@login_required
def seguir_usuario(username):
    current_user = session.get('user')
    success = Pokedex.seguir(current_user, username)
    if success:
        flash(f'Ahora sigues a {username}', 'success')
    else:
        flash('Error al seguir usuario', 'danger')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/dejar-seguir/<username>', methods=['POST'])
@login_required
def dejar_seguir_usuario(username):
    current_user = session.get('user')
    success = Pokedex.dejarDeSeguir(current_user, username)
    if success:
        flash(f'Has dejado de seguir a {username}', 'success')
    else:
        flash('Error al dejar de seguir', 'danger')
    return redirect(url_for('admin.usuarios'))
