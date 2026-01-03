# coding: utf-8
"""
Servicio para conectar con PokeAPI y obtener datos de Pokemon.
"""
import requests
import logging
import time

logger = logging.getLogger(__name__)


class PokeAPIService:
    """
    Servicio para obtener datos de Pokemon desde PokeAPI usando requests.
    """

    BASE_URL = "https://pokeapi.co/api/v2"
    GENERATION_1_END = 151

    @staticmethod
    def get_pokemon_by_id(pokemon_id):
        """
        Obtiene datos de un Pokemon por su ID desde PokeAPI.
        """
        try:
            response = requests.get(f"{PokeAPIService.BASE_URL}/pokemon/{pokemon_id}", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'id': data['id'],
                'name': data['name'].capitalize(),
                'height': data['height'],
                'weight': data['weight'],
                'base_experience': data.get('base_experience', 0),
                'types': [t['type']['name'] for t in data['types']],
                'abilities': [a['ability']['name'] for a in data['abilities']],
                'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
                'image_url': data['sprites']['front_default'],
                'image_url_back': data['sprites'].get('back_default', ''),
            }
        except Exception as e:
            logger.error("Error obteniendo Pokemon " + str(pokemon_id) + ": " + str(e))
            return None

    @staticmethod
    def get_pokemon_by_name(name):
        """
        Obtiene datos de un Pokemon por su nombre desde PokeAPI.
        """
        try:
            response = requests.get(f"{PokeAPIService.BASE_URL}/pokemon/{name.lower()}", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'id': data['id'],
                'name': data['name'].capitalize(),
                'height': data['height'],
                'weight': data['weight'],
                'base_experience': data.get('base_experience', 0),
                'types': [t['type']['name'] for t in data['types']],
                'abilities': [a['ability']['name'] for a in data['abilities']],
                'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
                'image_url': data['sprites']['front_default'],
                'image_url_back': data['sprites'].get('back_default', ''),
            }
        except Exception as e:
            logger.error("Error obteniendo Pokemon " + str(name) + ": " + str(e))
            return None

    @staticmethod
    def get_all_gen1_pokemon():
        """
        Obtiene todos los Pokemon de Generacion 1 (1-151).
        """
        pokemon_list = []
        for i in range(1, PokeAPIService.GENERATION_1_END + 1):
            pokemon_data = PokeAPIService.get_pokemon_by_id(i)
            if pokemon_data:
                pokemon_list.append(pokemon_data)
                logger.info("Pokemon " + str(i) + "/151 cargado: " + pokemon_data['name'])
            time.sleep(0.1)  # Rate limiting
        
        return pokemon_list


    @staticmethod
    def get_type_effectiveness():
        """Obtiene la efectividad de tipos."""
        try:
            effectiveness = {}
            for type_name in ['normal', 'fire', 'water', 'grass', 'electric', 'ice',
                             'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
                             'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']:
                try:
                    type_obj = pb.type_(type_name)
                    effectiveness[type_name] = {
                        'damages_to': [t.name for t in type_obj.damage_relations.damage_to],
                        'damaged_by': [t.name for t in type_obj.damage_relations.damage_from],
                    }
                except:
                    pass
            return effectiveness
        except Exception as e:
            logger.error("Error obteniendo efectividad de tipos: " + str(e))
            return {}

    @staticmethod
    @staticmethod
    def get_evolution_chain(pokemon_name):
        """Obtiene la cadena de evolucion de un Pokemon."""
        try:
            # Obtener el Pokémon
            response = requests.get(f"{PokeAPIService.BASE_URL}/pokemon/{pokemon_name.lower()}", timeout=10)
            response.raise_for_status()
            pokemon_data = response.json()
            pokemon_id = pokemon_data['id']
            
            # Obtener la especie
            species_response = requests.get(f"{PokeAPIService.BASE_URL}/pokemon-species/{pokemon_id}", timeout=10)
            species_response.raise_for_status()
            species_data = species_response.json()
            
            if not species_data.get('evolution_chain'):
                return [pokemon_name.capitalize()]
            
            # Obtener la cadena de evolución
            chain_url = species_data['evolution_chain']['url']
            chain_response = requests.get(chain_url, timeout=10)
            chain_response.raise_for_status()
            chain_data = chain_response.json()
            
            evolutions = []
            
            def extract_chain(chain):
                evolutions.append(chain['species']['name'].capitalize())
                if chain.get('evolves_to'):
                    for next_chain in chain['evolves_to']:
                        extract_chain(next_chain)
            
            extract_chain(chain_data['chain'])
            return evolutions
            
        except Exception as e:
            logger.error(f"Error obteniendo cadena de evolucion para {pokemon_name}: {str(e)}")
            return None

    @staticmethod
    def search_pokemon(query, gen1_only=True):
        """Busca Pokemon por nombre parcial."""
        try:
            results = []
            query_lower = query.lower()
            max_range = PokeAPIService.GENERATION_1_END if gen1_only else 1025
            
            for i in range(1, max_range + 1):
                try:
                    pokemon = pb.pokemon(i)
                    if query_lower in pokemon.name.lower():
                        results.append({
                            'id': pokemon.id,
                            'name': pokemon.name.capitalize(),
                            'image_url': pokemon.sprites.front_default,
                        })
                        if len(results) >= 10:
                            break
                except:
                    pass
            
            return results
        except Exception as e:
            logger.error("Error buscando Pokemon '" + query + "': " + str(e))
            return []
