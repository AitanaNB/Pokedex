import sqlite3

import row

from config.database import get_db_context


def vincularUsuario(username, TelegramUsername):
    """
    Agrega el string TelegramUsername al campo cuentaTelegram de la tabla usuario 
    donde el username coincide.
    """
    try:
        # Abrimos el contexto de la base de datos
        with get_db_context() as conn:
            cursor = conn.cursor()

            # Definimos la consulta SQL con placeholders (?) por seguridad
            sql = "UPDATE usuario SET cuentaTelegram = ? WHERE username = ?"

            # Ejecutamos la operación
            cursor.execute(sql, (TelegramUsername, username))

            # Confirmamos los cambios en la base de datos
            conn.commit()

            # Opcional: Verificar si se actualizó algún registro
            if cursor.rowcount == 0:
                print(f"Advertencia: No se encontró ningún usuario con el nombre '{username}'.")
                return 0
            else:
                print(f"Éxito: Usuario '{username}' vinculado a '{TelegramUsername}'.")
            return 1
    except sqlite3.Error as e:
        print(f"Error al acceder a SQLite: {e}")
        return 0

def buscarUsuario(query: str):
    """Buscar usuarios que contengan el texto en su cuenta de Telegram."""
    try:
        with get_db_context() as conn:
            # Importante para acceder por nombre de columna
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Usamos % a los lados para buscar coincidencias parciales
            # Ejemplo: 'diego' encontrará '@diego_p'
            search_query = f"%{query}%"

            cursor.execute("SELECT username FROM usuario WHERE cuentaTelegram LIKE ?", (search_query,))

            row = cursor.fetchone()

            if row:
                print(f"Usuario encontrado: {row['username']}")
                return row['username']
            else:
                print("No se encontró ningún usuario.")
                return None

    except Exception as e:
        print(f"Error al buscar usuario: {e}")
        return None

def obtenerNotificaciones(username):
    """Obtiene notificaciones generadas por los usuarios a los que se sigue"""
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

def generarEvento(username, tipo, texto):
    """Generar una notificación y guardarla en BD"""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO notificaciones (username, fecha, tipo, texto)
                           VALUES (?, datetime('now'), ?, ?)
                           """, (username, tipo, texto))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error al generar evento de notificación: {e}")
        return False