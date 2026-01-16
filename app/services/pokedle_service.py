from app.repositories.pokemon_repository import PokemonRepository

class PokedleService:

    @staticmethod
    def get_random_pokemon():
        pokemon = PokemonRepository.get_random()
        if not pokemon:
            raise Exception("No hay Pokémon en la base de datos")
        return pokemon

    @staticmethod
    def compare_pokemons(target, guess):
        return {
            "nombre": guess.nombre == target.nombre,
            "ataque": guess.ataque == target.ataque,
            "ataqueEsp": guess.ataqueEsp == target.ataqueEsp,
            "def": guess.def_ == target.def_,
            "defEsp": guess.defEsp == target.defEsp,
            "vel": guess.vel == target.vel,
            "vida": guess.vida == target.vida,
            "especie": guess.nombreEspecie == target.nombreEspecie
        }
