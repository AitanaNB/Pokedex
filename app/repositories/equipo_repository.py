"""
Repositorio para gestionar operaciones de Equipos de Pokémon.
"""
from typing import Optional, List
from app.models import Equipo, Pokemon
from config.database import get_db_context
from app.repositories.pokemon_repository import PokemonRepository


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
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
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
                return True
        except Exception as e:
            print(f"Error al actualizar nombre del equipo: {e}")
            return False
