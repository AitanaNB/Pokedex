import unittest
from unittest.mock import patch, MagicMock
from app.repositories.GestorUsuario import (
    crearCuenta,
    validarUsuario,
    actualizarDatos,
    buscarPorUsername
)

class TestFunc1GestionUsuarios(unittest.TestCase):
    """
    Implementación de los casos de prueba para la Funcionalidad 1: Gestión de usuarios.
    """

    def setUp(self):
        """Configurar datos de prueba comunes"""
        self.username = "AshKetchum"
        self.email = "ash@pokedex.com"
        self.password_ok = "Pikachu123!" #Cumple: 8-16 chars, mayúscula, número y carácter especial
        self.password_debil = "pika"

    # -------------------------------------------------------------------------
    # REGISTRO (casos 1-5)
    # -------------------------------------------------------------------------
    @patch('app.repositories.GestorUsuario.get_db_context')
    @patch('app.repositories.GestorUsuario.hash_password')
    def test_01_registro_nombre_usuario_duplicado(self, mock_hash, mock_db_context):
        """
        Caso 1: Registro con nombre de usuario ya registrado.
        Resultado esperado: "El usuario ya existe"
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular que el usuario ya existe en la BD
        mock_cursor.fetchone.return_value = ('AshKetchum',)
        # Ejecutar función
        resultado = crearCuenta(self.username, self.email, self.password_ok, self.password_ok)
        # Verificar
        self.assertEqual(resultado, "El usuario ya existe")

    def test_02_registro_email_erroneo(self):
        """
        Caso 2: Registro con email con formato inválido.
        Resultado esperado: "Email inválido"
        """
        email_incorrecto = "ash_sin_arroba.com"
        resultado = crearCuenta(self.username, email_incorrecto, self.password_ok, self.password_ok)
        self.assertEqual(resultado, "Email inválido")

    def test_03_registro_contrasena_debil(self):
        """
        Caso 3: Contraseña no cumple estándares.
        Resultado esperado: Mensaje de error sobre contraseña débil
        """
        pass_debil = "pikachu123"
        resultado = crearCuenta(self.username, self.email, pass_debil, pass_debil)
        self.assertIn("La contraseña debe tener", resultado)

    def test_04_registro_contrasena_no_coincide(self):
        """
        Caso 4: Contraseña y verificación no coinciden.
        Resultado esperado: "Las contraseñas no coinciden"
        """
        resultado = crearCuenta(self.username, self.email, "Pass1!", "Pass2!")
        self.assertEqual(resultado, "Las contraseñas no coinciden")

    @patch('app.repositories.GestorUsuario.get_db_context')
    @patch('app.repositories.GestorUsuario.hash_password')
    def test_05_registro_exito(self, mock_hash, mock_db_context):
        """
        Caso 5: Registro exitoso.
        Resultado esperado: Mensaje de éxito con aprobación pendiente
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular que el usuario NO existe en la BD
        mock_cursor.fetchone.return_value = None
        resultado = crearCuenta(self.username, self.email, self.password_ok, self.password_ok)
        self.assertIn("Usuario registrado exitosamente", resultado)

    # -------------------------------------------------------------------------
    # LOGIN (casos 6-9)
    # -------------------------------------------------------------------------

    @patch('app.repositories.GestorUsuario.get_db_context')
    def test_06_login_usuario_no_existe(self, mock_db_context):
        """
        Caso 6: Login - usuario no registrado.
        Resultado esperado: None y "Usuario o contraseña incorrectos"
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular que el usuario NO existe
        mock_cursor.fetchone.return_value = None
        usuario, mensaje = validarUsuario("UsuarioFantasma", self.password_ok)
        self.assertIsNone(usuario)
        self.assertEqual(mensaje, "Usuario o contraseña incorrectos")

    @patch('app.repositories.GestorUsuario.check_password')
    @patch('app.repositories.GestorUsuario.get_db_context')
    def test_07_login_contrasena_incorrecta(self, mock_db_context, mock_check_pass):
        """
        Caso 7: Login - usuario existe pero contraseña incorrecta.
        Resultado esperado: None y "Usuario o contraseña incorrectos"
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular usuario encontrado
        mock_cursor.fetchone.return_value = {'username': self.username, 'contrasena': 'hash', 'aprobado': 1}
        # Simular verificación de contraseña fallida
        mock_check_pass.return_value = False
        usuario, mensaje = validarUsuario(self.username, "ClaveErronea")
        self.assertIsNone(usuario)
        self.assertEqual(mensaje, "Usuario o contraseña incorrectos")

    @patch('app.repositories.GestorUsuario.check_password')
    @patch('app.repositories.GestorUsuario.get_db_context')
    def test_08_login_cuenta_no_aprobada(self, mock_db_context, mock_check_pass):
        """
        Caso 8: Login - cuenta no validada por administrador.
        Resultado esperado: None y "Su cuenta está pendiente de aprobación"
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular usuario con aprobado = 0
        mock_cursor.fetchone.return_value = {'username': self.username, 'contrasena': 'hash', 'aprobado': 0}
        # Simular contraseña correcta
        mock_check_pass.return_value = True
        usuario, mensaje = validarUsuario(self.username, self.password_ok)
        self.assertIsNone(usuario)
        self.assertEqual(mensaje, "Su cuenta está pendiente de aprobación")

    @patch('app.repositories.GestorUsuario.check_password')
    @patch('app.repositories.GestorUsuario.get_db_context')
    def test_09_login_exito(self, mock_db_context, mock_check_pass):
        """
        Caso 9: Login exitoso.
        Resultado esperado: Usuario dict y "Inicio de sesión exitoso"
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular usuario válido y aprobado
        mock_cursor.fetchone.return_value = {'username': self.username, 'contrasena': 'hash', 'aprobado': 1, 'email': self.email}
        # Simular contraseña correcta
        mock_check_pass.return_value = True
        usuario, mensaje = validarUsuario(self.username, self.password_ok)
        self.assertIsNotNone(usuario)
        self.assertEqual(mensaje, "Inicio de sesión exitoso")

    # -------------------------------------------------------------------------
    # BUSCAR USUARIO (casos 10)
    # -------------------------------------------------------------------------
    def test_10_buscar_usuario_no_existe(self):
        """
        Caso 10: Gestionar amigos - busca un usuario y no existe ninguno con dicho nombre.
        Resultado esperado: Lista vacía (no hay error explícito en la función)
        """
        # Configurar mock para simular BD vacía
        with patch('app.repositories.GestorUsuario.get_db_context') as mock_db:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_db.return_value.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor

            # Simular que NO encuentra ningún usuario
            mock_cursor.fetchall.return_value = []  # Lista VACÍA
            # Ejecutar búsqueda
            usuarios_encontrados = buscarPorUsername(
                usuarioActual="AshKetchum",  # Usuario que hace la búsqueda
                query="cualquiera"  # Usuario que busca (no existe)
        )

        # Verificar que devuelve lista vacía
        self.assertEqual(usuarios_encontrados, [])
        self.assertEqual(len(usuarios_encontrados), 0)

    # -------------------------------------------------------------------------
    # ACTUALIZAR DATOS (casos 11-14)
    # -------------------------------------------------------------------------
    @patch('app.repositories.GestorUsuario.buscarUsuarioLogueado')
    def test_11_actualizar_email_erroneo(self, mock_buscar_user):
        """
        Caso 11: Actualizar datos - email erróneo.
        Resultado esperado: False y "Email inválido"
        """
        # Configurar mock de usuario existente
        mock_buscar_user.return_value = {
            'username': self.username, 'email': 'viejo@email.com',
            'foto': None, 'contrasena': 'hash'
        }
        exito, mensaje = actualizarDatos(self.username, "email_incorrecto", None, "", "")
        self.assertFalse(exito)
        self.assertEqual(mensaje, "Email inválido")

    @patch('app.repositories.GestorUsuario.buscarUsuarioLogueado')
    def test_12_actualizar_contrasena_debil(self, mock_buscar_user):
        """
        Caso 12: Actualizar contraseña demasiado débil.
        Resultado esperado: False y mensaje de error
        """
        # Configurar mock de usuario existente
        mock_buscar_user.return_value = {
            'username': self.username, 'email': self.email,
            'foto': None, 'contrasena': 'hash'
        }
        # Probamos "123", debe fallar por ser débil (longitud y falta de caracteres)
        exito, mensaje = actualizarDatos(self.username, self.email, None, "123", "123")

        self.assertFalse(exito)
        # Ajustamos el assert para que coincida con el mensaje
        self.assertIn("La contraseña debe tener", mensaje)

    @patch('app.repositories.GestorUsuario.buscarUsuarioLogueado')
    def test_13_actualizar_contrasena_no_coincide(self, mock_buscar_user):
        """
        Caso 13: Actualizar - contraseñas no coinciden.
        Resultado esperado: False y "Las contraseñas nuevas no coinciden"
        """
        # Configurar mock de usuario existente
        mock_buscar_user.return_value = {
            'username': self.username, 'email': self.email,
            'foto': None, 'contrasena': 'hash'
        }
        # Ejecutar función con contraseñas diferentes
        exito, mensaje = actualizarDatos(self.username, self.email, None, "NewPass1", "NewPass2")
        self.assertFalse(exito)
        self.assertEqual(mensaje, "Las contraseñas nuevas no coinciden")

    @patch('app.repositories.GestorUsuario.get_db_context')
    @patch('app.repositories.GestorUsuario.hash_password')
    @patch('app.repositories.GestorUsuario.buscarUsuarioLogueado')
    def test_14_actualizar_datos_exito(self, mock_buscar_user, mock_hash, mock_db_context):
        """
        Caso 14: Actualizar datos - todo correcto.
        Resultado esperado: True y "Datos actualizados exitosamente"
        """
        # Configuración DB mocks
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular update correcto
        mock_cursor.rowcount = 1
        # Configurar mock de usuario existente
        mock_buscar_user.return_value = {
            'username': self.username, 'email': "viejo@pokedex.com",
            'foto': None, 'contrasena': 'old_hash'
        }

        # Ejecutar función con datos válidos
        exito, mensaje = actualizarDatos(self.username, "nuevo@pokedex.com", "nueva_foto.png", "NewPass123!",
                                         "NewPass123!")

        self.assertTrue(exito)
        self.assertEqual(mensaje, "Datos actualizados exitosamente")


if __name__ == '__main__':
    unittest.main()