"""
Servicio de autenticación que maneja la lógica de negocio relacionada con usuarios.
"""
from typing import Optional, Tuple, Dict, Any
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
        if UserRepository.find_by_username(username):
            return False, "El nombre de usuario ya está en uso"
        
        # Crear usuario
        hashed_password = hash_password(password)
        
        success = UserRepository.registrarse(username,email,hashed_password)
        if success:
            return True, "Usuario registrado exitosamente. Espera la aprobación de un administrador."
        else:
            return False, "Error al registrar usuario. Intenta nuevamente."
    
    @staticmethod
    def login(username: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Autentica un usuario manejando diccionarios en lugar de objetos.
        """
        if not username or not password:
            return False, "Usuario y contraseña son obligatorios", None
        # Obtener el diccionario del user_repository
        usuario = UserRepository.find_by_username(username)
        if not usuario:
            return False, "Usuario o contraseña incorrectos", None
        
        if not check_password(password, usuario['contrasena']):
            return False, "Usuario o contraseña incorrectos", None
        
        if not usuario['aprobado'] and not usuario['esAdmin']:
            return False, "Tu cuenta aún no ha sido aprobada por un administrador", None
        
        return True, "Inicio de sesión exitoso", usuario

    @staticmethod
    def aprobarCuenta(admin_username:str, usuarioSeleccionado: str) -> Tuple[bool, str]:
        """
        Aprueba un usuario (solo administradores).
        """
        admin = UserRepository.find_by_username(admin_username)
        if not admin or not admin['esAdmin']:
            return False, "No tienes permisos para aprobar usuarios"

        usuario = UserRepository.find_by_username(usuarioSeleccionado)
        if not usuario:
            return False, "Usuario no encontrado"

        if usuario['aprobado']:
            return False, "El usuario ya está aprobado"

        success = UserRepository.actualizarDatos(usuario['username'], usuario['email'], usuario['foto'], usuario['contrasena'], 0, 1)

        if success:
            return True, f"Usuario {usuarioSeleccionado} aprobado exitosamente"
        else:
            return False, "Error al aprobar usuario"
    
    @staticmethod
    def obtenerCuentasPdtes() -> list:
        """Obtiene usuarios pendientes de aprobación."""
        all_users = UserRepository.get_all()
        return [u for u in all_users if not u['aprobado'] and not u['esAdmin']]

    @staticmethod
    def actualizar_datos(username:str, email:str, foto:str, password: str=None, confirmar_pass: str=None) -> Tuple[bool, str]:
        """Actualiza los datos del usuario logueado"""
        # 1. Buscar usuario actual
        usuario = UserRepository.find_by_username(username)
        if not usuario:
            return False, "Usuario no encontrado"

        email_actual = usuario['email']
        contrasena_actual = usuario['contrasena']
        foto_actual = usuario['foto']

        # 2. Validar email
        if email!=email_actual:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                return False, "Email inválido"
            email_actual = email

        # 3. Actualizar foto
        if foto:
            foto_actual = foto

        # 4. Actualizar contraseña (sólo si el usuario escribió algo)
        if password:
            if password != confirmar_pass:
                return False, "Las contraseñas nuevas no coinciden"
            if len(password) < 6:
                return False, "La contraseña debe tener al menos 6 caracteres"
            contrasena_actual = hash_password(password)

        # 5. Guardar en la base de datos
        correcto=UserRepository.actualizarDatos(username,email_actual,foto_actual, contrasena_actual, usuario['esAdmin'], usuario['aprobado'])
        if correcto:
            return True, "Datos actualizados exitosamente"
        else:
            return False, "Error al actualizar datos"