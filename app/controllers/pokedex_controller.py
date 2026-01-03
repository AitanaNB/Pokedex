"""
Controlador de la Pokédex.
Maneja las rutas relacionadas con visualización y gestión de Pokémon.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.services.pokedex_service import PokedexService, EquipoService
from app.repositories.pokemon_repository import TipoRepository
from app.utils.decorators import login_required, approved_required

pokedex_bp = Blueprint('pokedex', __name__)


@pokedex_bp.route('/')
@pokedex_bp.route('/index')
@login_required
@approved_required
def index():
    """
    Página principal de la Pokédex.
    Muestra todas las especies disponibles.
    """
    # Obtener parámetros de búsqueda y filtro
    query = request.args.get('search', '').strip()
    tipo_filter = request.args.get('tipo', 'todos')
    
    # Obtener especies según filtros
    if query:
        especies = PokedexService.search_especies(query)
    elif tipo_filter and tipo_filter != 'todos':
        especies = PokedexService.filter_by_tipo(tipo_filter)
    else:
        especies = PokedexService.get_all_especies()
    
    # Obtener todos los tipos para el filtro
    tipos = PokedexService.get_tipos()
    
    return render_template('pokedex/index.html', 
                         especies=especies,
                         tipos=tipos,
                         tipo_filter=tipo_filter,
                         search_query=query,
                         user=session.get('user'))


@pokedex_bp.route('/especie/<nombre>')
@login_required
@approved_required
def especie_detail(nombre):
    """
    Muestra los detalles de una especie específica.
    """
    especie = PokedexService.get_especie_details(nombre)
    if not especie:
        flash('Especie no encontrada', 'warning')
        return redirect(url_for('pokedex.index'))
    
    return render_template('pokedex/especie_detail.html', 
                         especie=especie,
                         user=session.get('user'))


@pokedex_bp.route('/capture/<nombre>', methods=['POST'])
@login_required
@approved_required
def capture_pokemon(nombre):
    """
    Captura un Pokémon (crea una instancia de una especie).
    """
    nickname = request.form.get('nickname', '').strip()
    
    success, message, pokemon_id = PokedexService.create_pokemon_from_especie(nombre, nickname)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('pokedex.especie_detail', nombre=nombre))


@pokedex_bp.route('/equipos')
@login_required
@approved_required
def mis_equipos():
    """
    Muestra los equipos del usuario actual.
    """
    username = session.get('user')
    equipos = EquipoService.get_user_equipos(username)
    
    return render_template('pokedex/equipos.html', 
                         equipos=equipos,
                         user=username)


@pokedex_bp.route('/equipos/crear', methods=['POST'])
@login_required
@approved_required
def crear_equipo():
    """
    Crea un nuevo equipo.
    """
    nombre = request.form.get('nombre', '').strip()
    username = session.get('user')
    
    success, message, equipo_id = EquipoService.crear_equipo(username, nombre)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('pokedex.mis_equipos'))


@pokedex_bp.route('/equipos/<int:equipo_id>/eliminar', methods=['POST'])
@login_required
@approved_required
def eliminar_equipo(equipo_id):
    """
    Elimina un equipo.
    """
    username = session.get('user')
    success, message = EquipoService.delete_equipo(equipo_id, username)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    
    return redirect(url_for('pokedex.mis_equipos'))


@pokedex_bp.route('/api/especies', methods=['GET'])
@login_required
def api_especies():
    """
    API endpoint para obtener especies (para AJAX).
    """
    query = request.args.get('search', '').strip()
    tipo = request.args.get('tipo', 'todos')
    
    if query:
        especies = PokedexService.search_especies(query)
    elif tipo and tipo != 'todos':
        especies = PokedexService.filter_by_tipo(tipo)
    else:
        especies = PokedexService.get_all_especies()
    
    # Convertir a diccionarios
    especies_dict = []
    for e in especies:
        especies_dict.append({
            'nombreEspecie': e.nombreEspecie,
            'tipos': e.tipos,
            'vida': e.vida,
            'ataque': e.ataque,
            'defensa': e.def_,
            'esLegendario': e.esLegendario,
            'foto': e.foto
        })
    
    return jsonify(especies_dict)


@pokedex_bp.route('/api/equipos', methods=['GET'])
@login_required
def api_get_equipos():
    """
    API endpoint para obtener equipos del usuario en formato JSON.
    """
    username = session.get('user')
    equipos = EquipoService.get_user_equipos(username)
    
    equipos_dict = []
    for equipo in equipos:
        equipo_id = equipo.get('idEquipo', 0)
        pokemons = EquipoService.get_equipo_pokemon(equipo_id)
        
        # Convertir Pokémon a diccionarios simples
        pokemons_list = []
        for pokemon in pokemons:
            pokemons_list.append({
                'idPokemon': pokemon.get('idPokemon'),
                'nombre': pokemon.get('nombre'),
                'imagen': pokemon.get('imagen')
            })
        
        equipos_dict.append({
            'idEquipo': equipo_id,
            'nombre': equipo.get('nombre', ''),
            'pokemons': pokemons_list
        })
    
    return jsonify({'equipos': equipos_dict})


@pokedex_bp.route('/api/all-pokemon', methods=['GET'])
@login_required
def api_get_all_pokemon():
    """
    API endpoint para obtener todos los Pokémon de la BD en formato JSON.
    """
    try:
        pokemons = PokedexService.get_all_pokemon()
        
        pokemons_list = []
        for pokemon in pokemons:
            pokemons_list.append({
                'idPokemon': pokemon.get('idEspecie'),
                'nombre': pokemon.get('nombre'),
                'imagen': pokemon.get('imagen'),
                'name': pokemon.get('nombre')
            })
        
        return jsonify({'pokemons': pokemons_list})
    except Exception as e:
        import traceback
        print(f"ERROR en api_get_all_pokemon: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500
