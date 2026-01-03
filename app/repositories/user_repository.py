"""
Repositorio para gestionar operaciones de Usuario en la base de datos.
"""
from typing import Optional, List
from app.models import Usuario
from config.database import get_db_context


class UserRepository:
    """Repositorio para operaciones CRUD de usuarios."""
    
    @staticmethod
    def create(usuario: Usuario) -> bool:
        """
        Crea un nuevo usuario en la base de datos.
        
        Args:
            usuario: Instancia de Usuario a crear
            
        Returns:
            bool: True si se creó exitosamente
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO usuario (username, email, contrasena, foto, esAdmin, aprobado, cuentaTelegram)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (usuario.username, usuario.email, usuario.contrasena, usuario.foto,
                      int(usuario.esAdmin), int(usuario.aprobado), usuario.cuentaTelegram))
                return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
    
    @staticmethod
    def find_by_username(username: str) -> Optional[Usuario]:
        """
        Busca un usuario por su username.
        
        Args:
            username: Nombre de usuario a buscar
            
        Returns:
            Usuario si existe, None en caso contrario
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuario WHERE username = ?", (username,))
                row = cursor.fetchone()
                if row:
                    return Usuario(
                        username=row['username'],
                        email=row['email'],
                        contrasena=row['contrasena'],
                        foto=row['foto'],
                        esAdmin=bool(row['esAdmin']),
                        aprobado=bool(row['aprobado']),
                        cuentaTelegram=row['cuentaTelegram']
                    )
                return None
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None
    
    @staticmethod
    def find_by_email(email: str) -> Optional[Usuario]:
        """Busca un usuario por su email."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuario WHERE email = ?", (email,))
                row = cursor.fetchone()
                if row:
                    return Usuario(
                        username=row['username'],
                        email=row['email'],
                        contrasena=row['contrasena'],
                        foto=row['foto'],
                        esAdmin=bool(row['esAdmin']),
                        aprobado=bool(row['aprobado']),
                        cuentaTelegram=row['cuentaTelegram']
                    )
                return None
        except Exception as e:
            print(f"Error al buscar usuario por email: {e}")
            return None
    
    @staticmethod
    def get_all() -> List[Usuario]:
        """Obtiene todos los usuarios."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM usuario")
                rows = cursor.fetchall()
                return [Usuario(
                    username=row['username'],
                    email=row['email'],
                    contrasena=row['contrasena'],
                    foto=row['foto'],
                    esAdmin=bool(row['esAdmin']),
                    aprobado=bool(row['aprobado']),
                    cuentaTelegram=row['cuentaTelegram']
                ) for row in rows]
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
    
    @staticmethod
    def update(usuario: Usuario) -> bool:
        """Actualiza los datos de un usuario."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE usuario 
                    SET email = ?, contrasena = ?, foto = ?, esAdmin = ?, aprobado = ?, cuentaTelegram = ?
                    WHERE username = ?
                """, (usuario.email, usuario.contrasena, usuario.foto, int(usuario.esAdmin),
                      int(usuario.aprobado), usuario.cuentaTelegram, usuario.username))
                return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
    
    @staticmethod
    def delete(username: str) -> bool:
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
    def get_followers(username: str) -> List[Usuario]:
        """Obtiene los seguidores de un usuario."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.* FROM usuario u
                    INNER JOIN seguidores s ON u.username = s.seguidor
                    WHERE s.seguido = ?
                """, (username,))
                rows = cursor.fetchall()
                return [Usuario(
                    username=row['username'],
                    email=row['email'],
                    contrasena=row['contrasena'],
                    foto=row['foto'],
                    esAdmin=bool(row['esAdmin']),
                    aprobado=bool(row['aprobado']),
                    cuentaTelegram=row['cuentaTelegram']
                ) for row in rows]
        except Exception as e:
            print(f"Error al obtener seguidores: {e}")
            return []
    
    @staticmethod
    def get_following(username: str) -> List[Usuario]:
        """Obtiene los usuarios que sigue un usuario."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.* FROM usuario u
                    INNER JOIN seguidores s ON u.username = s.seguido
                    WHERE s.seguidor = ?
                """, (username,))
                rows = cursor.fetchall()
                return [Usuario(
                    username=row['username'],
                    email=row['email'],
                    contrasena=row['contrasena'],
                    foto=row['foto'],
                    esAdmin=bool(row['esAdmin']),
                    aprobado=bool(row['aprobado']),
                    cuentaTelegram=row['cuentaTelegram']
                ) for row in rows]
        except Exception as e:
            print(f"Error al obtener seguidos: {e}")
            return []
