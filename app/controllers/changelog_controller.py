# -*- coding: utf-8 -*-
"""
ChangeLog controller - Activity feed.
Shows user activities and notifications.
"""
from flask import Blueprint, render_template, session, jsonify
from app.utils.decorators import login_required
from config.database import get_db_context

changelog_bp = Blueprint('changelog', __name__)


@changelog_bp.route('/')
@login_required
def index():
    """Muestra el changelog con todas las notificaciones."""
    username = session.get('user')
    activities = obtenerNotificaciones(username)
    #devuelve el html completo
    return render_template('changelog/index.html', activities=activities)

@changelog_bp.route('/api/notificaciones')
@login_required
def getDatosBusqueda():
    """
    Devuelve datos en JSON para la búsqueda por usuario.
    Se filtra en el script de index.html
    """
    username = session.get('user')
    notificaciones = obtenerNotificaciones(username)

    return jsonify({'activities': notificaciones})

def obtenerNotificaciones(username):
    """función que conecta con la base de datos."""
    notificaciones = []

    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT n.username, n.fecha, n.tipo, n.texto
                       FROM notificaciones n
                                INNER JOIN seguidores s ON n.username = s.seguido
                       WHERE s.seguidor = ?
                       ORDER BY n.fecha DESC LIMIT 20
                       """, (username,))

        for row in cursor.fetchall():
            notificaciones.append({
                'username': row['username'],
                'fecha': row['fecha'],
                'tipo': row['tipo'],  # Este campo es el que JS leerá para filtrar
                'texto': row['texto']
            })

    return notificaciones
