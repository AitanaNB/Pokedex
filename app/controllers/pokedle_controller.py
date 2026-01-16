from flask import Blueprint, render_template, jsonify, request, session
from app.services.pokedle_service import PokedleService
from app.repositories.pokemon_repository import PokemonRepository
from app.utils.decorators import login_required

pokedle_bp = Blueprint('pokedle', __name__)

@pokedle_bp.route('/')
@login_required
def game():
    return render_template('pokedle/game.html')

@pokedle_bp.route('/api/start', methods=['POST'])
@login_required
def start_game():
    pokemon = PokedleService.get_random_pokemon()
    session['pokedle_target'] = pokemon.idPokemon
    return jsonify({"status": "ok"})


@pokedle_bp.route('/api/guess', methods=['POST'])
@login_required
def guess():
    data = request.json
    nombre = data.get("nombre", "").strip()

    if not nombre:
        return jsonify({"error": "Escribe una especie"}), 400

    guess = PokemonRepository.find_by_species(nombre)
    if not guess:
        return jsonify({"error": "Esa especie no existe"}), 404

    target_id = session.get("pokedle_target")
    target = PokemonRepository.find_by_id(target_id)

    comparison = PokedleService.compare_pokemons(target, guess)

    return jsonify({
        "correct": guess.nombreEspecie == target.nombreEspecie,
        "pokemon": {
            "nombre": guess.nombre,
            "ataque": guess.ataque,
            "ataqueEsp": guess.ataqueEsp,
            "def": guess.def_,
            "defEsp": guess.defEsp,
            "vel": guess.vel,
            "vida": guess.vida,
            "especie": guess.nombreEspecie
        },
        "comparison": comparison
    })



@pokedle_bp.route('/api/surrender', methods=['POST'])
@login_required
def surrender():
    target_id = session.get("pokedle_target")
    pokemon = PokemonRepository.find_by_id(target_id)

    return jsonify({
        "nombre": pokemon.nombreEspecie
    })
