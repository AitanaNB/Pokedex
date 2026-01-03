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
    """Show changelog with user activities."""
    username = session.get('user')
    activities = get_user_feed(username)
    return render_template('changelog/index.html', activities=activities)

@changelog_bp.route('/api/filter')
@login_required
def get_all_activities():
    """
    API endpoint that returns ALL activities as JSON.
    The filtering (by type) will be handled by the Client (JavaScript).
    """
    username = session.get('user')

    # Obtenemos todo el feed sin filtrar por tipo
    activities = get_user_feed(username)

    return jsonify({'activities': activities})

def get_user_feed(username):
    """Helper function to fetch the feed from DB"""
    activities = []

    with get_db_context() as conn:
        cursor = conn.cursor()

        # CONSULTA LIMPIA:
        # Solo filtramos por 's.seguidor' para seguridad (ver solo mis amigos).
        # NO hay WHERE n.tipo = ... ni WHERE n.username = ...
        cursor.execute("""
                       SELECT n.username, n.fecha, n.tipo, n.texto
                       FROM notificaciones n
                                INNER JOIN seguidores s ON n.username = s.seguido
                       WHERE s.seguidor = ?
                       ORDER BY n.fecha DESC LIMIT 50
                       """, (username,))

        for row in cursor.fetchall():
            activities.append({
                'username': row['username'],
                'fecha': row['fecha'],
                'tipo': row['tipo'],  # Este campo es el que JS leerá para filtrar
                'texto': row['texto']
            })

    return activities
