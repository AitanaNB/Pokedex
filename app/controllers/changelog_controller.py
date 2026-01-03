# -*- coding: utf-8 -*-
"""
ChangeLog controller - Activity feed.
Shows user activities and notifications.
"""
from flask import Blueprint, render_template, request, session, jsonify
from app.utils.decorators import login_required
from config.database import get_db_context

changelog_bp = Blueprint('changelog', __name__)


@changelog_bp.route('/')
@login_required
def index():
    """Show changelog with user activities."""
    username = session.get('user')
    
    # Get activities from followed users
    with get_db_context() as conn:
        cursor = conn.cursor()
        
        # Get all activities (notifications)
        cursor.execute("""
            SELECT n.username, n.fecha, n.tipo, n.texto
            FROM notificaciones n
            INNER JOIN seguidores s ON n.username = s.seguido
            WHERE s.seguidor = ?
            ORDER BY n.fecha DESC
            LIMIT 50
        """, (username,))
        
        activities = []
        for row in cursor.fetchall():
            activities.append({
                'username': row['username'],
                'fecha': row['fecha'],
                'tipo': row['tipo'],
                'texto': row['texto']
            })
    
    return render_template('changelog/index.html', activities=activities)


@changelog_bp.route('/api/filter')
@login_required
def filter_activities():
    """Filter activities by username."""
    username = session.get('user')
    filter_user = request.args.get('user', '')
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        
        if filter_user:
            cursor.execute("""
                SELECT n.username, n.fecha, n.tipo, n.texto
                FROM notificaciones n
                INNER JOIN seguidores s ON n.username = s.seguido
                WHERE s.seguidor = ? AND n.username = ?
                ORDER BY n.fecha DESC
                LIMIT 50
            """, (username, filter_user))
        else:
            cursor.execute("""
                SELECT n.username, n.fecha, n.tipo, n.texto
                FROM notificaciones n
                INNER JOIN seguidores s ON n.username = s.seguido
                WHERE s.seguidor = ?
                ORDER BY n.fecha DESC
                LIMIT 50
            """, (username,))
        
        activities = []
        for row in cursor.fetchall():
            activities.append({
                'username': row['username'],
                'fecha': row['fecha'],
                'tipo': row['tipo'],
                'texto': row['texto']
            })
    
    return jsonify({'activities': activities})
