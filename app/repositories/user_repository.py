"""
Repositorio para gestionar operaciones de Usuario en la base de datos.
"""
from typing import Optional, List, Dict, Any
from config.database import get_db_context
from app.repositories.notificacion_repository import NotificacionRepository
"repo que genera notificaciones"


class UserRepository:
    """Repositorio para operaciones CRUD de usuarios."""
    
    @staticmethod
    def registrarse(username, email, contrasena) -> bool:
        """
        Crea un nuevo usuario en la base de datos recibiendo parámetros individuales.
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO usuario (username, email, contrasena, esAdmin, aprobado)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, email, contrasena, 0, 0))
                return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
    @staticmethod
    def fila_a_dict(fila) -> Dict[str, Any]:
        if not fila:
            return None
        return {
            'username': fila['username'],
            'email': fila['email'],
            'contrasena': fila['contrasena'],
            'foto': fila['foto'],
            'esAdmin': bool(fila['esAdmin']),
            'aprobado': bool(fila['aprobado']),
        }
    @staticmethod
    def find_by_username(username: str) -> Optional[Dict[str, Any]]:
        """
        Busca un usuario por su username y devuelve un diccionario con sus datos.
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuario WHERE username = ?", (username,))
                row = cursor.fetchone()
                return UserRepository.fila_a_dict(row)
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None

    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Obtiene todos los usuarios (una lista de diccionarios)"""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuario")
                rows = cursor.fetchall()
                return [UserRepository.fila_a_dict(row) for row in rows]
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
    
    @staticmethod
    def actualizarDatos(username, email, foto, contrasena, esAdmin, aprobado) -> bool:
        """Actualiza los datos de un usuario."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE usuario 
                    SET email = ?, contrasena = ?, foto = ?, esAdmin = ?, aprobado = ?
                    WHERE username = ?
                """, (email, contrasena, foto, int(esAdmin), int(aprobado), username))
                return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False

    @staticmethod
    def borrarCuenta(username: str) -> bool:
        """Elimina un usuario."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM usuario WHERE username = ?", (username,))
                return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            return False
    
    @staticmethod
    def follow(seguidor: str, seguido: str) -> bool:
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
            NotificacionRepository.generarEvento(seguidor, "seguido", f"ha empezado a seguir a {seguido}")
            return True
        except Exception as e:
            print(f"Error al seguir usuario: {e}")
            return False
    
    @staticmethod
    def unfollow(seguidor: str, seguido: str) -> bool:
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
    
    @staticmethod
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
    
    @staticmethod
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


    @staticmethod
    def buscarUsuario(query: str) -> List[dict]:
        """Buscar usuarios que contengan el texto en su username."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuario WHERE username LIKE ?", (query,))
                rows = cursor.fetchone()
                return [{
                    'username': row['username'],
                    'foto': row['foto']
                } for row in rows]

        except Exception as e:
            print(f"Error al buscar usuarios: {e}")
            return []
