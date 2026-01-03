"""
Repositorio para gestionar operaciones de Pokémon y Especies.
"""
from typing import Optional, List
from app.models import Pokemon, Especie, Tipo, Ataque
from config.database import get_db_context


class PokemonRepository:
    """Repositorio para operaciones CRUD de Pokémon."""
    
    @staticmethod
    def create(pokemon: Pokemon) -> Optional[int]:
        """
        Crea un nuevo Pokémon en la base de datos.
        
        Args:
            pokemon: Instancia de Pokemon a crear
            
        Returns:
            int: ID del Pokémon creado, None si falla
        """
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pokemon (nombre, ataque, ataqueEsp, def, defEsp, vel, vida, nombreEspecie)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (pokemon.nombre, pokemon.ataque, pokemon.ataqueEsp, pokemon.def_, 
                      pokemon.defEsp, pokemon.vel, pokemon.vida, pokemon.nombreEspecie))
                
                pokemon_id = cursor.lastrowid
                
                # Asignar ataques al Pokémon
                if pokemon.ataques:
                    for ataque in pokemon.ataques:
                        cursor.execute("""
                            INSERT INTO pokemon_ataque (idPokemon, nombreAtaque)
                            VALUES (?, ?)
                        """, (pokemon_id, ataque))
                
                return pokemon_id
        except Exception as e:
            print(f"Error al crear Pokémon: {e}")
            return None
    
    @staticmethod
    def find_by_id(pokemon_id: int) -> Optional[Pokemon]:
        """Busca un Pokémon por su ID."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pokemon WHERE idPokemon = ?", (pokemon_id,))
                row = cursor.fetchone()
                if row:
                    # Obtener ataques del Pokémon
                    cursor.execute("""
                        SELECT nombreAtaque FROM pokemon_ataque WHERE idPokemon = ?
                    """, (pokemon_id,))
                    ataques = [a['nombreAtaque'] for a in cursor.fetchall()]
                    
                    return Pokemon(
                        idPokemon=row['idPokemon'],
                        nombre=row['nombre'],
                        ataque=row['ataque'],
                        ataqueEsp=row['ataqueEsp'],
                        def_=row['def'],
                        defEsp=row['defEsp'],
                        vel=row['vel'],
                        vida=row['vida'],
                        nombreEspecie=row['nombreEspecie'],
                        ataques=ataques
                    )
                return None
        except Exception as e:
            print(f"Error al buscar Pokémon: {e}")
            return None
    
    @staticmethod
    def get_all() -> List[Pokemon]:
        """Obtiene todos los Pokémon."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pokemon")
                rows = cursor.fetchall()
                pokemons = []
                for row in rows:
                    # Obtener ataques
                    cursor.execute("""
                        SELECT nombreAtaque FROM pokemon_ataque WHERE idPokemon = ?
                    """, (row['idPokemon'],))
                    ataques = [a['nombreAtaque'] for a in cursor.fetchall()]
                    
                    pokemons.append(Pokemon(
                        idPokemon=row['idPokemon'],
                        nombre=row['nombre'],
                        ataque=row['ataque'],
                        ataqueEsp=row['ataqueEsp'],
                        def_=row['def'],
                        defEsp=row['defEsp'],
                        vel=row['vel'],
                        vida=row['vida'],
                        nombreEspecie=row['nombreEspecie'],
                        ataques=ataques
                    ))
                return pokemons
        except Exception as e:
            print(f"Error al obtener Pokémon: {e}")
            return []
    
    @staticmethod
    def delete(pokemon_id: int) -> bool:
        """Elimina un Pokémon."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pokemon WHERE idPokemon = ?", (pokemon_id,))
                return True
        except Exception as e:
            print(f"Error al eliminar Pokémon: {e}")
            return False


class EspecieRepository:
    """Repositorio para operaciones CRUD de Especies."""
    
    @staticmethod
    def create(conn, especie_dict: dict) -> Optional[str]:
        """
        Crea una nueva especie desde un diccionario.
        
        Args:
            conn: Conexión a BD
            especie_dict: Dict con campos de especie
            
        Returns:
            Nombre de la especie creada o None
        """
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO especie (nombreEspecie, ataque, ataqueEsp, def, defEsp, vida, velocidad, foto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                especie_dict.get('nombre', ''),
                especie_dict.get('ataque', 0),
                especie_dict.get('ataqueEsp', 0),
                especie_dict.get('def', 0),
                especie_dict.get('defEsp', 0),
                especie_dict.get('vida', 0),
                especie_dict.get('velocidad', 0),
                especie_dict.get('imagen_url', '')
            ))
            return especie_dict.get('nombre', '')
        except Exception as e:
            print(f"Error al crear especie: {e}")
            return None
    
    @staticmethod
    def add_tipo(conn, nombre_especie: str, nombre_tipo: str) -> bool:
        """Asocia un tipo a una especie usando nombres."""
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO especie_tipo (nombreEspecie, nombreTipo)
                VALUES (?, ?)
            """, (nombre_especie, nombre_tipo))
            return True
        except Exception as e:
            print(f"Error al agregar tipo: {e}")
            return False
    
    @staticmethod
    def find_by_name(conn, nombre: str) -> Optional[dict]:
        """Busca una especie por su nombre. Retorna dict con datos."""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM especie WHERE nombreEspecie = ?", (nombre,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al buscar especie: {e}")
            return None
    
    @staticmethod
    def get_all(conn=None) -> List[Especie]:
        """Obtiene todas las especies."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM especie")
                rows = cursor.fetchall()
                especies = []
                for row in rows:
                    # Obtener tipos
                    cursor.execute("""
                        SELECT nombreTipo FROM especie_tipo WHERE nombreEspecie = ?
                    """, (row['nombreEspecie'],))
                    tipos = [t['nombreTipo'] for t in cursor.fetchall()]
                    
                    especies.append(Especie(
                        nombreEspecie=row['nombreEspecie'],
                        ataque=row['ataque'],
                        ataqueEsp=row['ataqueEsp'],
                        def_=row['def'],
                        defEsp=row['defEsp'],
                        vida=row['vida'],
                        velocidad=row['velocidad'],
                        foto=row['foto'],
                        esLegendario=bool(row['esLegendario']),
                        shiny=bool(row['shiny']),
                        tipos=tipos
                    ))
                return especies
        except Exception as e:
            print(f"Error al obtener especies: {e}")
            return []
    
    @staticmethod
    def search_by_name(query: str) -> List[Especie]:
        """Busca especies por nombre (búsqueda parcial)."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM especie WHERE nombreEspecie LIKE ?
                """, (f"%{query}%",))
                rows = cursor.fetchall()
                especies = []
                for row in rows:
                    cursor.execute("""
                        SELECT nombreTipo FROM especie_tipo WHERE nombreEspecie = ?
                    """, (row['nombreEspecie'],))
                    tipos = [t['nombreTipo'] for t in cursor.fetchall()]
                    
                    especies.append(Especie(
                        nombreEspecie=row['nombreEspecie'],
                        ataque=row['ataque'],
                        ataqueEsp=row['ataqueEsp'],
                        def_=row['def'],
                        defEsp=row['defEsp'],
                        vida=row['vida'],
                        velocidad=row['velocidad'],
                        foto=row['foto'],
                        esLegendario=bool(row['esLegendario']),
                        shiny=bool(row['shiny']),
                        tipos=tipos
                    ))
                return especies
        except Exception as e:
            print(f"Error al buscar especies: {e}")
            return []
    
    @staticmethod
    def get_by_tipo(tipo: str) -> List[Especie]:
        """Obtiene especies filtradas por tipo."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.* FROM especie e
                    INNER JOIN especie_tipo et ON e.nombreEspecie = et.nombreEspecie
                    WHERE et.nombreTipo = ?
                """, (tipo,))
                rows = cursor.fetchall()
                especies = []
                for row in rows:
                    cursor.execute("""
                        SELECT nombreTipo FROM especie_tipo WHERE nombreEspecie = ?
                    """, (row['nombreEspecie'],))
                    tipos = [t['nombreTipo'] for t in cursor.fetchall()]
                    
                    especies.append(Especie(
                        nombreEspecie=row['nombreEspecie'],
                        ataque=row['ataque'],
                        ataqueEsp=row['ataqueEsp'],
                        def_=row['def'],
                        defEsp=row['defEsp'],
                        vida=row['vida'],
                        velocidad=row['velocidad'],
                        foto=row['foto'],
                        esLegendario=bool(row['esLegendario']),
                        shiny=bool(row['shiny']),
                        tipos=tipos
                    ))
                return especies
        except Exception as e:
            print(f"Error al filtrar por tipo: {e}")
            return []


class TipoRepository:
    """Repositorio para operaciones de Tipos."""
    
    @staticmethod
    def get_all(conn=None) -> List[Tipo]:
        """Obtiene todos los tipos."""
        try:
            if conn is None:
                with get_db_context() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM tipo")
                    rows = cursor.fetchall()
                    return [Tipo(nombreTipo=row['nombreTipo']) for row in rows]
            else:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tipo")
                rows = cursor.fetchall()
                return [Tipo(nombreTipo=row['nombreTipo']) for row in rows]
        except Exception as e:
            print(f"Error al obtener tipos: {e}")
            return []
    
    @staticmethod
    def get_by_name(conn, nombre: str) -> Optional[dict]:
        """Obtiene un tipo por su nombre."""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipo WHERE nombreTipo = ?", (nombre,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener tipo: {e}")
            return None
    
    @staticmethod
    def create(conn, tipo: Tipo) -> bool:
        """Crea un nuevo tipo."""
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tipo (nombreTipo) VALUES (?)", (tipo.nombreTipo,))
            return True
        except Exception as e:
            print(f"Error al crear tipo: {e}")
            return False
    
    @staticmethod
    def create_if_not_exists(conn, nombre: str) -> bool:
        """Crea un tipo si no existe."""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipo WHERE nombreTipo = ?", (nombre,))
            if cursor.fetchone():
                return True
            cursor.execute("INSERT INTO tipo (nombreTipo) VALUES (?)", (nombre,))
            return True
        except Exception as e:
            print(f"Error al crear tipo: {e}")
            return False
