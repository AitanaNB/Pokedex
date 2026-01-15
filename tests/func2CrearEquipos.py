import unittest
from app.repositories.equipo_repository import EquipoRepository

from app.models import Equipo
from app.models import Pokemon
from unittest.mock import patch, MagicMock
#Funcionalidad 2: Crear Equipos Pokémon

#Clases Mock para simular los modelos
class MockPokemon:
    def __init__(self, id):
        self.idPokemon = id

class MockEquipo:
    def __init__(self, nombre, username, pokemons=[]):
        self.nombre = nombre
        self.username = username
        self.pokemons = pokemons

class TestFunc2(unittest.TestCase):
    pokemon=Pokemon(
        idPokemon= 10,
        nombre= "Pikachu",
        ataque= 10,
        ataqueEsp= 10,
        def_= 2,
        defEsp= 5,
        vel= 30,
        vida= 20,
        nombreEspecie= "Especie",
        ataques = None
    )
    equipo = Equipo(
        idEquipo = None,
        nombre= "EquipoPrueba",
        fechaCreacion="01-01-2026",
        username = "Paco",
        pokemons = [pokemon]
    )

    # Caso 1: en web
    # Caso 2: en web
    # Caso 3: en web

    # Caso 4: Límite de equipos alcanzado (10)
    @patch('app.repositories.equipo_repository.get_db_context')
    def test4(self,mock_get_db_context):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        #simular que hay 10 equipos
        mock_cursor.fetchone.return_value = {'total':10}

        rdo=EquipoRepository.create(self.equipo)
        self.assertIsNone(rdo, "Debería rechazar la creación porque hay 10 equipos")

    # Caso 5: Crear equipo sin ningún Pokémon
    @patch('app.repositories.equipo_repository.get_db_context')
    def test5(self, mock_get_db_context):
        # Preparar
        e = Equipo(
            idEquipo=None,
            nombre="Equipo Vacío",
            fechaCreacion="01-01-2026",
            username="Paco",
            pokemons=[]  # <--- Lista vacía
        )
        # Ejecutar
        rdo = EquipoRepository.create(e)

        #tiene que devolver None
        self.assertIsNone(rdo, "El repositorio debería rechazar equipos sin Pokémon")

    # Caso 6: Crear equipo sin nombre
    @patch('app.repositories.equipo_repository.get_db_context')
    def test6(self, mock_get_db_context):
        # Preparar
        e = Equipo(
            idEquipo=None,
            nombre="",
            fechaCreacion="01-01-2026",
            username="Paco",
            pokemons=[self.pokemon]
        )
        # Ejecutar
        rdo = EquipoRepository.create(e)

        # tiene que devolver None
        self.assertIsNone(rdo, "El repositorio debería rechazar equipos sin nombre")


    # Caso 7:Crear equipo correctamente
    @patch('app.repositories.equipo_repository.get_db_context')
    @patch('app.repositories.equipo_repository.NotificacionRepository')
    def test7(self, mock_notif, mock_get_db_context):
            mock_conn=MagicMock()
            mock_cursor=MagicMock()
            mock_get_db_context.return_value.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor

            #tiene 1 equipo
            mock_cursor.fetchone.return_value = {'total': 1}
            #Simular id 10 al nuevo equipo
            mock_cursor.lastrowid= 10

            #Datos de entrada
            poke=self.pokemon
            e = Equipo(
                idEquipo=None,
                nombre="Equipo Bueno",
                fechaCreacion="01-01-2026",
                username="Paco",
                pokemons=[poke]
            )

            rdo=EquipoRepository.create(e)
            self.assertEqual(rdo,10)

            #Verificar INSERT de equipo
            #llamada 0 es el count, 1 insert into equipo
            self.assertTrue(mock_cursor.execute.called)
            args_equipo = mock_cursor.execute.call_args_list[1][0][0]
            self.assertIn("INSERT INTO equipo", args_equipo)

            # Verificar INSERT de pokemon (equipo_pokemon)
            args_poke = mock_cursor.execute.call_args_list[2][0][0]
            self.assertIn("INSERT INTO equipo_pokemon", args_poke)

            # Verificar COMMIT
            mock_conn.commit.assert_called_once()

            # Verificar NOTIFICACIÓN, username, tipo y texto
            mock_notif.generarEvento.assert_called_once_with(
                "Paco",
                "equipo",
                "Paco ha creado el equipo Equipo Bueno."
            )

    # Caso 8: en web

    # Caso 9: Añadir Pokémon a equipo
    @patch('app.repositories.equipo_repository.get_db_context')
    @patch('app.repositories.equipo_repository.NotificacionRepository')
    def test9(self, mock_notif, mock_get_db_context):
        # 1. Configurar Mocks
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        #side effect con mock, porque se usa el mismo cursor
        mock_cursor.fetchone.side_effect =[
            {'count': 1},
            {'usuario': 'Paco', 'equipo': 'Equipo Bueno', 'pokemon': 'Pikachu'}
        ]
        rdo=EquipoRepository.add_pokemon(10,25)
        self.assertTrue(rdo, "Debería devolver true al añadir correctamente")

        #verificar la notificación
        mock_notif.generarEvento.assert_called_once_with(
            "Paco",
            "captura",
            "Paco ha añadido un Pikachu en el equipo Equipo Bueno."
        )

    # Caso 10: Añadir Pokémon en equipo con ya 6 Pokémon
    @patch('app.repositories.equipo_repository.get_db_context')
    def test10(self,mock_get_db_context):
        # 1. Configurar Mocks
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {'count':6}
        rdo = EquipoRepository.add_pokemon(10, 25)
        self.assertFalse(rdo, "Debería devolver false si hay más de 6 pokemon")


    # Caso 11: Eliminar Pokémon de equipo
    @patch('app.repositories.equipo_repository.get_db_context')
    def test11(self, mock_get_db_context):
        #1 configurar mocks
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        rdo = EquipoRepository.remove_pokemon(10,25)
        self.assertTrue(rdo, "Debería devolver true al eliminar")

        # Verificar sentencia DELETE
        args_delete = mock_cursor.execute.call_args[0][0]
        self.assertIn("DELETE FROM equipo_pokemon", args_delete)

        # Verificar parámetros (equipo 10, pokemon 25)
        args_params = mock_cursor.execute.call_args[0][1]
        self.assertEqual(args_params, (10, 25))

        # Verificar Commit
        mock_conn.commit.assert_called_once()
    # Caso 12: Añadir un Pokémon de la misma especie al mismo equipo
   #patch('app.repositories.equipo_repository.get_db_context')
   #def test12(self, mock_get_db_context):

    # Caso 13: cambiar nombre del equipo
    @patch('app.repositories.equipo_repository.get_db_context')
    def test13(self, mock_get_db_context):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        nuevoNombre="Nombre cambiado"
        rdo= EquipoRepository.update_nombre(10,nuevoNombre)

        self.assertTrue(rdo, "Debería devolver true al actualizar el nombre")

        #verifical el update
        args_update = mock_cursor.execute.call_args[0][0]  # La query SQL
        params_update = mock_cursor.execute.call_args[0][1]  # Los datos (?, ?)

        self.assertIn("UPDATE equipo SET nombre", args_update)
        self.assertEqual(params_update, (nuevoNombre, 10))

        # Verificar que se guardaron los cambios
        mock_conn.commit.assert_called_once()
    # Caso 14: en web
    # Caso 15: en web
    # Caso 16: en web
    # Caso 17: Eliminar equipo
    @patch('app.repositories.equipo_repository.get_db_context')
    def test17(self, mock_get_db_context):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_context.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        rdo=EquipoRepository.delete(10)
        self.assertTrue(rdo, "Debería devolver true al eliminar")

        #verificar delete de ta tabla equipo
        found_delete = False
        for call in mock_cursor.execute.call_args_list:
            if "DELETE FROM equipo" in call[0][0]:
                found_delete = True
                break
        self.assertTrue(found_delete)
        mock_conn.commit.assert_called_once()
        #no hace falta mirar equipo_pokemon, tiene borrado en cascada.

    # Caso 18: en web
    # Caso 19: en web
    # Caso 20: en web