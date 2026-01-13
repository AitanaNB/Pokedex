from config.database import get_db_context
from typing import List
from app.models import Equipo
from app.repositories.pokemon_repository import PokemonRepository

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
            print("Se han encontrado los sguientes")
            return equipos
    except Exception as e:
        print(f"Error al obtener equipos del usuario: {e}")
        return []