"""
Servicio de autenticación que maneja la lógica de negocio relacionada con usuarios.
"""
from typing import Optional, Tuple
from app.models import Usuario
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password, check_password
import re


class AuthService:
    """Servicio para operaciones de autenticación y gestión de usuarios."""
    
    @staticmethod
    def register_user(username: str, email: str, password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en el sistema.
        
        Args:
            username: Nombre de usuario deseado
            email: Email del usuario
            password: Contraseña
            confirm_password: Confirmación de contraseña
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validaciones
        if not username or not email or not password:
            return False, "Todos los campos son obligatorios"
        
        if password != confirm_password:
            return False, "Las contraseñas no coinciden"
        
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        
        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"
        
        # Validar formato de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return False, "Email inválido"
        
        # Verificar si el usuario ya existe
        existing_user = UserRepository.find_by_username(username)
        if existing_user:
            return False, "El nombre de usuario ya está en uso"
        
        existing_email = UserRepository.find_by_email(email)
        if existing_email:
            return False, "El email ya está registrado"
        
        # Crear usuario
        hashed_password = hash_password(password)
        usuario = Usuario(
            username=username,
            email=email,
            contrasena=hashed_password,
            esAdmin=False,
            aprobado=False  # Por defecto, los usuarios deben ser aprobados
        )
        
        success = UserRepository.create(usuario)
        if success:
            return True, "Usuario registrado exitosamente. Espera la aprobación de un administrador."
        else:
            return False, "Error al registrar usuario. Intenta nuevamente."
    
    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str, Optional[Usuario]]:
        """
        Autentica un usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            Tuple[bool, str, Optional[Usuario]]: (éxito, mensaje, usuario)
        """
        if not username or not password:
            return False, "Usuario y contraseña son obligatorios", None
        
        usuario = UserRepository.find_by_username(username)
        if not usuario:
            return False, "Usuario o contraseña incorrectos", None
        
        if not check_password(password, usuario.contrasena):
            return False, "Usuario o contraseña incorrectos", None
        
        if not usuario.aprobado and not usuario.esAdmin:
            return False, "Tu cuenta aún no ha sido aprobada por un administrador", None
        
        return True, "Inicio de sesión exitoso", usuario
    
    @staticmethod
    def change_password(username: str, old_password: str, new_password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            username: Nombre de usuario
            old_password: Contraseña actual
            new_password: Nueva contraseña
            confirm_password: Confirmación de nueva contraseña
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        if new_password != confirm_password:
            return False, "Las contraseñas no coinciden"
        
        if len(new_password) < 6:
            return False, "La nueva contraseña debe tener al menos 6 caracteres"
        
        usuario = UserRepository.find_by_username(username)
        if not usuario:
            return False, "Usuario no encontrado"
        
        if not check_password(old_password, usuario.contrasena):
            return False, "Contraseña actual incorrecta"
        
        # Actualizar contraseña
        usuario.contrasena = hash_password(new_password)
        success = UserRepository.update(usuario)
        
        if success:
            return True, "Contraseña actualizada exitosamente"
        else:
            return False, "Error al actualizar contraseña"
    
    @staticmethod
    def approve_user(admin_username: str, username_to_approve: str) -> Tuple[bool, str]:
        """
        Aprueba un usuario (solo administradores).
        
        Args:
            admin_username: Username del administrador
            username_to_approve: Username del usuario a aprobar
            
        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        admin = UserRepository.find_by_username(admin_username)
        if not admin or not admin.esAdmin:
            return False, "No tienes permisos para aprobar usuarios"
        
        usuario = UserRepository.find_by_username(username_to_approve)
        if not usuario:
            return False, "Usuario no encontrado"
        
        if usuario.aprobado:
            return False, "El usuario ya está aprobado"
        
        usuario.aprobado = True
        success = UserRepository.update(usuario)
        
        if success:
            return True, f"Usuario {username_to_approve} aprobado exitosamente"
        else:
            return False, "Error al aprobar usuario"
    
    @staticmethod
    def get_pending_users() -> list:
        """Obtiene usuarios pendientes de aprobación."""
        all_users = UserRepository.get_all()
        return [u for u in all_users if not u.aprobado and not u.esAdmin]
