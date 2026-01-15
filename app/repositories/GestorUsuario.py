import sqlite3

from config.database import get_db_context
from app.utils.security import hash_password, check_password
from typing import Optional, List, Dict, Any
import re


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

def crearCuenta(username, email, password, confirm_password):
    if not username or not email or not password:
        return "Todos los campos son obligatorios"

    if password != confirm_password:
        return "Las contraseñas no coinciden"

    if len(username) < 3:
        return "El nombre de usuario debe tener al menos 3 caracteres"

    if len(password) < 6:
        return "La contraseña debe tener al menos 6 caracteres"

    # Validar email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return "Email inválido"

    with get_db_context() as conn:
        cursor = conn.cursor()

        # 1. Verificar si existe
        cursor.execute("SELECT username FROM USUARIO WHERE username = ?", (username,))
        if cursor.fetchone():
            return "El usuario ya existe"
        # Crear usuario
        hashed_password = hash_password(password)
        # 2. Insertar
        cursor.execute("""
            INSERT INTO USUARIO(username, email, contrasena, esAdmin, aprobado) 
            VALUES (?, ?, ?, 0, 0)
        """, (username, email, hashed_password))

    return "Usuario registrado exitosamente. Espera la aprobación de un administrador."


def validarUsuario(username, password):
    """Valida las credenciales del usuario. Devuelve el registro del usuario o None"""
    with get_db_context() as conn:
        cursor = conn.cursor()
        # Obtenemos el usuario por username
        cursor.execute("SELECT * FROM USUARIO WHERE username = ?", (username,))
        usuario = cursor.fetchone()

        # Si no se encuentra el usuario
        if not usuario:
            return None, "Usuario o contraseña incorrectos"

        # Convertir a diccionario
        usuario_dicc = dict(usuario)

        # Verificar contraseña usando check_password
        if not check_password(password, usuario_dicc['contrasena']):
            return None, "Usuario o contraseña incorrectos"

        # Verificar si la cuenta está aprobada
        if usuario_dicc.get('aprobado') == 0:
            return None, "Su cuenta está pendiente de aprobación"

        return usuario_dicc, "Inicio de sesión exitoso"


def actualizarDatos(username, email, foto, password, confirm_pass) -> tuple:
    """Actualiza los datos del usuario logueado"""
    # 1. Buscar usuario actual
    usuario = buscarUsuarioLogueado(username)
    if not usuario:
        return False, "Usuario no encontrado"

    email_actual = usuario['email']
    contrasena_actual = usuario['contrasena']
    foto_actual = usuario['foto']

    # 2. Validar email
    if email != email_actual:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return False, "Email inválido"
        email_actual = email

    # 3. Actualizar foto
    if foto:
        foto_actual = foto

    # 4. Actualizar contraseña (sólo si el usuario escribió algo)
    if password:
        if password != confirm_pass:
            return False, "Las contraseñas nuevas no coinciden"
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        contrasena_actual = hash_password(password)

    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuario 
                SET email = ?, contrasena = ?, foto = ?
                WHERE username = ?
            """, (email, contrasena_actual, foto, username))
            if cursor.rowcount > 0:
                return True, "Datos actualizados exitosamente"
            else:
                return False, "No se ha actualizado su usuario"
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False, f"Error al actualizar usuario: {e}"

def aprobarCuenta(username) -> tuple:
    """Activa cuenta de un usuario en BD"""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuario 
                SET APROBADO = ?
                WHERE username = ?
                """, (1, username ))
            conn.commit()
        if cursor.rowcount > 0:
            return True, f"Usuario {username} aprobado exitosamente"
        else:
            return False, "Usuario no encontrado"
    except Exception as e:
        print(f"Error al aprobar usuario: {e}")
        return False, f"Error: {str(e)}"

def borrarCuenta(username):
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuario WHERE username = ?", (username,))
            conn.commit()

            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False

def buscarUsuarioLogueado(username: str) -> Optional[Dict[str, Any]]:
    """
    Busca un usuario por su username y devuelve un diccionario con sus datos.
    """
    try:
        with get_db_context() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE username = ?", (username,))
            row = cursor.fetchone()
            return {
                'username': row['username'],
                'email': row['email'],
                'foto': row['foto'],
                'contrasena': row['contrasena']
            }
    except Exception as e:
        print(f"Error al buscar usuario: {e}")
        return None

def obtenerTodosUsuarios() -> List[Dict[str, Any]]:
    """Obtiene todos los usuarios (una lista de diccionarios)"""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario")
            rows = cursor.fetchall()
            return [{
                'username': row['username'],
                'email': row['email'],
                'aprobado': row['aprobado']
            } for row in rows]
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def obtenerCuentasPendientes():
    users = obtenerTodosUsuarios()
    cuentasPendientes = [u for u in users if not u['aprobado']]
    return cuentasPendientes

def obtenerCuentasAprobadas():
    users = obtenerTodosUsuarios()
    cuentasAprobadas = [u for u in users if u['aprobado']]
    return cuentasAprobadas

def seguir(seguidor: str, seguido: str) -> bool:
    """Crea una relación de seguimiento entre dos usuarios."""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO seguidores (seguidor, seguido)
                    VALUES (?, ?)
                """, (seguidor, seguido))
            conn.commit()
        # generar evento notificación
        generarEvento(seguidor, "seguido", f"ha empezado a seguir a {seguido}")
        return True
    except Exception as e:
        print(f"Error al seguir usuario: {e}")
        return False

def dejarDeSeguir(seguidor: str, seguido: str) -> bool:
    """Elimina una relación de seguimiento."""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    DELETE FROM seguidores WHERE seguidor = ? AND seguido = ?
                """, (seguidor, seguido))
            return True
    except Exception as e:
        print(f"Error al dejar de seguir: {e}")
        return False

def get_followers(username: str) -> List[dict]:
    """Obtiene los seguidores de un usuario."""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT u.username, u.foto FROM usuario u
                    INNER JOIN seguidores s ON u.username = s.seguidor
                    WHERE s.seguido = ?
                """, (username,))
            rows = cursor.fetchall()
            return [{
                'username': row['username'],
                'foto': row['foto']
            } for row in rows]
    except Exception as e:
        print(f"Error al obtener seguidores: {e}")
        return []

def get_following(username: str) -> List[dict]:
    """Obtiene los usuarios que sigue un usuario."""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT u.username, u.foto FROM usuario u
                    INNER JOIN seguidores s ON u.username = s.seguido
                    WHERE s.seguidor = ?
                """, (username,))
            rows = cursor.fetchall()
            return [{
                'username': row['username'],
                'foto': row['foto']
            } for row in rows]
    except Exception as e:
        print(f"Error al obtener seguidos: {e}")
        return []

def buscarPorUsername(usuarioActual, query):
    """Buscar usuarios que contengan el texto en su username."""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            search_query = f"%{query}%"
            cursor.execute("""SELECT username, foto FROM usuario 
                           WHERE username LIKE ? 
                           AND username != ? 
                           AND aprobado = 1 
                           AND esAdmin = 0
                           ORDER BY username""", (search_query, usuarioActual))
            rows = cursor.fetchall()
            return [{
                'username': row['username'],
                'foto': row['foto']
            } for row in rows]

    except Exception as e:
        print(f"Error al buscar usuarios: {e}")
        return []