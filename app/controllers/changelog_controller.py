# -*- coding: utf-8 -*-
"""
ChangeLog controller - Activity feed.
Shows user activities and notifications.
"""
from flask import Blueprint, render_template, session, jsonify
from app.utils.decorators import login_required
from config.database import get_db_context
import app.repositories.GestorUsuario as GestorUsuario

changelog_bp = Blueprint('changelog', __name__)

@changelog_bp.route('/')
@login_required
def index():
    """Muestra el changelog con todas las notificaciones."""
    username = session.get('user')
    activities = GestorUsuario.obtenerNotificaciones(username)

    return render_template('changelog/index.html', activities=activities)

@changelog_bp.route('/api/notificaciones')
@login_required
def getDatosBusqueda():
    """
    Devuelve datos en JSON para la búsqueda por usuario.
    Se filtra en el script de index.html
    """
    username = session.get('user')
    notificaciones = GestorUsuario.obtenerNotificaciones(username)

    return jsonify({'activities': notificaciones})


