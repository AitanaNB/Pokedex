from unittest.mock import patch
from tests import TestBase
from config.database import get_db_context, init_database
import app.repositories.GestorUsuario as GestorUsuario

#si no se encuentra la ruta
#print("\n=== RUTAS DISPONIBLES EN FLASK ===")
#print(self.app.url_map)
#print("==================================\n")

#Funcionalidad 3: ChangeLog
class TestFuc3(TestBase):

    def setUp(self):
        # al importar TestBase hereda setup y teardown
        super().setUp()

        #no hacen falta pokemon de la api (por ahora)
        with patch('config.database._load_type_data'), \
            patch('config.database._load_species_data'):
            init_database()

        self.insertarDatosPruebas()

        #instertar datos de prueba
    def insertarDatosPruebas(self):
        with get_db_context() as conn:
            conn.execute(""" INSERT INTO usuario (username, email, contrasena)
                VALUES ('user1', 'user1@gmail.com', '123456')""")
            conn.execute(""" INSERT INTO usuario (username, email, contrasena)
                             VALUES ('user2', 'user2@gmail.com', '123456')""")
            conn.execute(""" INSERT INTO usuario (username, email, contrasena)
                             VALUES ('user3', 'user3@gmail.com', '123456')""")
            conn.execute(""" INSERT INTO seguidores (seguidor, seguido)
                             VALUES ('user1', 'user2')""")
            conn.execute(""" INSERT INTO seguidores (seguidor, seguido)
                             VALUES ('user1', 'user3')""")
            conn.commit()

    def generarNotificaciones(self, cantidad, usuario):
        """Genera cantidad notificaciones para un usuario, máximo 31"""
        with get_db_context() as conn:
            for i in range(cantidad):
                #fecha diferente cada una
                fecha = f"2026-01-{i+1:02d} 10:00:00"
                conn.execute(""" INSERT INTO notificaciones (username, fecha, tipo, texto)
                             VALUES (?, ?, 'seguido', ?)""", (usuario, fecha, f'{usuario} ha seguido a Test{i}'))


    def testAccesoSinLogin(self):
        #hacer petición get
        response = self.client.get('/changelog/')
        self.assertEqual(response.status_code, 302)  # 302, redirige al login

    def testAccesoConLogin(self):
        # iniciar sesión
        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'
        response = self.client.get('/changelog/')
        self.assertEqual(response.status_code, 200)  # 302, redirige al login

    def testSinNotificacion(self):
        #iniciar sesión
        with self.client.session_transaction() as sess:
            sess['user']='user1'
        response = self.client.get('/changelog/')
        self.assertEqual(response.status_code, 200, "La página debería cargar incluso sin notificaciones.")

        #verificar mensaje en la web, decode porque hay tildes :(
        self.assertIn('No hay actividades recientes. ¡Sigue a más usuarios para ver su actividad!', response.data.decode('utf-8'))

        #verificar json
        response_api=self.client.get('/changelog/api/notificaciones')
        self.assertEqual(response_api.status_code, 200)
        self.assertTrue(response_api.is_json)

        data = response_api.get_json()

        # Verificamos que 'activities' existe y es una lista VACÍA
        self.assertIn('activities', data)
        self.assertIsInstance(data['activities'], list)
        self.assertEqual(len(data['activities']), 0, "La lista de actividades debería estar vacía")

    def testConNotificaciones(self):
        self.generarNotificaciones(10, 'user2')
        #login como user1
        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'

        response = self.client.get('/changelog/api/notificaciones')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        cantidad_recibida = len(data['activities'])
        self.assertEqual(cantidad_recibida, 10,
                         f"Se esperaban 10 notificaciones, pero llegaron {cantidad_recibida}")

    def test20Notificaciones(self):
        self.generarNotificaciones(20, 'user2')
        #login como user1
        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'

        response = self.client.get('/changelog/api/notificaciones')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        cantidad_recibida = len(data['activities'])
        self.assertEqual(cantidad_recibida, 20,
                         f"Se esperaban 20 notificaciones como máximo, pero llegaron {cantidad_recibida}")

    def testMas20Notificaciones(self):
        self.generarNotificaciones(25, 'user2')

        #login como user1
        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'

        response = self.client.get('/changelog/api/notificaciones')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        cantidad_recibida = len(data['activities'])
        self.assertEqual(cantidad_recibida, 20,
                         f"Se esperaban 20 notificaciones como máximo, pero llegaron {cantidad_recibida}")

    def testFiltroSeguido(self):
        #función ya definida en GestorUsuario
        GestorUsuario.generarEvento('user2', 'seguido','textoX de user2')
        GestorUsuario.generarEvento('user3', 'captura', 'textoX')

        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'
        response = self.client.get('/changelog/api/notificaciones')
        data = response.get_json()
        items = data['activities']

        #Verificar que el filtro por "seguido" funciona
        seguidos= [i for i in items if i['tipo'] == 'seguido']
        self.assertTrue(len(seguidos)>0, "No se envía el tipo 'seguido' correctamente.")

    def testFiltroEquipo(self):
        #función ya definida en GestorUsuario
        GestorUsuario.generarEvento('user2', 'equipo','textoX de user2')
        GestorUsuario.generarEvento('user3', 'captura', 'textoX')

        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'
        response = self.client.get('/changelog/api/notificaciones')
        data = response.get_json()
        items = data['activities']

        #Verificar que el filtro por "seguido" funciona
        seguidos= [i for i in items if i['tipo'] == 'equipo']
        self.assertTrue(len(seguidos)>0, "No se envía el tipo 'seguido' correctamente.")

    def testFiltroCaptura(self):
        #función ya definida en GestorUsuario
        GestorUsuario.generarEvento('user2', 'seguido','textoX de user2')
        GestorUsuario.generarEvento('user3', 'captura', 'textoX')

        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'
        response = self.client.get('/changelog/api/notificaciones')
        data = response.get_json()
        items = data['activities']

        #Verificar que el filtro por "seguido" funciona
        seguidos= [i for i in items if i['tipo'] == 'seguido']
        self.assertTrue(len(seguidos)>0, "No se envía el tipo 'seguido' correctamente.")

    def testNotificacionAntigua(self):
        with get_db_context() as conn:
            # Orden diferente de notificaciones
            conn.execute("""
                         INSERT INTO notificaciones (username, fecha, tipo, texto)
                         VALUES ('user2', '2025-01-01 10:00:00', 'captura', 'Vieja'),
                                ('user2', '2026-01-15 10:05:00', 'equipo', 'Nueva'),
                                ('user2', '2026-01-01 10:10:00', 'seguido', 'Media')
                         """)
            conn.commit()
        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'

        response = self.client.get('/changelog/api/notificaciones')
        data = response.get_json()
        items = data['activities']

        #Verificar que aparecen en orden correcto
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0]['texto'], 'Nueva', "El primer elemento debería ser el más reciente")
        self.assertEqual(items[1]['texto'], 'Media')
        self.assertEqual(items[2]['texto'], 'Vieja', "El último elemento debería ser el más antiguo")

    def testDejarDeSeguir(self):
        with self.client.session_transaction() as sess:
            GestorUsuario.generarEvento('user2', 'seguido','textoX de user2')

        with self.client.session_transaction() as sess:
            sess['user'] = 'user1'

        response1=self.client.get('/changelog/api/notificaciones')
        self.assertEqual(len(response1.get_json()['activities']), 1)

        #user1 deja de seguir a user2
        with get_db_context() as conn:
            conn.execute("DELETE FROM seguidores WHERE seguidor='user1' AND seguido='user2'")
            conn.commit()

        #verificar que ya no aparece la notificación
        response2 = self.client.get('/changelog/api/notificaciones')
        datos_actualizados = response2.get_json()['activities']
        self.assertEqual(len(datos_actualizados), 0, "Al dejar de seguir, el feed debería vaciarse")