
"""
Servicio de Pokédex que maneja la lógica de negocio relacionada con Pokémon.
"""
from config.database import get_db_context
from app.models import Equipo
from app.repositories.pokemon_repository import PokemonRepository
from typing import List, Optional, Dict, Tuple
from app.repositories.pokemon_repository import EspecieRepository, TipoRepository
from datetime import datetime
import app.repositories.GestorUsuario as GestorUsuario

class GestorEquipo:
    """Clase para operaciones relacionadas con equipos."""

    def get_by_user(username: str) -> List[Equipo]:
        """Obtiene todos los equipos de un usuario."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                            SELECT *
                            FROM equipo
                            WHERE username = ?
                            """, (username,))
                rows = cursor.fetchall()
                equipos = []
                for row in rows:
                    # Obtener Pokémon del equipo
                    cursor.execute("""
                                SELECT idPokemon
                                FROM equipo_pokemon
                                WHERE idEquipo = ?
                                """, (row['idEquipo'],))
                    pokemon_ids = [p['idPokemon'] for p in cursor.fetchall()]

                    pokemons = []
                    for pid in pokemon_ids:
                        pokemon = PokemonRepository.find_by_id(pid)
                        
                        if pokemon:
                            
                            pokemons.append(pokemon)

                    equipos.append(Equipo(
                        idEquipo=row['idEquipo'],
                        nombre=row['nombre'],
                        fechaCreacion=row['fechaCreacion'],
                        username=row['username'],
                        pokemons=pokemons
                    ))
                print("Se han encontrado los siguientes")
                return equipos
        except Exception as e:
            print(f"Error al obtener equipos del usuario: {e}")
            return []
        
    @staticmethod
    def get_user_equipos(usuario: str) -> List[Dict]:
            """Obtiene los equipos de un usuario, con sus Pokemons, sus fotos y los slots a los que pertenecen."""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT * FROM equipo WHERE username = ?
                    """, (usuario,))
                    equipos_db = cursor.fetchall()

                equipos = []

                #Queremos que los equipos contengan su lista de pokemons para mostrarlos.
                #cursor.fetchall nos da un formato no modificable, creamos nuestro dict modificable: equipos[]

                for equipo_db in equipos_db:
                    equipo = dict(equipo_db)
                    pokemons_db = GestorEquipo.get_equipo_pokemon(equipo['idEquipo'])
                    pokemons = []

                    #Queremos que los pokemons tengan su foto para mostrarla, a si que hacemos dict modificable: pokemons[]

                    for pokemon_db in pokemons_db:
                        pokemon = dict(pokemon_db)
                        detalles = GestorEquipo.get_especie_details(pokemon['nombreEspecie'])
                        pokemon['foto'] = detalles['foto']
                        pokemons.append(pokemon)

                    equipo['pokemons'] = pokemons
                    equipos.append(equipo)
                return equipos
            except Exception as e:
                print(f"Error obteniendo equipos: {e}")
                return []
        
        
    @staticmethod
    def get_all_especies() -> List[Dict]:
            """Obtiene todas las especies disponibles."""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT * FROM especie ORDER BY nombreEspecie
                    """)
                    return cursor.fetchall()
            except Exception as e:
                print(f"Error obteniendo especies: {e}")
                return []
        
    @staticmethod
    def search_especies(query: str) -> List[Dict]:
            """
            Busca especies por nombre.
            
            Args:
                query: Término de búsqueda
                
            Returns:
                List[Dict]: Especies que coinciden
            """
            if not query:
                return GestorEquipo.get_all_especies()
            
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT * FROM especie 
                        WHERE LOWER(nombreEspecie) LIKE LOWER(?)
                    """, (f"%{query}%",))
                    return cursor.fetchall()
            except Exception as e:
                print(f"Error buscando especies: {e}")
                return []
        
    @staticmethod
    def filter_by_tipo(tipo: str) -> List[Dict]:
            """
            Filtra especies por tipo.
            
            Args:
                tipo: Nombre del tipo
                
            Returns:
                List[Dict]: Especies del tipo especificado
            """
            if not tipo or tipo == "todos":
                return GestorEquipo.get_all_especies()
            
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT DISTINCT e.* FROM especie e
                        INNER JOIN especie_tipo et ON e.nombreEspecie = et.nombreEspecie
                        INNER JOIN tipo t ON et.nombreTipo = t.nombreTipo
                        WHERE LOWER(t.nombreTipo) = LOWER(?)
                    """, (tipo,))
                    return cursor.fetchall()
            except Exception as e:
                print(f"Error filtrando por tipo: {e}")
                return []
        
    @staticmethod
    def get_especie_details(nombre: str) -> Optional[Dict]:
            """
            Obtiene los detalles completos de una especie.
            
            Args:
                nombre: Nombre de la especie
                
            Returns:
                Dict con datos de la especie
            """
            try:
                with get_db_context() as conn:
                    return EspecieRepository.find_by_name(conn, nombre)
            except Exception as e:
                print(f"Error obteniendo detalles: {e}")
                return None
        
    @staticmethod
    def get_tipos() -> List[Dict]:
            """Obtiene todos los tipos."""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM tipo ORDER BY nombreTipo")
                    return cursor.fetchall()
            except Exception as e:
                print(f"Error obteniendo tipos: {e}")
                return []
        
    @staticmethod
    def get_especie_tipos(nombreEspecie: int) -> List[str]:
            """Obtiene los tipos de una especie."""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT t.nombreTipo FROM especie_tipo et
                        JOIN tipo t ON et.nombreTipo = t.nombreTipo
                        WHERE et.nombreEspecie = ?
                    """, (nombreEspecie,))
                    return [row[0] for row in cursor.fetchall()]
            except Exception as e:
                print(f"Error obteniendo tipos: {e}")
                return []
        
    @staticmethod
    def get_all_pokemon() -> List[Dict]:
            """Obtiene todos los Pokémon de la base de datos."""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT nombreEspecie, foto FROM especie ORDER BY nombreEspecie ASC
                    """)
                    results = cursor.fetchall()
                    
                    # Convertir sqlite3.Row a diccionarios
                    pokemons = []
                    for row in results:
                        pokemons.append({
                            'nombre': row['nombreEspecie'],
                            'imagen': row['foto']
                        })
                    return pokemons
            except Exception as e:
                print(f"Error obteniendo Pokémon: {e}")
                import traceback
                traceback.print_exc()
                return []

    @staticmethod
    def crear_equipo(usuario: str, nombre: str) -> Tuple[bool, str, Optional[int]]:
            """
            Crea un nuevo equipo.
            
            Args:
                usuario: Nombre del usuario
                nombre: Nombre del equipo
                
            Returns:
                (éxito: bool, mensaje: str, equipo_id: int or None)
            """
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO equipo (username, nombre, fechaCreacion)
                        VALUES (?, ?, ?)
                    """, (usuario, nombre, datetime.now()))
                    equipo_id = cursor.lastrowid
                    #generar notificación
                GestorUsuario.generarEvento(usuario, "equipo", f"{usuario} ha creado el equipo {nombre}")
                return True, "Equipo creado", equipo_id
            except Exception as e:
                return False, f"Error: {str(e)}", None
        
    @staticmethod
    def agregar_pokemon_equipo(equipo_id: int, slot: int, pokemon_id: int) -> Tuple[bool, str]:
            """Agrega un Pokémon a un equipo."""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    # Verificar que no haya más de 6 Pokémon
                    cursor.execute("SELECT COUNT(*) FROM equipo_pokemon WHERE idEquipo = ?", (equipo_id,))
                    count = cursor.fetchone()[0]
                    if count >= 6:
                        GestorEquipo.eliminar_pokemon(pokemon_id, conn)
                        return False, "Máximo 6 Pokémon por equipo"
                    
                    # Verificar que no esté el slot del equipo ocupado ya
                    cursor.execute("SELECT 1 FROM equipo_pokemon WHERE idEquipo = ? AND slot = ?", (equipo_id, slot))
                    if cursor.fetchone():
                        GestorEquipo.eliminar_pokemon(pokemon_id, conn)
                        return False, f"Slot {slot} ya está ocupado"

                    cursor.execute("""
                        INSERT INTO equipo_pokemon (idEquipo, slot, idPokemon)
                        VALUES (?, ?, ?)
                    """, (equipo_id, slot, pokemon_id))

                    # Obtener datos para generar la notificación
                    cursor.execute("""
                                SELECT e.username, p.nombreEspecie
                                FROM equipo e,
                                        pokemon p
                                WHERE e.idEquipo = ?
                                    AND p.idPokemon = ?
                                """, (equipo_id, pokemon_id))
                    datos = cursor.fetchone()

                # generar notificación
                GestorUsuario.generarEvento(datos['username'], "captura", f"{datos['username']} ha capturado un {datos['nombreEspecie']}")
                return True, "Pokémon agregado al equipo"
                
            except Exception as e:
                return False, f"Error: {str(e)}"
            
    @staticmethod
    def eliminar_pokemon(pokemon_id: int, conn) -> bool:
            "Elimina un Pokémon de la base de datos"
            try:
                cursor = conn.cursor()
                cursor.execute(
                        "DELETE FROM pokemon WHERE idPokemon = ?",
                        (pokemon_id,)
                )
                return True
            except Exception as e:
                print(f"Error eliminando Pokémon: {e}")
                return False
        
    @staticmethod
    def delete_pokemon(pokemon_id: int) -> Tuple[bool,str]:
            "Elimina un Pokémon y lo expulsa del equipo"
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                            DELETE FROM pokemon_ataque AS pa
                            WHERE pa.idPokemon = ?
                            """,(pokemon_id,))

                    cursor.execute("""
                            DELETE FROM equipo_pokemon AS ep 
                            WHERE ep.idPokemon = ?
                        """,(pokemon_id,))

                    cursor.execute("""
                            DELETE FROM pokemon AS p 
                            WHERE p.idPokemon = ?
                        """,(pokemon_id,))
                return True, "Pokemon expulsado correctamente"
            except Exception as e:
                print(f"Error al eliminar Pokémon: ",e)
                return False, "Error expulsando al Pokémon del equipo"
        
    
    @staticmethod
    def get_equipo_details(equipo_id: int) -> Optional[Dict]:
            """Obtiene los detalles de un equipo."""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT e.*, COUNT(ep.idPokemon) as cantidad_pokemon
                        FROM equipo e
                        LEFT JOIN equipo_pokemon ep ON e.idEquipo = ep.idEquipo
                        WHERE e.idEquipo = ?
                    """, (equipo_id,))
                    return cursor.fetchone()
            except Exception as e:
                print(f"Error obteniendo equipo: {e}")
                return None
        
    @staticmethod
    def get_equipo_pokemon(equipo_id: int) -> List[Dict]:
            """Obtiene los Pokémon de un equipo."""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT p.*, ep.slot FROM pokemon p
                        JOIN equipo_pokemon ep ON p.idPokemon = ep.idPokemon
                        WHERE ep.idEquipo = ?
                        ORDER BY ep.slot
                    """, (equipo_id,))
                    data = cursor.fetchall()
                return data
            except Exception as e:
                print(f"Error obteniendo Pokémon del equipo: {e}")
                return []
            
    @staticmethod
    def delete_equipo(equipo_id: int) -> Tuple[bool, str]:
            """Dado el ID de un equipo, lo elimina a este, a todos sus pokémon, y su relación con los ataques"""
            try:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT p.idPokemon FROM pokemon p
                        JOIN equipo_pokemon ep ON p.idPokemon = ep.idPokemon
                        WHERE ep.idEquipo = ?
                    """, (equipo_id,))
                    pokemon_ids = cursor.fetchall()

                    for fila in pokemon_ids:
                        pokemon_id = fila['idPokemon']
                        cursor.execute("""
                            DELETE FROM pokemon_ataque AS pa
                            WHERE pa.idPokemon = ?
                            """,(pokemon_id,))

                        cursor.execute("""
                            DELETE FROM equipo_pokemon AS ep 
                            WHERE ep.idPokemon = ? AND ep.idEquipo = ?
                        """,(pokemon_id, equipo_id))

                        cursor.execute("""
                            DELETE FROM pokemon AS p 
                            WHERE p.idPokemon = ?
                        """,(pokemon_id,))

                    cursor.execute("""
                        DELETE FROM equipo AS e 
                        WHERE e.idEquipo = ?
                    """,(equipo_id,))
                return True, "equipo eliminado con éxito"
            except Exception as e:
                print(f"Error eliminando el equipo: {e}")
                return False, "ha habido un problema eliminando el equipo"

    @staticmethod
    def crear_pokemon(nickname: str, nomEspecie: str) -> Optional[int]:
            """"Dado un nickname y el nombre de una especie, genera un Pokémon nuevo.
                Returns:
                    id del Pokémon generado.
            """
            especie = GestorEquipo.get_especie_details(nomEspecie)
            if especie:

                ataque = especie['ataque']
                ataqueEsp = especie['ataqueEsp']
                defensa = especie['def']
                defEsp = especie['defEsp']
                vel = especie['velocidad']
                vida = especie['vida']

                try:
                    with get_db_context() as conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO pokemon(nombre, ataque, ataqueEsp, def, defEsp, vel, vida, nombreEspecie)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (nickname, ataque, ataqueEsp, defensa, defEsp, vel, vida, nomEspecie))
                        pokemon_id = cursor.lastrowid

                    return pokemon_id
                
                except Exception as e:
                    print(f"Error creando Pokémon: {e}")
                    return -1
            else:
                return -1
