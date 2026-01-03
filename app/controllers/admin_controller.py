# -*- coding: utf-8 -*-
"""
Admin controller - User management.
Handles user administration, approval, and followers.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.decorators import login_required, admin_required
from app.repositories.user_repository import UserRepository

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/usuarios')
@login_required
def usuarios():
    """Show users management page."""
    is_admin = session.get('is_admin', False)
    
    if is_admin:
        # Admin view: all users
        users = UserRepository.get_all()
        pending_users = [u for u in users if not u.aprobado]
        approved_users = [u for u in users if u.aprobado]
        return render_template('admin/usuarios.html', 
                             pending_users=pending_users,
                             approved_users=approved_users,
                             is_admin=True)
    else:
        # Regular user view: own profile and followers
        username = session.get('user')
        user = UserRepository.find_by_username(username)
        followers = UserRepository.get_followers(username)
        following = UserRepository.get_following(username)
        return render_template('admin/usuarios.html',
                             user=user,
                             followers=followers,
                             following=following,
                             is_admin=False)


@admin_bp.route('/usuarios/aprobar/<username>', methods=['POST'])
@admin_required
def aprobar_usuario(username):
    """Approve a user account."""
    from app.services.auth_service import AuthService
    admin_username = session.get('user')
    success, message = AuthService.approve_user(admin_username, username)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/eliminar/<username>', methods=['POST'])
@admin_required
def eliminar_usuario(username):
    """Delete a user account."""
    success = UserRepository.delete(username)
    if success:
        flash(f'Usuario {username} eliminado correctamente', 'success')
    else:
        flash('Error al eliminar usuario', 'danger')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/seguir/<username>', methods=['POST'])
@login_required
def seguir_usuario(username):
    """Follow a user."""
    current_user = session.get('user')
    success = UserRepository.follow(current_user, username)
    if success:
        flash(f'Ahora sigues a {username}', 'success')
    else:
        flash('Error al seguir usuario', 'danger')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/dejar-seguir/<username>', methods=['POST'])
@login_required
def dejar_seguir_usuario(username):
    """Unfollow a user."""
    current_user = session.get('user')
    success = UserRepository.unfollow(current_user, username)
    if success:
        flash(f'Has dejado de seguir a {username}', 'success')
    else:
        flash('Error al dejar de seguir', 'danger')
    return redirect(url_for('admin.usuarios'))
