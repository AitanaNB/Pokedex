import unittest
from app.repositories.GestorEquipo import GestorEquipo
from unittest.mock import patch, MagicMock, ANY

#Funcionalidad 2: Crear Equipos Pokémon

class TestFunc2(unittest.TestCase):

    # Caso 1: ver equipos
    @patch("app.repositories.GestorEquipo.GestorEquipo.get_equipo_pokemon")
    @patch("app.repositories.GestorEquipo.GestorEquipo.get_especie_details")
    @patch("app.repositories.GestorEquipo.get_db_context")
    def test1_ver_equipos(self, mock_db, mock_especie, mock_pokemons):
        print(f"\n \n ############### Caso 1.1: Ver los equipos del usuario cuando tiene 1 equipo sin Pokémons ############## \n")
       
        # Mock de conexión y cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular que el usuario tiene un equipo en la BD
        mock_cursor.fetchall.return_value = [
            {'idEquipo': 1, 'nombre': 'Equipo 1', 'fechaCreacion':'16/1/2026','username': 'Paco'}
        ]

        # Simular que el equipo no tiene Pokémons
        mock_pokemons.return_value = []

        mock_especie.return_value = {}

        #Ejecutar el método que devuelve los equipos para mostrarlos
        resultados = GestorEquipo.get_user_equipos("Paco")
        
        print(resultados,f"\n \n")

        #Comprobar un equipo
        self.assertEqual(len(resultados), 1)
        #Comprobar info correcta
        equipo = resultados[0]
        self.assertEqual(equipo['idEquipo'], 1)
        self.assertEqual(equipo['nombre'], 'Equipo 1')
        self.assertEqual(equipo['username'], 'Paco')
        self.assertEqual(equipo['pokemons'], [])

        print(f"############### Caso 1.2: Ver los equipos del usuario cuando tiene 1 equipo con 1 Pokémon ############## \n")

        # Simular algunos Pokémons
        mock_pokemons.return_value = [{'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu'}]

        mock_especie.return_value = {'nombreEspecie':'Pikachu', 'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1, 'foto':'foto.png', 'esLegendario':False, 'shiny':False}

        #Ejecutar el método que devuelve los equipos para mostrarlos
        resultados = GestorEquipo.get_user_equipos("Paco")
        
        print(resultados,f"\n \n")

        #Comprobar un equipo
        self.assertEqual(len(resultados), 1)
        #Comprobar info correcta
        equipo = resultados[0]
        self.assertEqual(equipo['idEquipo'], 1)
        self.assertEqual(equipo['nombre'], 'Equipo 1')
        self.assertEqual(equipo['username'], 'Paco')
        self.assertEqual(equipo['pokemons'], [{'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu', 'foto':'foto.png'}])

        print(f"############### Caso 1.3: Ver los equipos del usuario cuando tiene 1 equipo con 2 o más Pokémon ############## \n")

        # Simular algunos Pokémons
        mock_pokemons.return_value = [
            {'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu'},
            {'idPokemon':2, 'nombre':'tomas', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard'},
            {'idPokemon':3, 'nombre':'pepe', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax'},
            {'idPokemon':4, 'nombre':'gabriela', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey'},
            {'idPokemon':5, 'nombre':'sofia', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados'}
            ]

        mock_especie.side_effect = [

            {'nombreEspecie':'Pikachu', 'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1, 'foto':'foto.png', 'esLegendario':False, 'shiny':False},
            {'nombreEspecie':'Charizard', 'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1, 'foto':'foto2.png', 'esLegendario':False, 'shiny':False},
            {'nombreEspecie':'Snorlax', 'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1, 'foto':'foto3.png', 'esLegendario':False, 'shiny':False},
            {'nombreEspecie':'Pidgey', 'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1, 'foto':'foto4.png', 'esLegendario':False, 'shiny':False},
            {'nombreEspecie':'Gyarados', 'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1, 'foto':'foto5.png', 'esLegendario':False, 'shiny':False}
        ]

        #Ejecutar el método que devuelve los equipos para mostrarlos
        resultados = GestorEquipo.get_user_equipos("Paco")
        
        print(resultados,f"\n \n")

        #Comprobar un equipo
        self.assertEqual(len(resultados), 1)
        #Comprobar info correcta
        equipo = resultados[0]
        self.assertEqual(equipo['idEquipo'], 1)
        self.assertEqual(equipo['nombre'], 'Equipo 1')
        self.assertEqual(equipo['username'], 'Paco')
        self.assertEqual(equipo['pokemons'], [
            {'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu', 'foto':'foto.png'},
            {'idPokemon':2, 'nombre':'tomas', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard', 'foto':'foto2.png'},
            {'idPokemon':3, 'nombre':'pepe', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax', 'foto':'foto3.png'},
            {'idPokemon':4, 'nombre':'gabriela', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey', 'foto':'foto4.png'},
            {'idPokemon':5, 'nombre':'sofia', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados', 'foto':'foto5.png'}
            ])
        
        print(f"############### Caso 1.4: Ver los equipos del usuario cuando tiene 2 o más equipos con 2 o más Pokémon ############## \n")

        # Simular que el usuario tiene un equipo en la BD
        mock_cursor.fetchall.return_value = [
            {'idEquipo': 1, 'nombre': 'Equipo 1', 'fechaCreacion':'16/1/2026','username': 'Paco'},
            {'idEquipo': 2, 'nombre': 'Equipo 2', 'fechaCreacion':'16/1/2026','username': 'Paco'},
            {'idEquipo': 3, 'nombre': 'Equipo 3', 'fechaCreacion':'16/1/2026','username': 'Paco'},
            {'idEquipo': 4, 'nombre': 'Equipo 4', 'fechaCreacion':'16/1/2026','username': 'Paco'}
        ]
        # Simular algunos Pokémons
        mock_pokemons.side_effect = [

            [
            {'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu'},
            {'idPokemon':2, 'nombre':'tomas', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard'},
            {'idPokemon':3, 'nombre':'pepe', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax'},
            {'idPokemon':4, 'nombre':'gabriela', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey'},
            {'idPokemon':5, 'nombre':'sofia', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados'}
            ],
            [
            {'idPokemon':6, 'nombre':'daniel', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu'},
            {'idPokemon':7, 'nombre':'iker', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard'},
            {'idPokemon':8, 'nombre':'samuel', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax'},
            {'idPokemon':9, 'nombre':'maria', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey'},
            {'idPokemon':10, 'nombre':'berta', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados'}
            ],
            [
            {'idPokemon':11, 'nombre':'mutumbu', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu'},
            {'idPokemon':12, 'nombre':'linda', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard'},
            {'idPokemon':13, 'nombre':'franchesco', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax'},
            {'idPokemon':14, 'nombre':'franchesca', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey'},
            {'idPokemon':15, 'nombre':'daniela', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados'}
            ],
            [
            {'idPokemon':16, 'nombre':'Purificación', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu'},
            {'idPokemon':17, 'nombre':'Inocencio', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard'},
            {'idPokemon':18, 'nombre':'MaríaIsabel', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax'},
            {'idPokemon':19, 'nombre':'Ferdinando', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey'},
            {'idPokemon':20, 'nombre':'Morat', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados'}
            ]
            ]

        def especie_mock(nombreEspecie):
            especies = {
            'Pikachu': {'nombreEspecie':'Pikachu','foto':'foto.png'},
            'Charizard': {'nombreEspecie':'Charizard','foto':'foto2.png'},
            'Snorlax': {'nombreEspecie':'Snorlax','foto':'foto3.png'},
            'Pidgey': {'nombreEspecie':'Pidgey','foto':'foto4.png'},
            'Gyarados': {'nombreEspecie':'Gyarados','foto':'foto5.png'}
            }
            return especies[nombreEspecie]

        mock_especie.side_effect = especie_mock


        #Ejecutar el método que devuelve los equipos para mostrarlos
        resultados = GestorEquipo.get_user_equipos("Paco")
        
        print(resultados,f"\n \n")

        #Comprobar un equipo
        self.assertEqual(len(resultados), 4)
        #Comprobar info correcta

        equipo = resultados[0]
        self.assertEqual(equipo['idEquipo'], 1)
        self.assertEqual(equipo['nombre'], 'Equipo 1')
        self.assertEqual(equipo['username'], 'Paco')
        self.assertEqual(equipo['pokemons'], [
            {'idPokemon':1, 'nombre':'xavi', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu', 'foto':'foto.png'},
            {'idPokemon':2, 'nombre':'tomas', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard', 'foto':'foto2.png'},
            {'idPokemon':3, 'nombre':'pepe', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax', 'foto':'foto3.png'},
            {'idPokemon':4, 'nombre':'gabriela', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey', 'foto':'foto4.png'},
            {'idPokemon':5, 'nombre':'sofia', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados', 'foto':'foto5.png'}
            ])
        
        equipo = resultados[1]
        self.assertEqual(equipo['idEquipo'], 2)
        self.assertEqual(equipo['nombre'], 'Equipo 2')
        self.assertEqual(equipo['username'], 'Paco')
        self.assertEqual(equipo['pokemons'], [
            {'idPokemon':6, 'nombre':'daniel', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu', 'foto':'foto.png'},
            {'idPokemon':7, 'nombre':'iker', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard', 'foto':'foto2.png'},
            {'idPokemon':8, 'nombre':'samuel', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax', 'foto':'foto3.png'},
            {'idPokemon':9, 'nombre':'maria', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey', 'foto':'foto4.png'},
            {'idPokemon':10, 'nombre':'berta', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados', 'foto':'foto5.png'}
            ])
        
        equipo = resultados[2]
        self.assertEqual(equipo['idEquipo'], 3)
        self.assertEqual(equipo['nombre'], 'Equipo 3')
        self.assertEqual(equipo['username'], 'Paco')
        self.assertEqual(equipo['pokemons'], [
            {'idPokemon':11, 'nombre':'mutumbu', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu','foto':'foto.png'},
            {'idPokemon':12, 'nombre':'linda', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard','foto':'foto2.png'},
            {'idPokemon':13, 'nombre':'franchesco', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax','foto':'foto3.png'},
            {'idPokemon':14, 'nombre':'franchesca', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey','foto':'foto4.png'},
            {'idPokemon':15, 'nombre':'daniela', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados','foto':'foto5.png'}
            ])
        
        equipo = resultados[3]
        self.assertEqual(equipo['idEquipo'], 4)
        self.assertEqual(equipo['nombre'], 'Equipo 4')
        self.assertEqual(equipo['username'], 'Paco')
        self.assertEqual(equipo['pokemons'], [
            {'idPokemon':16, 'nombre':'Purificación', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pikachu','foto':'foto.png'},
            {'idPokemon':17, 'nombre':'Inocencio', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Charizard','foto':'foto2.png'},
            {'idPokemon':18, 'nombre':'MaríaIsabel', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Snorlax','foto':'foto3.png'},
            {'idPokemon':19, 'nombre':'Ferdinando', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Pidgey','foto':'foto4.png'},
            {'idPokemon':20, 'nombre':'Morat', 'ataque':1,'ataqueEsp':1,'def':1,'defEsp':1,'vel':1,'vida':1,'nombreEspecie':'Gyarados','foto':'foto5.png'}
            ])
        
    #Caso 2: Acceder a la opción ver equipos desde el menú principal, sin tener ningún equipo: En web
    #Caso 3: Crear nuevo equipo cuando el usuario tiene menos de 10 equipos

    @patch("app.repositories.GestorEquipo.GestorUsuario")  # Mock de la notificación
    @patch("app.repositories.GestorEquipo.get_db_context")  # Mock de la base de datos
    def test_crear_equipo_exitoso(self, mock_db, mock_notif):
        """Caso: Crear un equipo correctamente para un usuario con menos de 10 equipos"""

        # Configurar mocks de conexión y cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular que el cursor asigna el ID 42 al nuevo equipo
        mock_cursor.lastrowid = 42

        # Ejecutar el método
        resultado = GestorEquipo.crear_equipo("Paco", "EquipoTest")

        #  Comprobaciones
        self.assertEqual(resultado, (True, "Equipo creado", 42))

        # Verificar que se hizo un INSERT en la tabla equipo
        args_sql = mock_cursor.execute.call_args_list[0][0][0]  # La query
        self.assertIn("INSERT INTO equipo", args_sql)

        # Verificar que se pasó el usuario y nombre correctos
        args_params = mock_cursor.execute.call_args_list[0][0][1]
        self.assertEqual(args_params[0], "Paco")
        self.assertEqual(args_params[1], "EquipoTest")

        #  Verificar que se llamó a generarEvento
        mock_notif.generarEvento.assert_called_once_with(
            "Paco",
            "equipo",
            "Paco ha creado el equipo EquipoTest"
        )

    #Caso 4: Crear nuevo equipo cuando el usuario tiene ya 10: En web
    #Caso 5: Añadir un Pokémon al equipo

    @patch("app.repositories.GestorEquipo.get_db_context")
    @patch("app.repositories.GestorEquipo.GestorUsuario.generarEvento")
    @patch("app.repositories.GestorEquipo.GestorEquipo.get_especie_details")
    def test_crear_y_agregar_pokemon_exitoso(self, mock_especie, mock_generarEvento, mock_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_especie.return_value = {
            'nombreEspecie': 'Pikachu',
            'ataque': 10,
            'ataqueEsp': 5,
            'def': 3,
            'defEsp': 2,
            'velocidad': 20,
            'vida': 15
        }

        mock_cursor.lastrowid = 42
        # Aquí ponemos side_effect en orden de llamadas a fetchone()
        mock_cursor.fetchone.side_effect = [
            (0,),  # COUNT(*)
            None,  # slot libre
            {'username': 'Paco', 'nombreEspecie': 'Pikachu'}  # para generarEvento
        ]

        # Crear Pokémon
        pokemon_id = GestorEquipo.crear_pokemon("PikaBaby", "Pikachu")
        self.assertEqual(pokemon_id, 42)

        # Agregar Pokémon al equipo
        success, message = GestorEquipo.agregar_pokemon_equipo(1, 2, pokemon_id)
        self.assertTrue(success)
        self.assertEqual(message, "Pokémon agregado al equipo")

        #  Generar evento
        mock_generarEvento.assert_called_with('Paco', "captura", "Paco ha capturado un Pikachu")


    #Caso 6: Eliminar un Pokémon del equipo

    @patch("app.repositories.GestorEquipo.get_db_context")
    def test_delete_pokemon_exitoso(self, mock_db):
        """
        Test de delete_pokemon: se eliminan las filas de pokemon_ataque, equipo_pokemon y pokemon correctamente.
        """

        # Mock de conexión y cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # ID de prueba
        pokemon_id = 42

        # Llamada al método
        success, message = GestorEquipo.delete_pokemon(pokemon_id)

        # Comprobaciones de retorno
        self.assertTrue(success)
        self.assertEqual(message, "Pokemon expulsado correctamente")

        # Comprobaciones de llamadas a execute
        # Usamos assert_any_call para ignorar espacios/saltos de línea
        mock_cursor.execute.assert_any_call(ANY, (pokemon_id,))
        mock_cursor.execute.assert_any_call(ANY, (pokemon_id,))
        mock_cursor.execute.assert_any_call(ANY, (pokemon_id,))

        # También podemos comprobar que se llamaron 3 veces exactamente
        self.assertEqual(mock_cursor.execute.call_count, 3)

        # Opcional: verificar que los SQL contienen las tablas correctas
        sql_calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
        self.assertTrue(any("pokemon_ataque" in sql for sql in sql_calls))
        self.assertTrue(any("equipo_pokemon" in sql for sql in sql_calls))
        self.assertTrue(any("pokemon AS p" in sql for sql in sql_calls))
    

    @patch("app.repositories.GestorEquipo.get_db_context")
    def test_delete_pokemon_error(self, mock_db):
        """
        Test cuando ocurre un error al eliminar el Pokémon (simulamos una excepción).
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular que execute lanza una excepción
        mock_cursor.execute.side_effect = Exception("DB error")

        pokemon_id = 42
        success, message = GestorEquipo.delete_pokemon(pokemon_id)

        self.assertFalse(success)
        self.assertEqual(message, "Error expulsando al Pokémon del equipo")

    #Caso 7: Añadir un Pokémon de una especie X a un equipo cuando ya hay un Pokémon de la especie X en el equipo

    @patch("app.repositories.GestorEquipo.get_db_context")
    @patch("app.repositories.GestorEquipo.GestorUsuario.generarEvento")
    @patch("app.repositories.GestorEquipo.GestorEquipo.get_especie_details")
    def test_agregar_pokemon_misma_especie(self, mock_get_especie, mock_generar_evento, mock_db):
        """
        Test: añadir un Pokémon de una especie que ya existe en el equipo.
        """
        # Configurar mocks de DB
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simular que el equipo tiene menos de 6 Pokémon y el slot libre
        mock_cursor.fetchone.side_effect = [ (1,),  # count de Pokémon: 1
                                             None, # slot libre
                                             {'username': 'Paco', 'nombreEspecie': 'Pikachu'}]  # datos para notificación
        # Simular ID generado al crear el Pokémon
        mock_cursor.lastrowid = 99

        # Simular especie
        mock_get_especie.return_value = {
            'ataque': 10, 'ataqueEsp': 5, 'def': 8, 'defEsp': 4,
            'velocidad': 7, 'vida': 20
        }

        # Crear Pokémon
        pokemon_id = GestorEquipo.crear_pokemon("PikachuClone", "Pikachu")
        self.assertEqual(pokemon_id, 99)

        # Agregar Pokémon al equipo
        success, message = GestorEquipo.agregar_pokemon_equipo(equipo_id=1, slot=2, pokemon_id=pokemon_id)

        # Comprobaciones
        self.assertTrue(success)
        self.assertEqual(message, "Pokémon agregado al equipo")

        # Verificar inserciones en la BD
        mock_cursor.execute.assert_any_call(
            """
                        INSERT INTO equipo_pokemon (idEquipo, slot, idPokemon)
                        VALUES (?, ?, ?)
                    """, (1, 2, 99)
        )

        # Verificar que se generó notificación
        mock_generar_evento.assert_called_once_with('Paco', 'captura', 'Paco ha capturado un Pikachu')

    #Caso 8: Eliminar un equipo
    #Caso 9: Eliminar un equipo, seleccionando “Cancelar” en el cuadro de texto: En web
    #Caso 9: Pulsar la flecha de la esquina superior derecha, estando en la lista de equipos: En web
    #Caso 10: Pulsar la flecha de la esquina superior izquierda, estando en pantalla de captura de Pokémons (ilustración 16): En web


