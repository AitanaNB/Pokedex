"""
Repositorio para gestionar la generación de notificaciones en la base de datos.
"""
from typing import Optional, List
from app.models import Notificacion
from config.database import get_db_context

class NotificacionRepository:
    @staticmethod
    def generarEvento(username, tipo, texto):
        "guardar notificación en la base de datos"
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                               INSERT INTO notificaciones (username, tipo, texto, fecha)
                               VALUES (?, ?, ?, datetime('now'))
                               """, (username, tipo, texto))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al generar evento de notificación: {e}")
            return False