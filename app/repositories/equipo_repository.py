"""
Repositorio para gestionar operaciones de Equipos de Pokémon.
"""
from typing import Optional, List
from app.models import Equipo, Pokemon
from config.database import get_db_context
from app.repositories.pokemon_repository import PokemonRepository
from app.repositories.notificacion_repository import NotificacionRepository


class EquipoRepository:
    """Repositorio para operaciones CRUD de Equipos."""
    
    @staticmethod
    def create(equipo: Equipo) -> Optional[int]:
        """
        Crea un nuevo equipo.
        
        Args:
            equipo: Instancia de Equipo a crear
            
        Returns:
            int: ID del equipo creado, None si falla
        """
        #no permitir equipos sin nombre o sin Pokémon
        if not equipo.nombre or not equipo.nombre.strip():
            print("Error: Sin nombre")
            return None
        if not equipo.pokemons:
            print("Error: Sin pokemons")
            return None
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                #validar que hay menos de 10 equipos para añadir uno nuevo
                cursor.execute("SELECT COUNT(*) as total FROM equipo WHERE username = ?", equipo.username)
                rdo = cursor.fetchone()
                cantidad= rdo['total'] if rdo else 0

                if cantidad ==10:
                    print("Error: Ya hay 10 equipos")
                    return None

                cursor.execute("""
                    INSERT INTO equipo (nombre, fechaCreacion, username)
                    VALUES (?, ?, ?)
                """, (equipo.nombre, equipo.fechaCreacion, equipo.username))
                
                equipo_id = cursor.lastrowid
                
                # Agregar Pokémon al equipo si hay
                if equipo.pokemons:
                    for pokemon in equipo.pokemons:
                        if pokemon.idPokemon:
                            cursor.execute("""
                                INSERT INTO equipo_pokemon (idEquipo, idPokemon)
                                VALUES (?, ?)
                            """, (equipo_id, pokemon.idPokemon))
                conn.commit()
            #Generar evento en notificación
            NotificacionRepository.generarEvento(equipo.username,"equipo",f"{equipo.username} ha creado el equipo {equipo.nombre}.")
            return equipo_id
        except Exception as e:
            print(f"Error al crear equipo: {e}")
            return None
    
    @staticmethod
    def find_by_id(equipo_id: int) -> Optional[Equipo]:
        """Busca un equipo por su ID."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM equipo WHERE idEquipo = ?", (equipo_id,))
                row = cursor.fetchone()
                if row:
                    # Obtener Pokémon del equipo
                    cursor.execute("""
                        SELECT idPokemon FROM equipo_pokemon WHERE idEquipo = ?
                    """, (equipo_id,))
                    pokemon_ids = [p['idPokemon'] for p in cursor.fetchall()]
                    
                    pokemons = []
                    for pid in pokemon_ids:
                        pokemon = PokemonRepository.find_by_id(pid)
                        if pokemon:
                            pokemons.append(pokemon)
                    
                    return Equipo(
                        idEquipo=row['idEquipo'],
                        nombre=row['nombre'],
                        fechaCreacion=row['fechaCreacion'],
                        username=row['username'],
                        pokemons=pokemons
                    )
                return None
        except Exception as e:
            print(f"Error al buscar equipo: {e}")
            return None
    
    @staticmethod
    def get_by_user(username: str) -> List[Equipo]:
        """Obtiene todos los equipos de un usuario."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM equipo WHERE username = ?
                """, (username,))
                rows = cursor.fetchall()
                equipos = []
                for row in rows:
                    # Obtener Pokémon del equipo
                    cursor.execute("""
                        SELECT idPokemon FROM equipo_pokemon WHERE idEquipo = ?
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
                return equipos
        except Exception as e:
            print(f"Error al obtener equipos del usuario: {e}")
            return []
    
    @staticmethod
    def add_pokemon(equipo_id: int, pokemon_id: int) -> bool:
        """Agrega un Pokémon a un equipo."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                # Verificar que el equipo no tenga más de 6 Pokémon
                cursor.execute("""
                    SELECT COUNT(*) as count FROM equipo_pokemon WHERE idEquipo = ?
                """, (equipo_id,))
                count = cursor.fetchone()['count']
                
                if count >= 6:
                    print("El equipo ya tiene 6 Pokémon")
                    return False
                
                cursor.execute("""
                    INSERT INTO equipo_pokemon (idEquipo, idPokemon)
                    VALUES (?, ?)
                """, (equipo_id, pokemon_id))

                 #obtener nombre de usuario que crea el equipo, nombre del equipo y del pokemon para generar la notificación
                cursor.execute("""
                    SELECT e.username as usuario, e.nombre as equipo, p.nombre as pokemon
                    FROM equipo e 
                    INNER JOIN equipo_pokemon ep ON e.id = ep.idEquipo
                    INNER JOIN pokemon p ON ep.idPokemon = p.idPokemon
                    WHERE e.idEquipo = ? AND p.idPokemon = ?
                    """, (equipo_id,pokemon_id,))
                resultado= cursor.fetchone()
                conn.commit()
            if resultado:
                username=resultado['usuario']
                equipo=resultado['equipo']
                pokemon=resultado['pokemon']
                #generar notificación
                NotificacionRepository.generarEvento(username,"captura", f"{username} ha añadido un {pokemon} en el equipo {equipo}.")
            return True
        except Exception as e:
            print(f"Error al agregar Pokémon al equipo: {e}")
            return False
    
    @staticmethod
    def remove_pokemon(equipo_id: int, pokemon_id: int) -> bool:
        """Elimina un Pokémon de un equipo."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM equipo_pokemon WHERE idEquipo = ? AND idPokemon = ?
                """, (equipo_id, pokemon_id))
                conn.commit()
                return True

        except Exception as e:
            print(f"Error al eliminar Pokémon del equipo: {e}")
            return False
    
    @staticmethod
    def delete(equipo_id: int) -> bool:
        """Elimina un equipo."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM equipo WHERE idEquipo = ?", (equipo_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al eliminar equipo: {e}")
            return False
    
    @staticmethod
    def update_nombre(equipo_id: int, nuevo_nombre: str) -> bool:
        """Actualiza el nombre de un equipo."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE equipo SET nombre = ? WHERE idEquipo = ?
                """, (nuevo_nombre, equipo_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar nombre del equipo: {e}")
            return False
