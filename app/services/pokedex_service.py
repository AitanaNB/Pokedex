# -*- coding: utf-8 -*-
"""
Servicio de Pokédex que maneja la lógica de negocio relacionada con Pokémon.
"""
from typing import List, Optional, Dict, Tuple
from app.repositories.pokemon_repository import EspecieRepository, TipoRepository
from config.database import get_db_context
from datetime import datetime


class PokedexService:
    """Servicio para operaciones relacionadas con la Pokédex."""
    
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
            return PokedexService.get_all_especies()
        
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
            return PokedexService.get_all_especies()
        
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


class EquipoService:
    """Servicio para operaciones relacionadas con equipos."""
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
                    EquipoService.eliminar_pokemon(pokemon_id)
                    return False, "Máximo 6 Pokémon por equipo"
                
                # Verificar que no esté el slot del equipo ocupado ya
                cursor.execute("SELECT 1 FROM equipo_pokemon WHERE idEquipo = ? AND slot = ?", (equipo_id, slot))
                if cursor.fetchone():
                    EquipoService.eliminar_pokemon(pokemon_id)
                    return False, f"Slot {slot} ya está ocupado"
                
                cursor.execute("""
                    INSERT INTO equipo_pokemon (idEquipo, slot, idPokemon)
                    VALUES (?, ?, ?)
                """, (equipo_id, slot, pokemon_id))
                
                return True, "Pokémon agregado al equipo"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
        
    @staticmethod
    def eliminar_pokemon(pokemon_id = int) -> Optional[bool]:
        try:
            with get_db_context as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM pokemon WHERE idPokemon = ?
                """, (pokemon_id,))
        except Exception as e:
            return False, f"Error: {str(e)}"

        return True
    
    @staticmethod
    def get_user_equipos(usuario: str) -> List[Dict]:
        """Obtiene los equipos de un usuario."""
        try:
            with get_db_context() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM equipo WHERE username = ?
                """, (usuario,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo equipos: {e}")
            return []
    
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
                    SELECT p.* FROM pokemon p
                    JOIN equipo_pokemon ep ON p.idPokemon = ep.idPokemon
                    WHERE ep.idEquipo = ?
                """, (equipo_id,))
                return cursor.fetchall()
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
        especie = PokedexService.get_especie_details(nomEspecie)
        print(dict(especie))
        if especie:
            #TODO: RANDOMIZAR VALORES + AÑADIR ATAQUES
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
